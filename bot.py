import telebot
import config
import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot(config.BOT_TOKEN)


def handle_update(update):
    bot.process_new_updates([telebot.types.Update.de_json(update)])
    return 'ok'


@bot.message_handler(commands=['start'])
def handle_start(message):
    # Кнопка "Поделиться номером"
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton(text="📱 Отправить номер телефона", request_contact=True)
    markup.add(button)

    bot.send_message(
        message.chat.id,
        "Пожалуйста, поделитесь своим номером телефона:",
        reply_markup=markup
    )


@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    phone = message.contact.phone_number

    # Приводим номер к формату +998...
    if not phone.startswith('+'):
        phone = '+' + phone

    try:
        response = requests.post(
            "https://online-shop.milliybiz.uz/auth/send-code/",
            json={"username": phone},
            timeout=5
        )

        print(response.json())

        if response.status_code == 200:
            data = response.json()
            code = data.get("code")

            if code:
                bot.send_message(message.chat.id, f"Ваш код подтверждения: {code}")
            else:
                bot.send_message(message.chat.id, "Код не получен. Попробуйте позже.")
        else:
            bot.send_message(message.chat.id, "Ошибка при получении кода.")
    except Exception:
        bot.send_message(message.chat.id, "Ошибка соединения с сервером.")


@bot.message_handler(content_types=['text'])
def block_manual_input(message):
    bot.send_message(
        message.chat.id,
        "❌ Ввод номера вручную отключён. Пожалуйста, нажмите кнопку «📱 Отправить номер телефона»."
    )
