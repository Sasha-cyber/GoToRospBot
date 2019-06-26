import telebot
import time
import datetime
from threading import Thread
now = datetime.datetime.now()    
    
token = "733795990:AAH2i-rEl1CEnCoNnryQrAU2EPlhYJ0dtxQ"
telebot.apihelper.proxy = {'https': 'socks5h://geek:socks@t.geekclass.ru:7777'}

bot = telebot.TeleBot(token=token)
groups = []
"""
@bot.message_handler(content_type=['text'])
def groupc(message):
    group =  message.chat.id
    if group not in groups:
        rosp(message)
# TODO: запоминать расписание для каждого из чатов по отдельности
"""
timetable = []
users = []
last_save = 0

def sender():
    global timetable
    while True:
        # TODO: узнать текущее время в формате HH:MM
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        print(current_time)
        for user in users:
            for event_time, event in timetable:
                if event_time == current_time:
                    bot.send_message(user, event)
        
        if time.time() - last_save > 60 * 60 * 24:
            timetable = []

        time.sleep(60)

        
@bot.message_handler(content_types=['text'])
def rosp(message):
    global timetable
    if message.chat.id not in users:
        users.append(message.chat.id)
        b = message.text.lower()
    if "расписание" in b:
        timetable = []
        lines = message.text.split('\n')
        for line in lines:
            if line[:2].isdigit():
                event_time = line[:5]
                name = line[6:] 
                timetable.append((event_time, name))
        last_save = time.time()
        print(timetable)        

def polling():
    bot.polling(none_stop=True) 
# TODO: запустить сендер в отдельном потоке
polling_thread = Thread(target=polling)
sender_thread = Thread(target=sender)

polling_thread.start()
sender_thread.start()