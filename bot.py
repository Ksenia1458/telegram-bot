import telebot
from telebot import types
import random
from datetime import datetime

# Вставь свой токен сюда
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Список мотивирующих фраз
quotes = [
    "Маленькие шаги каждый день приводят к большим результатам.",
    "Ты справишься. Просто начни.",
    "Дисциплина побеждает мотивацию.",
    "Каждый эксперт когда-то был новичком.",
    "Лучшее время начать — сейчас."
]

# Хранилище заметок (пока в памяти)
notes = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Время")
    btn2 = types.KeyboardButton("Мотивация")
    btn3 = types.KeyboardButton("Добавить заметку")
    btn4 = types.KeyboardButton("Мои заметки")
    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name}!\n\nЯ бот-помощник для учёбы и продуктивности.\nВыбери действие на клавиатуре или используй команды.",
        reply_markup=markup
    )

@bot.message_handler(commands=['time'])
@bot.message_handler(func=lambda message: message.text == "Время")
def current_time(message):
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    bot.send_message(message.chat.id, f"Сейчас: {now}")

@bot.message_handler(commands=['quote'])
@bot.message_handler(func=lambda message: message.text == "Мотивация")
def motivation(message):
    bot.send_message(message.chat.id, random.choice(quotes))

@bot.message_handler(commands=['add'])
@bot.message_handler(func=lambda message: message.text == "Добавить заметку")
def add_note(message):
    msg = bot.send_message(message.chat.id, "Напиши заметку, которую хочешь сохранить:")
    bot.register_next_step_handler(msg, save_note)

def save_note(message):
    user_id = message.from_user.id
    if user_id not in notes:
        notes[user_id] = []
    notes[user_id].append(message.text)
    bot.send_message(message.chat.id, "Заметка сохранена!")

@bot.message_handler(commands=['notes'])
@bot.message_handler(func=lambda message: message.text == "Мои заметки")
def show_notes(message):
    user_id = message.from_user.id
    if user_id in notes and notes[user_id]:
        text = "Твои заметки:\n\n"
        for i, note in enumerate(notes[user_id], 1):
            text += f"{i}. {note}\n"
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, "У тебя пока нет заметок.")

@bot.message_handler(func=lambda message: True)
def other(message):
    bot.send_message(message.chat.id, "Я не понял команду. Используй кнопки или /start")

print("Бот запущен...")
bot.infinity_polling()