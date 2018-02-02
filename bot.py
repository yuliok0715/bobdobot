import config
import os
import telebot
import bond_quotes
import sqlalchemy as sa
from random import choice
from models import Base, Quote
from sqlalchemy.orm import sessionmaker
from flask import Flask, request



engine = sa.create_engine(config.DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)


bot = telebot.TeleBot(config.token)
app = Flask(__name__)



@app.route(f"/{config.token}", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"https://shielded-river-72517.herokuapp.com/{config.token}")
    return "!", 200

@bot.message_handler(commands=['about'])
def about_bot(message):
    text = """Присвячується Віктору Григоровичу, одному з найпозитивніших викладачів у моєму житті."""
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=["text"])
def help_message(message):
    session = Session()
    text = choice(session.query(Quote.quote))
    bot.send_message(message.chat.id, text)
    session.close()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    session = Session()
    for line in open('quotes.txt'):
        session.add(Quote(quote=line))
    session.commit()
    session.close()