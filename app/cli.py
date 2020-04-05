from app import db
from app.models import State, User, StateSchema, UserSchema, News
import requests
from bs4 import BeautifulSoup
import json
import os

from datetime import datetime

from newsapi import NewsApiClient
newsapi = NewsApiClient(api_key=os.environ["NEWS_API_KEY"])


def register(app):

    @app.cli.command()
    def update_news():
        top_headlines = newsapi.get_top_headlines(q='covid-19',
                                                  language='en',
                                                  country='in')
        articles = top_headlines["articles"]

        News.query.delete()

        for article in articles:
            title = article["title"]
            description = article["description"]

            new_news = News(Title=title, Description=description)
            db.session.add(new_news)

        db.session.commit()

    @app.cli.command()
    def scrape():
        """Scrape https://www.mohfw.gov.in/ for data"""
        headers = {
            0: "id",
            1: "state",
            2: "confirmed",
            3: "cured",
            4: "deaths"
        }

        def get_table_from_web():
            url = "https://mohfw.gov.in"
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            div = soup.find('div', class_='data-table')
            extracted_time = "2020-03-28 17:45:00"

            table = div.find('table', class_='table')
            return table, extracted_time

        def html_to_json(content, time, indent=None):
            rows = content.find_all("tr")
            data = []
            for row in rows:
                cells = row.find_all("td")

                if len(cells) != 0 and len(cells) == len(headers):
                    items = {}
                    for index in headers:
                        items[headers[index]] = cells[index].text.replace(
                            '\n', '').replace('#', '')

                    data.append(items)
                    body = {}
                    body["state_data"] = data

            total = rows[len(rows) - 2].find_all("strong")
            total_items = {}

            for index in headers:
                if index != 0 and index != 1:
                    total_items[headers[index]] = total[index - 1].text

            body["total_data"] = total_items
            body["last_updated"] = str(time)
            response = {"data": body}
            return response

        def data_extract():
            table, extracted_time = get_table_from_web()
            state_wise_data = html_to_json(table, datetime.now())
            last_extracted_content = state_wise_data
            return last_extracted_content

        extracted_data = data_extract()
        state_list = extracted_data["data"]["state_data"]

        # {'id': '29', 'state': 'West Bengal', 'confirmed': '69', 'cured': '10', 'deaths': '3'}

        for state in state_list:
            print(state)
            new_state = State(State=state["state"],
                              Confirmed=state["confirmed"],
                              Cured=state["cured"],
                              Dead=state["deaths"])
            db.session.add(new_state)

        db.session.commit()
