import telebot
from telebot import types
from load_config import load_config
import subprocess
import os
import time
import threading

# Загрузка конфигурации
config = load_config()
BOT_TOKEN = config.get("BOT_TOKEN")
USER_MAP = config.get("USER_MAP")

# Анимация спиннера
SPINNER = ["|", "/", "-", "\\"]

# Кнопки
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

btn_plan = types.KeyboardButton("🟡План")
btn_fact = types.KeyboardButton("✅Факт")
btn_all_inwork = types.KeyboardButton("Все задачи в работе")
btn_all_done_today = types.KeyboardButton("Все задачи выполненные сегодня")
btn_restart = types.KeyboardButton("Перезапуск бота")

markup.row(btn_plan, btn_fact)

markup.add(btn_all_inwork)
markup.add(btn_all_done_today)
markup.add(btn_restart)

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

# Функция для запуска скрипта all_inwork.py
def run_all_inwork_script(user_id):
    try:
        subprocess.run(["python", "all_inwork.py", user_id], check=True)
    except Exception as e:
        print(f"Ошибка при выполнении all_inwork.py: {e}")

# Функция для запуска скрипта all_done_today.py
def run_all_done_today_script(user_id):
    try:
        subprocess.run(["python", "all_done_today.py", user_id], check=True)
    except Exception as e:
        print(f"Ошибка при выполнении all_done_today.py: {e}")

# Функция для запуска скрипта fact.py
def run_fact_script(user_id):
    try:
        subprocess.run(["python", "fact.py", user_id], check=True)
    except Exception as e:
        print(f"Ошибка при выполнении fact.py: {e}")

# Функция для запуска скрипта plan.py
def run_plan_script(user_id):
    try:
        subprocess.run(["python", "plan.py", user_id], check=True)
    except Exception as e:
        print(f"Ошибка при выполнении plan.py: {e}")

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Привет! \n\n"
        "🟡*План* — все задачи в статусе 'в работе' для которых вы добавили комментарий за последние 24 часа \n\n"
        "✅*Факт* — все задачи в статусе 'в работе' и 'готово' для которых вы добавили комментарий за последние 24 часа \n\n"
        "*Все задачи в работе* — все задачи в работе \n\n"
        "*Все задачи выполненные сегодня* — выполненные задачи за сегодня \n\n"
        "*Перезапуск бота* — перезапуск бота",
        reply_markup=markup, parse_mode="Markdown"
    )

