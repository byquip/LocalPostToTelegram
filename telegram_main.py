import sys
import threading
import time
from get_emails import ReceiveMails
import telebot  # type: ignore
import logging
import yaml

# log level
logging.basicConfig(level=logging.INFO)
conf = yaml.safe_load(open("conf/application.yml"))
chat_id = conf['telegram']['chat_id']
telbot = telebot.TeleBot(conf['telegram']['TOKEN'])  # init
ReceiveMails_inst = ReceiveMails(conf)
link = conf['user']['link']
errors = list()


@telbot.message_handler(commands=['start'])
def welcome(message):
    if message.chat.id != chat_id:
        telbot.send_message(message.chat.id, text="Leave this bot it's not for you")
        return
    telbot.send_message(message.chat.id, text=f"Ready to check your mails {message.chat.first_name}")


@telbot.message_handler(commands=['get'])  # type: ignore
def welcome(message):
    if message.chat.id != chat_id:
        telbot.send_message(message.chat.id, text="Leave this bot it's not for you")
        return
    n, froms, heads = ReceiveMails_inst()
    if n > 0:
        if n > 1:
            for letter_num in range(n):
                tel_send(letter_num, froms, heads)
        else:
            tel_send(0, froms, heads)
    else:
        telbot.send_message(message.chat.id, text="There is no letters")


def telbot_tread():
    while True:
        try:
            telbot.polling(none_stop=True, interval=1)
        except Exception:
            er = f"Telebot error: {sys.exc_info()}"
            errors.append(er)
            print(er)


def email_tread():
    global chat_id
    while True:
        time.sleep(60)
        try:
            n, froms, heads = ReceiveMails_inst()
            if n > 0:
                if n > 1:
                    for letter_num in range(n):
                        tel_send(letter_num, froms, heads)
                else:
                    tel_send(0, froms, heads)
        except Exception:
            er = f"Telebot error: {sys.exc_info()}"
            errors.append(er)
            print(er)


def tel_send(letter_num, froms, heads):
    text = f"From: {froms[letter_num]}\n" \
           f"Subject: {heads[letter_num]}\n" \
           f"[login]({link})"
    telbot.send_message(chat_id, text=text, parse_mode='Markdown')


def main():
    telbot_trd = threading.Thread(target=telbot_tread)
    email_trd = threading.Thread(target=email_tread)

    telbot_trd.start()
    email_trd.start()


if __name__ == "__main__":
    main()
