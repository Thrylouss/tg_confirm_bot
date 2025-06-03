# bot.py — основная логика Telegram-бота

import telebot
import config
import requests

bot = telebot.TeleBot(config.BOT_TOKEN)


def handle_update(update):
    bot.process_new_updates([telebot.types.Update.de_json(update)])
    return 'ok'


@bot.message_handler(content_types=['text'])
def handle_message(message):
    phone = message.text.strip()

    # Простая проверка на номер
    if not phone.startswith('+') or not phone[1:].isdigit():
        bot.send_message(message.chat.id, "Пожалуйста, введите номер в формате +998901234567")
        return

    try:
        # Запрос на твой backend
        response = requests.post(
            "https://online-shop.milliybiz.uz/auth/send-code/",
            json={"username": phone},
            timeout=5
        )

        if response.status_code == 200:
            data = response.json()
            code = data.get("code")

            if code:
                bot.send_message(message.chat.id, f"Ваш код подтверждения: {code}")
            else:
                bot.send_message(message.chat.id, "Код не получен. Попробуйте позже.")
        else:
            bot.send_message(message.chat.id, "Ошибка при получении кода.")
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка соединения с сервером.")
