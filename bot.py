import config
import os
import telebot

from flask import Flask, request




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


@bot.message_handler(commands=['help_me'])
def help_message(message):
    """Send message to user with explaining game rules."""

    text = """
    Hello, I'm a super dictionary bot!
    I'll glad to help you with learning new words!
    For register please call /start command!
    Game: first of all you need to add some words to you dictionary
    call /add <your word> command to add new one
    When you'll be ready, just call /game command.
    If you feel that it's enough for today, call /end command just from game
    To see list of all words in dictionary - call /show_all command!
    Hope you'll like me!
    Let's start!
    """
    bot.send_message(message.chat.id, text)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)