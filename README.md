# Welcome to Break the chain 👋
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://choosealicense.com/licenses/mit/)
[![Twitter: aks2899](https://img.shields.io/twitter/follow/aks2899.svg?style=social)](https://twitter.com/aks2899)



## 🤩 How to Run

Prerequisite : 
Install Sqlite

Basic setup:
    
    $ git clone https://github.com/Akshay090/break-the-chain 
    $ cd break-the-chain
    $ pip install pipenv
    $ pipenv shell
    $ pipenv install
    
## 🤐 Set env value for News Api
> Get your api from https://newsapi.org/
>
make a .env file in project root directory like example.env,
then add api key to it
    
Setup Database

    $ flask db init
    $ flask db migrate
    $ flask db upgrade
    
Scrape and Populate database 
> It get covid-19 data from https://www.mohfw.gov.in/
>and news from https://newsapi.org/

    $ flask scrape
    $ flask update-news
    
## 😋 Run Flask application:

    $ flask run
    
## 🎇 Now make the port available to twilio

Install ngrok
```
ngrok http 5000
```
Now add the ngrok url to https://www.twilio.com/console/sms/whatsapp/sandbox
to WHEN A MESSAGE COMES IN to with whatsapp
OR to https://www.twilio.com/console/phone-numbers and click on phone
no you bought, and add ngrok url to A MESSAGE COMES IN field

This application is written using Python 3.7.

# ✨ Bot commands

👉 add state {state name}

👉 all states

👉 remove state {state name}

👉 get news

👉 what is covid 19

👉 symptoms of covid 19

👉 how to be safe
