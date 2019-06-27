import telebot
import time
import datetime
import random
from threading import Thread
import json
now = datetime.datetime.now()    
    
token = "864457409:AAFFnm9ORq-5akxuxpAIlC1mCQ6I6attVaY"
telebot.apihelper.proxy = {'https': 'socks5h://geek:socks@t.geekclass.ru:7777'}

bot = telebot.TeleBot(token=token)

users = {}  # id <=> timetable
#users[user] = timetable
last_save = {}

def save():
    with open('data.json', 'w') as file:
        data = json.dumps([users, last_save])
        file.write(data)

def load():
    try:
        with open('data.json', 'r') as file:
            users, last_save = json.loads(file.read())
    except:
            save()
load()

def sender():
    global users
    while True:
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        print(current_time)
        for user in users:
            for event_time, event in users[user]:
                print(event_time, current_time)
                if event_time == current_time:
                    bot.send_message(user, "Наступает событие: {}!".format(event))
                    s = ['CAADAgADjgADEyscBFeorVcqn4_hAg', 'CAADAgADhQADEyscBLji2-mncNu6Ag', 'CAADAgADnAADEyscBAmmHWlOokzmAg', 'CAADAgADlQADEyscBCJrPko1HxqnAg', 'CAADAgADngADEyscBDHY4Sshc4VGAg', 'CAADAgADpgADEyscBH4_c_4faUwVAg']
                    bot.send_sticker(user, random.choice(s))

            if time.time() - last_save[user] > 60 * 60 * 24:
                users[user] = []

        time.sleep(60)

        
@bot.message_handler(content_types=['text'])
def rosp(message):
    global users
    b = message.text.lower()
    if "расписание" in b:
        bot.send_message(message.chat.id, "Zapomnil...")
        users[message.chat.id] = []
        lines = message.text.split('\n')
        last_save[message.chat.id] = time.time()
        for line in lines:
            if line[:2].isdigit():
                event_time = line[:5]
                name = line[6:] 
                users[message.chat.id].append((event_time, name))
        save()

def polling():
    bot.polling(none_stop=True) 
polling_thread = Thread(target=polling)
sender_thread = Thread(target=sender)

polling_thread.start()
sender_thread.start()