# Обработчик кнопки "Все задачи в работе"
@bot.message_handler(func=lambda message: message.text == "Все задачи в работе")
def handle_all_inwork_button(message):
    try:
        # Убираем клавиатуру
        loading_message = bot.send_message(message.chat.id, "⏳ Загружаю данные... |", reply_markup=types.ReplyKeyboardRemove())
        bot.delete_message(chat_id=message.chat.id, message_id=loading_message.message_id)

        # Получаем username пользователя из Telegram
        username = message.from_user.username
        if not username:
            bot.send_message(message.chat.id, "Ошибка: У вас не установлен username в Telegram.")
            return

        # Формируем ключ для поиска в USER_MAP
        user_key = f"@{username}"
        if user_key not in USER_MAP:
            bot.send_message(message.chat.id, f"Ошибка: Ваш username ({user_key}) не найден в базе данных.")
            return

        # Получаем USER_ID из USER_MAP
        current_user_id = USER_MAP[user_key]

        # Запускаем выполнение all_inwork.py в отдельном потоке
        thread = threading.Thread(target=run_all_inwork_script, args=(current_user_id,))
        thread.start()

        # Отправляем сообщение с начальной анимацией
        loading_message = bot.send_message(message.chat.id, "⏳ Загружаю данные... |")

        # Запускаем анимацию спиннера
        spinner_index = 0
        while thread.is_alive():
            spinner_index = (spinner_index + 1) % len(SPINNER)
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=loading_message.message_id,
                text=f"⏳ Загружаю данные... {SPINNER[spinner_index]}"
            )
            time.sleep(0.5)

        # Проверяем, завершился ли процесс
        if os.path.exists("all_inwork_output.txt"):
            with open("all_inwork_output.txt", "r", encoding="utf-8") as file:
                all_inwork_content = file.read()

        # Удаляем спиннер
        bot.delete_message(chat_id=message.chat.id, message_id=loading_message.message_id)

        # Отправка содержимого файла в формате monospace
        bot.send_message(message.chat.id, f"```\n{all_inwork_content}\n```", parse_mode="MarkdownV2", reply_markup=markup)
        subprocess.run(["rm", "all_inwork_output.txt"], check=True)

    except FileNotFoundError:
        bot.send_message(message.chat.id, "Файл all_inwork_output не найден. Проверьте работу скрипта all_inwork.py.")
    except subprocess.CalledProcessError:
        bot.send_message(message.chat.id, "Произошла ошибка при выполнении скрипта all_inwork.py.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

# Обработчик кнопки "Все задачи выполненные сегодня"
@bot.message_handler(func=lambda message: message.text == "Все задачи выполненные сегодня")
def handle_all_done_today_button(message):
    try:
        # Убираем клавиатуру
        loading_message = bot.send_message(message.chat.id, "⏳ Загружаю данные... |", reply_markup=types.ReplyKeyboardRemove())
        bot.delete_message(chat_id=message.chat.id, message_id=loading_message.message_id)

        # Получаем username пользователя из Telegram
        username = message.from_user.username
        if not username:
            bot.send_message(message.chat.id, "Ошибка: У вас не установлен username в Telegram.")
            return

        # Формируем ключ для поиска в USER_MAP
        user_key = f"@{username}"
        if user_key not in USER_MAP:
            bot.send_message(message.chat.id, f"Ошибка: Ваш username ({user_key}) не найден в базе данных.")
            return

        # Получаем USER_ID из USER_MAP
        current_user_id = USER_MAP[user_key]

        # Запускаем выполнение all_done_today.py в отдельном потоке
        thread = threading.Thread(target=run_all_done_today_script, args=(current_user_id,))
        thread.start()

        # Отправляем сообщение с начальной анимацией
        loading_message = bot.send_message(message.chat.id, "⏳ Загружаю данные... |")

        # Запускаем анимацию спиннера
        spinner_index = 0
        while thread.is_alive():
            spinner_index = (spinner_index + 1) % len(SPINNER)
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=loading_message.message_id,
                text=f"⏳ Загружаю данные... {SPINNER[spinner_index]}"
            )
            time.sleep(0.5)

        # Проверяем, завершился ли процесс
        if os.path.exists("all_done_today_output.txt"):
            with open("all_done_today_output.txt", "r", encoding="utf-8") as file:
                all_done_today_content = file.read()

        # Удаляем спиннер
        bot.delete_message(chat_id=message.chat.id, message_id=loading_message.message_id)

        # Отправка содержимого файла в формате monospace
        bot.send_message(message.chat.id, f"```\n{all_done_today_content}\n```", parse_mode="MarkdownV2", reply_markup=markup)
        subprocess.run(["rm", "all_done_today_output.txt"], check=True)

    except FileNotFoundError:
        bot.send_message(message.chat.id, "Файл all_done_today_output не найден. Проверьте работу скрипта all_done_today.py.")
    except subprocess.CalledProcessError:
        bot.send_message(message.chat.id, "Произошла ошибка при выполнении скрипта all_done_today.py.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

# Обработчик кнопки "✅Факт"
@bot.message_handler(func=lambda message: message.text == "✅Факт")
def handle_fact_button(message):
    try:
        # Убираем клавиатуру
        loading_message = bot.send_message(message.chat.id, "⏳ Загружаю данные... |", reply_markup=types.ReplyKeyboardRemove())
        bot.delete_message(chat_id=message.chat.id, message_id=loading_message.message_id)

        # Получаем username пользователя из Telegram
        username = message.from_user.username
        if not username:
            bot.send_message(message.chat.id, "Ошибка: У вас не установлен username в Telegram.")
            return

        # Формируем ключ для поиска в USER_MAP
        user_key = f"@{username}"
        if user_key not in USER_MAP:
            bot.send_message(message.chat.id, f"Ошибка: Ваш username ({user_key}) не найден в базе данных.")
            return

        # Получаем USER_ID из USER_MAP
        current_user_id = USER_MAP[user_key]

        # Запускаем выполнение all_done_today.py в отдельном потоке
        thread = threading.Thread(target=run_fact_script, args=(current_user_id,))
        thread.start()

        # Отправляем сообщение с начальной анимацией
        loading_message = bot.send_message(message.chat.id, "⏳ Загружаю данные... |")

        # Запускаем анимацию спиннера
        spinner_index = 0
        while thread.is_alive():
            spinner_index = (spinner_index + 1) % len(SPINNER)
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=loading_message.message_id,
                text=f"⏳ Загружаю данные... {SPINNER[spinner_index]}"
            )
            time.sleep(0.5)

        # Проверяем, завершился ли процесс
        if os.path.exists("fact_output.txt"):
            with open("fact_output.txt", "r", encoding="utf-8") as file:
                fact_content = file.read()

        # Удаляем спиннер
        bot.delete_message(chat_id=message.chat.id, message_id=loading_message.message_id)

        # Отправка содержимого файла в формате monospace
        bot.send_message(message.chat.id, f"```\n{fact_content}\n```", parse_mode="MarkdownV2", reply_markup=markup)
        subprocess.run(["rm", "fact_output.txt"], check=True)

    except FileNotFoundError:
        bot.send_message(message.chat.id, "Файл fact_output не найден. Проверьте работу скрипта fact.py.")
    except subprocess.CalledProcessError:
        bot.send_message(message.chat.id, "Произошла ошибка при выполнении скрипта fact.py.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")


