import telebot
from telebot import types
from load_config import load_config
import subprocess

config = load_config()
BOT_TOKEN = config.get("BOT_TOKEN")

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_plan = types.KeyboardButton("План")
    btn_fact = types.KeyboardButton("Факт")
    markup.add(btn_plan)
    markup.add(btn_fact)
    bot.send_message(message.chat.id, "Привет! \n\n Кнопка 'План' -- все задачи в работе \n Кнопка 'Факт' -- выполненные задачи за сегодня", reply_markup=markup)

# Обработчик "План"
@bot.message_handler(func=lambda message: message.text == "План")
def handle_plan_button(message):
    try:
        subprocess.run(["python", "plan.py"], check=True)

        with open("plan_output.txt", "r", encoding="utf-8") as file:
            plan_content = file.read()

        # Отправка содержимого файла в формате monospace
        bot.send_message(message.chat.id, f"```\n{plan_content}\n```", parse_mode="MarkdownV2")

    except FileNotFoundError:
        bot.send_message(message.chat.id, "Файл plan_output не найден. Проверьте работу скрипта plan.py.")
    except subprocess.CalledProcessError:
        bot.send_message(message.chat.id, "Произошла ошибка при выполнении скрипта plan.py.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

# Обработчик "Факт"
@bot.message_handler(func=lambda message: message.text == "Факт")
def handle_plan_button(message):
    try:
        subprocess.run(["python", "fact.py"], check=True)

        with open("fact_output.txt", "r", encoding="utf-8") as file:
            fact_content = file.read()

        # Отправка содержимого файла в формате monospace
        bot.send_message(message.chat.id, f"```\n{fact_content}\n```", parse_mode="MarkdownV2")

    except FileNotFoundError:
        bot.send_message(message.chat.id, "Файл fact_output не найден. Проверьте работу скрипта fact.py.")
    except subprocess.CalledProcessError:
        bot.send_message(message.chat.id, "Произошла ошибка при выполнении скрипта fact.py.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)