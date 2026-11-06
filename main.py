import telebot
import psutil
from config import token
bot = telebot.TeleBot(token)
markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)    
btn1 = telebot.types.KeyboardButton('CPU Usage')
btn2 = telebot.types.KeyboardButton('Memory Usage')
btn3 = telebot.types.KeyboardButton('Disk Usage')
btn4 = telebot.types.KeyboardButton('CPU All Cores')
markup.add(btn1, btn2, btn3, btn4)

@bot.message_handler(commands=['start'])
def start(message): 
    bot.send_message(message.chat.id, 'Welcome! Please choose an option:', reply_markup=markup)

@bot.message_handler(content_types=["text"])
def handle_metrics(message):
    if message.text == "CPU Usage":
        cpu = psutil.cpu_percent(interval=1)
        bot.send_message(message.chat.id, f"💻 Использование CPU: {cpu}%")

    elif message.text == "Memory Usage":
        ram = psutil.virtual_memory()
        bot.send_message(
            message.chat.id, f"🧠 Использование памяти: {ram.percent}%"
        )

    elif message.text == "Disk Usage":
        disk = psutil.disk_usage("/")
        bot.send_message(
            message.chat.id, f"💾 Использование диска: {disk.percent}%"
        )

    elif message.text == "CPU All Cores":
        cores = psutil.cpu_percent(interval=1, percpu=True)
        phys_count = psutil.cpu_count(logical=False)

        # Просто делим один список на две части по индексу
        phys_cores = [
            f"🔹 Физ ядро {i+1}: {u}%" for i, u in enumerate(cores[:phys_count])
        ]
        logic_cores = [
            f"🔸 Лог ядро {i+1}: {u}%"
            for i, u in enumerate(cores[phys_count:])
        ]

        # Склеиваем всё в одно сообщение
        report = (
            "📊 **Нагрузка по ядрам:**\n\n"
            + "\n".join(phys_cores)
            + "\n\n"
            + "\n".join(logic_cores)
        )

        bot.send_message(message.chat.id, report, parse_mode="Markdown")


bot.infinity_polling()