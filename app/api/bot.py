from app import db
from app.api import bp
from flask import jsonify, request, abort
from twilio.twiml.messaging_response import MessagingResponse
import os

from app.models import State, StateSchema, User, UserSchema, News, NewsSchema

from chatterbot import ChatBot

chat_bot = ChatBot('break-chain')
# from chatterbot.trainers import ChatterBotCorpusTrainer
# Create a new trainer for the chat bot
# trainer = ChatterBotCorpusTrainer(chat_bot)
# Train the chat bot based on the english corpus
# trainer.train("chatterbot.corpus.english")

# NOTE: There is no point in training, problem with installation of chatterbot-corpus with pipenv, but works when
# installed from requirements.txt in a virtual environment

NEWS_API_KEY = os.environ["NEWS_API_KEY"]


@bp.route("/bot", methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    sender_number = request.values.get('From')
    print("IN BOT")
    print(incoming_msg)
    responded = False
    if 'add state' in incoming_msg:
        state_name = incoming_msg.split("add state", 1)[1]

        search_term = state_name.strip()
        search_term = f"%{search_term}%"

        state = State.query.filter((State.State.like(search_term))).first()
        stateSchema = StateSchema()
        state = stateSchema.dump(state)
        state_id = state["Id"]
        state_cured = state["Cured"]
        state_dead = state["Dead"]
        state_confirmed = state["Confirmed"]
        state_name = state["State"]

        check_user_state_exist = User.query.filter_by(MobileNo=sender_number, State_Id=state['Id']).first()

        if not check_user_state_exist:
            user_new = User(State_Id=state_id, MobileNo=sender_number)
            db.session.add(user_new)
            db.session.commit()

            msg.body(f"{state_name} added for COVID-19 tracking.")

        else:
            msg.body(f"{state_name} already added for tracking.")

        msg.body(f"Currently in {state_name}, there are \n {state_confirmed} cases confirmed \n {state_cured} cases "
                 f"cured \n {state_dead} deaths ")

        responded = True

    if 'all states' in incoming_msg:
        user_list = User.query.filter_by(MobileNo=sender_number).all()
        userSchema = UserSchema(many=True)
        user_list = userSchema.dump(user_list)

        print(user_list)
        if not user_list:
            msg.body(f"No states added currently add it like *add state Gujarat*")
        for user_detail in user_list:
            state_id = user_detail["states"]

            state = State.query.filter_by(Id=state_id).first()
            stateSchema = StateSchema()
            state = stateSchema.dump(state)
            state_id = state["Id"]
            state_cured = state["Cured"]
            state_dead = state["Dead"]
            state_confirmed = state["Confirmed"]
            state_name = state["State"]

            empty = "‎‎ ‎"  # invisible character, to get new line hack
            msg.body(empty)
            msg.body(
                f" Currently in \n *{state_name}*, there are \n {state_confirmed} cases confirmed \n {state_cured} cases "
                f"cured \n {state_dead} deaths. \n {empty}\n")

        responded = True
    if 'remove state' in incoming_msg:
        state_name = incoming_msg.split("remove state", 1)[1]
        search_term = state_name.strip()
        search_term = f"%{search_term}%"

        user_list = User.query.filter_by(MobileNo=sender_number).all()
        userSchema = UserSchema(many=True)
        user_list = userSchema.dump(user_list)

        print(user_list)
        if not user_list:
            msg.body(f"No states to remove currently add it like *add state Gujarat*")

        if user_list:
            state = State.query.filter((State.State.like(search_term))).first()
            stateSchema = StateSchema()
            state = stateSchema.dump(state)
            state_id = state["Id"]
            state_name = state["State"]

            User.query.filter_by(MobileNo=sender_number, State_Id=state_id).delete()
            db.session.commit()
            msg.body(f"{state_name} removed from tracking")

        responded = True

    if 'get news' in incoming_msg:

        all_news = News.query.all()
        news_schema = NewsSchema(many=True)
        all_news = news_schema.dump(all_news)

        for news in all_news:
            title = news["Title"]

            empty = "‎‎ ‎"  # invisible character, to get new line hack
            msg.body(f" \n *Title* :  {title} \n {empty}\n ")

        responded = True

    if "what is covid 19" in incoming_msg:
        msg.body("COVID-19 is a disease caused by a new strain of coronavirus. ‘CO’ stands for corona, ‘VI’ for virus, and ‘D’ for disease. Formerly, this disease was referred to as ‘2019 novel coronavirus’ or ‘2019-nCoV.’ The COVID-19 virus is a new virus linked to the same family of viruses as Severe Acute Respiratory Syndrome (SARS) and some types of common cold")

        responded = True
    if "symptoms of covid 19" in incoming_msg:
        msg.body("Symptoms can include fever, cough and shortness of breath. In more severe cases, infection can cause pneumonia or breathing difficulties. More rarely, the disease can be fatal. These symptoms are similar to the flu (influenza) or the common cold, which are a lot more common than COVID-19. This is why testing is required to confirm if someone has COVID-19.")

        responded = True

    if "how to be safe" in incoming_msg:
        msg.body('''✓ staying home when sick
✓ covering mouth and nose with flexed elbow or tissue when coughing or sneezing. Dispose ofused tissue immediately;
✓ washing hands often with soap and water; and
✓ cleaning frequently touched surfaces and objects
        ''')
        responded = True

    if "help" in incoming_msg:
        msg.body('''You can give me the following commands
👉 add state {state name}
👉 all states
👉 remove state {state name}
👉 get news
👉 what is covid 19
👉 symptoms of covid 19
👉 how to be safe
👉 help
''')
        responded = True
    if not responded:
        chatter_resp = chat_bot.get_response(incoming_msg)
        # print(chatter_resp)
        # print(chatter_resp.serialize())
        serialize_resp = chatter_resp.serialize()
        res_text = serialize_resp["text"]
        # print(res_text)

        empty = "‎‎ ‎"  # invisible character, to get new line hack
        msg.body(f"{res_text}")
        msg.body(f"{empty} \n you can type *help* for menu")
    return str(resp)
