import telebot
import datetime
import time
import random

bot = telebot.TeleBot("ваш токен")

user_reminders = {}

def send_reminders():
    while True:
        now = datetime.datetime.now()
        now_str = now.strftime("%H:%M")
        now_hour = now.hour

        for user_id, reminder_data in list(user_reminders.items()):
            next_time = datetime.datetime.strptime(reminder_data["next_time"], "%H:%M")

            if now_str == next_time.strftime("%H:%M") and (8 <= now_hour < 22):
                bot.send_message(user_id, "Напоминание - выпей стакан воды")
                next_time += datetime.timedelta(hours=3)

                if next_time.hour >= 22:
                    next_time += datetime.timedelta(hours=((24 - next_time.hour) + 8))
                user_reminders[user_id]["next_time"] = next_time.strftime("%H:%M")
                time.sleep(61)
        time.sleep(10)

def set_time(message):
    try:
        initial_time_str = message.text
        user_id = message.chat.id
        initial_time = datetime.datetime.strptime(initial_time_str, "%H:%M")

        if initial_time.hour >= 22 or initial_time.hour < 8:
            bot.reply_to(message, "Введено время в ночном режиме (с 22:00 до 8:00). Установка напоминаний в это время недоступна. Пожалуйста, выберите другое время.")
            ask_for_time(message)
        else:
            now = datetime.datetime.now()
            if initial_time.time() < now.time():
                next_time = initial_time + datetime.timedelta(days=1)
            else:
                next_time = initial_time

            next_time_str = next_time.strftime("%H:%M")
            user_reminders[user_id] = {"initial_time": initial_time_str, "next_time": next_time_str}
            bot.reply_to(message, f"Установлено время первого напоминания: {initial_time_str}. Следующее напоминание будет в {next_time_str}.")

    except ValueError:
        bot.reply_to(message, "Неверный формат времени. Попробуйте еще раз.")
        ask_for_time(message)

    except Exception as e:
        bot.reply_to(message, f"Что-то пошло не так. Попробуйте еще раз. Ошибка: {e}")
        ask_for_time(message)

def ask_for_time(message):
    msg = bot.reply_to(message, "Введите время первого напоминания в формате ЧЧ:ММ (например, 09:00):")
    bot.register_next_step_handler(msg, set_time)

@bot.message_handler(commands=['settingtime'])
def set_initial_reminder(message):
    ask_for_time(message)

@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.chat.id
    now = datetime.datetime.now()
    bot.reply_to(message, "Время выпить стакан воды")

    if 8 <= now.hour < 19:
        next_time = now + datetime.timedelta(hours=3)

    else:
        next_hours_till_morning = ((24 - now.hour) + 8) % 24
        next_time = now + datetime.timedelta(hours=next_hours_till_morning)
    next_time_str = next_time.strftime("%H:%M")
    user_reminders[user_id] = {"next_time": next_time_str}
    bot.send_message(user_id, f"Следующее напоминание будет в {next_time_str}.\nБот не будет вас беспокоить в период с 22:00 - 8:00(ночной режим).\n /help - для получения помощи")

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.reply_to(message, f"Мои команды: \n/start - для старта напоминаний выпить воды. "
                          f"\n/fact - факты о воде. \n/foto - фотография воды. \n/audio - музыка воды. "
                          f"\n/settingtime - Если хотите задать боту свое начальное время (будет приходить уведомление с переодичностью в 3 часа)")

@bot.message_handler(commands=['fact'])
def fact_message(message):
    list = ["*Вода составляет около 71% поверхности Земли и является жизненно важным ресурсом для всех организмов.*",
            "*Вода является единственным веществом, которое существует в трех состояниях - жидком, твердом (лед) и газообразном (пар).*",
            "*Молекула воды состоит из двух атомов водорода и одного атома кислорода, поэтому ее химическая формула H2O.*",
            "*Вода обладает высокой теплоемкостью, что позволяет ей сохранять температурные условия и уравновешивать климат на Земле.*",
            "*Вода является универсальным растворителем и играет важную роль во всех биологических процессах, включая пищеварение, транспорт питательных веществ и выведение отходов из организма.*"
            "*Вода имеет аномальное свойство плавать в жидком состоянии на твердой воде в виде льда, что помогает поддерживать жизнь в океанах и водоемах.*",
            "*Вода является отличным растворителем для многих веществ, что способствует химическим реакциям и биологическим процессам.*",
            "*Вода играет ключевую роль в процессе фотосинтеза, позволяя растениям преобразовывать солнечный свет в энергию.*",
            "*Вода способствует терморегуляции организма, поддерживая постоянную температуру внутри его клеток.*",
            "*Вода является неотъемлемой частью многих культур и религиозных обрядов в различных культурах мира, символизируя очищение, обновление и жизнь.*"]
    random_fact = random.choice(list)
    bot.reply_to(message, f"Вот один интересный факт о воде:  \n{random_fact}")

@bot.message_handler(commands=['foto'])
def foto_message(message):
    photo_urls = [
        "https://oskada.ru/wp-content/uploads/2015/11/315.jpg",
        "https://traveltimes.ru/wp-content/uploads/2022/06/vod2.jpg",
        "https://live.staticflickr.com/3336/3213516246_3aa7869d18_b.jpg",
        "https://vsegda-pomnim.com/uploads/posts/2022-04/1649112171_59-vsegda-pomnim-com-p-voda-v-prirode-foto-77.jpg",
        "https://sportishka.com/uploads/posts/2022-02/1645635616_17-sportishka-com-p-morskaya-voda-turizm-krasivo-foto-20.jpg"
        "https://sportishka.com/uploads/posts/2022-11/1667580766_44-sportishka-com-p-krasota-vodi-v-more-oboi-50.jpg",
        "https://vodaminsk.by/wp-content/uploads/2022/03/vodaST.jpg",
        "https://i.pinimg.com/originals/d8/7a/13/d87a13178c146167c5aa9e724a956899.jpg",
        "https://wips.plug.it/cips/paginegiallecasa/cms/2020/07/55564000_m.jpg?w=832&amp;h=468&amp;a=c",
        "https://catherineasquithgallery.com/uploads/posts/2021-02/1612770244_158-p-fon-voda-goluboi-vodnii-219.jpg",
        "https://media.cntraveller.in/wp-content/uploads/2018/11/shutterstock_326584550.jpg",
        "https://b2344126.smushcdn.com/2344126/wp-content/uploads/2021/08/AdobeStock_193256438-scaled.jpeg?lossy=0&strip=1&webp=1"
        ]
    random_photo = random.choice(photo_urls)
    bot.send_photo(message.chat.id, photo=random_photo)

@bot.message_handler(commands=['audio'])
def send_audio_file(message):
    with open('water.mp3', 'rb') as f:
        bot.send_audio(message.chat.id, audio=f.read())

bot.polling(none_stop=True)