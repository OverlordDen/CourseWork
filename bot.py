import telebot
import config
import time
import utils
from SQLighter import SQLighter
from config import database_name
import sqlite3
import schedule

con = sqlite3.connect(database_name)
cur = con.cursor()
bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['set_id'])
def Set_ID(message):
    db_worker = SQLighter(config.database_name)
    i = 0
    mass = []
    while i < utils.get_rows_count():
        row = db_worker.select_single(i+1)
        mass.append(row[2])
        i = i + 1

    bot.send_message(message.chat.id, "*примітка (якщо вивведете невірний номер, буде ввімкнена затримка)\n" +
                                      "Введіть номер зілікової книги:")
    utils.set_user_game(message.chat.id, mass)
    db_worker.close()


@bot.message_handler(commands=['grades'])
def send_grades(message):
    db_worker = SQLighter(config.database_name)
    i = 0
    n = 4
    while i < utils.get_rows_count():
        row = db_worker.select_single(i+1)
        if row[3] == str(message.chat.id):
            while n < 7:
                bot.send_message(message.chat.id, str(row[1])+" ("+str(row[n]) + ") = " + str(row[n+1]))
                n = n + 2
            break
        i = i + 1
    db_worker.close()

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Якщо в вас немає прив'язки до аккаунта і ви хочете прив'язати свій аккаунт телеграм введіть /set_id " +
                                      "в іншому випадку, щоб вивести оцінки, enter /grades " +
                                      "щоб видалити прив'язку введіть, /del ")

@bot.message_handler(commands=['all'])
def send_all(message):
    def job():
        if str(message.chat.id) == '530401755':
            db_worker = SQLighter(config.database_name)
            i = 1
            while i <= utils.get_rows_count():
                row = db_worker.select_single(i)
                if row[3] == "":
                    while row[3] == "":
                        i = i + 1
                        row = db_worker.select_single(i)

                n = 4
                while n < 7:
                    bot.send_message(int(row[3]), str(row[1]) + " (" + str(row[n]) + ") = " + str(row[n + 1]))
                    n = n + 2
                i = i + 1
            db_worker.close()
        else:
            bot.send_message(message.chat.id, "У вас немає прав для цього!")
    job()
    schedule.every(1).minutes.do(job)
    while True:
        schedule.run_pending()


@bot.message_handler(commands=['del'])
def delete(message):
    db_worker = SQLighter(config.database_name)
    i = 0
    while i < utils.get_rows_count():
        i = i + 1
        row = db_worker.select_single(i)
        if row[3] == str(message.chat.id):
            db_worker.del_id(i)
            bot.send_message(message.chat.id, "Видалення прив'язки до id (" + str(row[1]) + ") було успішним")
            break
    db_worker.close()



@bot.message_handler(commands=['dig'])
def check_answer(message):
    bot.send_message(message.chat.id, "Щоб прив'язати ID введіть /set_id \n"
                                      "Щоб дізнатись оцінки, введіть /grades \n"
                                      "Щоб розіслати оцінки, введіть /all \n"
                                      "Щоб видалити прив'язку, введіть /del \n"
                                      "Для допомоги, введіть /help")

@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    answer = utils.get_answer_for_user(message.chat.id)
    if not answer:
        bot.send_message(message.chat.id, 'Щоб почати діалог /dig')
    else:
        i = 0
        for y in answer:
            i = i + 1
            if message.text == y:
                bot.send_message(message.chat.id, 'Успішно!')
                db_worker = SQLighter(config.database_name)
                row = db_worker.select_single(i)
                db_worker.set_id(str(message.chat.id), i)
                db_worker.close()
                break
        else:
            bot.send_message(message.chat.id, 'Не вірно! Спробуйте ще раз!')
            utils.finish_user_game(message.chat.id)
            bot.send_message(message.chat.id, 'Щоб почати діалог /dig')
            time.sleep(30)

if __name__ == '__main__':
    bot.polling(none_stop=True)
    utils.count_rows()
