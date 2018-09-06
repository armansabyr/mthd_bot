# -*- coding: utf-8 -*-
import config
import telebot
from telebot import types
import requests
# from urllib.parse import urlencode
# from urlparse import urlparse
# from urllib2 import Request
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# from urllib.request import Request, urlopen
from telegraphapi import Telegraph

telegraph = Telegraph()
telegraph.createAccount("Method.api")

# telegraph_token = 'c56794f4b7cdaaacece5b8ca4def88c915ecdaa63353e13bc67d4c2a74ef'
bot = telebot.TeleBot(config.token)
proglang = {
"Python": 34, #python 3.6
"C++": 11,    #gcc 6.4.0
"Java":27,  #jdk 8
"Ruby": 38,  #ruby 2.4
}
#
@bot.message_handler(commands=['1'])
def handle_start_help(message):
    print(message)
    bot.send_message(message.chat.id, "http://telegra.ph/Solve-Me-First-07-24")

def send_request(downloaded_file, input, output, lang_id):
    """
    send request Judje API to check task
    """
    url = "https://api.judge0.com/submissions?wait=true"
    data = {
        "source_code": downloaded_file.decode("utf-8"),
        "language_id": 34,
        "number_of_runs": "1",
        "stdin": input,
        "expected_output": output,
        "cpu_time_limit": "2",
        "cpu_extra_time": "0.5",
        "wall_time_limit": "5",
        "memory_limit": "128000",
        "stack_limit": "64000",
        "max_processes_and_or_threads": "30",
        "enable_per_process_and_thread_time_limit": False,
        "enable_per_process_and_thread_memory_limit": True,
        "max_file_size": "1024"
    }
    r = requests.post(url, data=data)
    debug(r)
    return (r)

def make_markup_tasks(data):
    print(data)
    markup = types.InlineKeyboardMarkup()
    print("here we go")
    # print(data[0]['title'])
    for task in data:
        # print(task['url'])
        # if (task['id']):
        #     continue
        # print(task['title'])
        # print(task['url'][0:16])
        # url =
        page = telegraph.createPage(task['title'], html_content="<b>"+ str(task['description'])+"</b>")
        t_url = 'http://telegra.ph/{}'.format(page['path'])
        # t_url = 'https://telegra.ph//Any-task-rage-08-15' #requests.get(url)
        # t_url.json()['result']['url']
        curr = types.InlineKeyboardButton(str(task['title']),
            callback_data=t_url)
        markup.add(curr)
        # markup.row(*row)
    # markup.row(*row)
    # row=[]
    # row.append(types.InlineKeyboardButton("<",callback_data="previous-month"))
    # row.append(types.InlineKeyboardButton(" ",callback_data="ignore"))
    # row.append(types.InlineKeyboardButton(">",callback_data="next-month"))
    # markup.row(*row)
    return markup

#перенести в другой файл, подгружает таски
def load_tasks(message):
    print(message)
    url = "http://0.0.0.0:3000/api/v1/tasks.json"
    payload = {
        'chat_id': message.chat.id
    }
    r = requests.post(url, json=payload)
    print(r)
    data = r.json()

    return data

    # debug(r)

def send_m(message, text):
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["start"])
def add_new_number(message):
    print(message)
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    reg_button = types.KeyboardButton(text="Share your phone number", request_contact=True)
    keyboard.add(reg_button)
    response = bot.send_message(message.chat.id,
                                "You should share your phone number",
                                reply_markup=keyboard)

    # url = "http://0.0.0.0:3000/api/v1/tasks.json"
    # payload = {
    # 	'chat_id': message.chat.id,
    #     'name': message.chat.username
    # }
    # r = requests.post(url, json=payload)
    # markup = types.ReplyKeyboardMarkup()
    # markup.row('Tasks', 'LeaderBoard')
    # bot.send_message(message.chat.id, "Welcome, {0}!".format(payload['name']), reply_markup=markup)
    # debug(r)

@bot.message_handler(content_types=["contact"])
def load(message):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    chat_id = message.json['contact']['user_id']
    phone_number = message.json['contact']['phone_number']
    url = "http://0.0.0.0:3000/api/v1/adduser.json"
    print('87778172034'[1:])
    payload = {
    	'chat_id': chat_id,
        'phone_number': '87778172034'[1:]#phone_number[2:]
    }
    r = requests.post(url, json=payload)
    markup = types.ReplyKeyboardMarkup()
    markup.row('Tasks', 'LeaderBoard')
    status = r.json()['status']
    if status == "OK":
        bot.send_message(chat_id, "Welcome, {0}!".format(message.json['contact']['first_name']), reply_markup=markup)
    else:
        bot.send_message(chat_id, "Your phone is not registred in Method.kz. Tell your teacher to add you to the list of students.")
    debug(r)

@bot.message_handler(content_types=["text"])
def load(message):
    if (message.text == "Tasks"):
        data = load_tasks(message)
        status = data['status']
        if status == "OK":
            markup = make_markup_tasks(data["titles"])
            bot.send_message(message.chat.id, "Tasks", reply_markup = markup)
            # bot.send_message(message.chat.id, data["titles"][0]["title"])
            # bot.send_message(message.chat.id, data["titles"][0]["url"])
        else:
            bot.send_message(chat_id, "You are not registered in Method.kz")

@bot.callback_query_handler(func=lambda call: 'http://telegra.ph/' in call.data)
def get_day(call):
    print(call)
    chat_id = call.message.chat.id
    url = call.data
    bot.send_message(chat_id, url)
    # bot.send_message(chat_id, 'название отправляемого файла ' + file_name)
#     saved_date = current_shown_dates.get(chat_id)
#     if(saved_date is not None):
#         day=call.data[13:]
#         date = datetime.datetime(int(saved_date[0]),int(saved_date[1]),int(day),0,0,0)
#         bot.send_message(chat_id, str(date))
#         bot.answer_callback_query(call.id, text="")

#     else:
#         #Do something to inform of the error
#         pass

def debug(r):
    print(r.status_code, r.reason)
    print(r.text)
    print(type(r))

@bot.message_handler(content_types=["document"])
def repeat_all_message(message):
    print(message)
    chat_id = message.chat.id
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    print(downloaded_file)
    url = "http://0.0.0.0:3000/api/v1/get_results.json"
    payload = {
        'chat_id': message.chat.id,
        'filename': message.document.file_name.split(".")[0]
    }
    results_req = requests.get(url, json=payload)
    results = results_req.json()
    lang_id = proglang[results['proglang']]
    correct_test = 0
    if results["status"] == "OK":
        for test in results['tests']:
            r = send_request(downloaded_file, test["input"], test["output"], lang_id)
            debug(r)
            if (r.status_code == 201):
                if (r.json()["status"]["description"] == "Accepted"):
                    correct_test += 1
                else:
                    send_m(message, "Wrong answer")
            else:
                send_m(message, "Wrong answer")
        if correct_test == len(results['tests']):
            url = "http://0.0.0.0:3000/api/v1/submit.json"
            payload = {
                'chat_id': chat_id,
                'filename': message.document.file_name
            }
            submit = requests.get(url, json=payload)
            print(submit.json())
            status = submit.json()['status']
            if status == "OK":
                send_m(message, "Correct answer recorded")
            else:
                send_m(message, "Couldn't submit")
    else:
        send_m(message, "Couldn't find mathicg task:\n Try to change filename")

if __name__ == "__main__":
    bot.polling(none_stop=True)