# Обработчик кнопки "🟡План"
@bot.message_handler(func=lambda message: message.text == "🟡План")
def handle_plan_button(message):
    try:
        # Убираем клавиатуру
        loading_message = bot.send_message(message.chat.id, "⏳ Загружаю данные... |", reply_markup=types.ReplyKeyboardRemove())
        bot.delete_message(chat_id=message.chat.id, message_id=loading_message.message_id)

        # Получаем username пользователя из Telegram
        username = message.from_user.username
        if not username:
            bot.send_message(message.chat.id, "Ошибка: У вас не установлен username в Telegram.")
            return

        # Формируем ключ для поиска в USER_MAP
        user_key = f"@{username}"
        if user_key not in USER_MAP:
            bot.send_message(message.chat.id, f"Ошибка: Ваш username ({user_key}) не найден в базе данных.")
            return

        # Получаем USER_ID из USER_MAP
        current_user_id = USER_MAP[user_key]

        # Запускаем выполнение all_done_today.py в отдельном потоке
        thread = threading.Thread(target=run_plan_script, args=(current_user_id,))
        thread.start()

        # Отправляем сообщение с начальной анимацией
        loading_message = bot.send_message(message.chat.id, "⏳ Загружаю данные... |")

        # Запускаем анимацию спиннера
        spinner_index = 0
        while thread.is_alive():
            spinner_index = (spinner_index + 1) % len(SPINNER)
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=loading_message.message_id,
                text=f"⏳ Загружаю данные... {SPINNER[spinner_index]}"
            )
            time.sleep(0.5)

        # Проверяем, завершился ли процесс
        if os.path.exists("plan_output.txt"):
            with open("plan_output.txt", "r", encoding="utf-8") as file:
                plan_content = file.read()

        # Удаляем спиннер
        bot.delete_message(chat_id=message.chat.id, message_id=loading_message.message_id)

        # Отправка содержимого файла в формате monospace
        bot.send_message(message.chat.id, f"```\n{plan_content}\n```", parse_mode="MarkdownV2", reply_markup=markup)
        subprocess.run(["rm", "plan_output.txt"], check=True)

    except FileNotFoundError:
        bot.send_message(message.chat.id, "Файл plan_output не найден. Проверьте работу скрипта plan.py.")
    except subprocess.CalledProcessError:
        bot.send_message(message.chat.id, "Произошла ошибка при выполнении скрипта plan.py.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

# Обработчик кнопки "Перезапуск бота"
@bot.message_handler(func=lambda message: message.text == "Перезапуск бота")
def handle_restart_button(message):
    bot.send_message(message.chat.id, "Бот перезапущен!", reply_markup=markup)
    send_welcome(message)  # Вызываем обработчик команды /start

# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)