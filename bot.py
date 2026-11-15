import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            "🎁 Открыть GiftBoost",
            callback_data="open_game"
        )
    )

    bot.send_message(
        message.chat.id,
        "Добро пожаловать в GiftBoost! 🎮"
    )

bot.infinity_polling()
