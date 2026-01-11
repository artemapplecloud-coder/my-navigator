import telebot
import google.generativeai as genai
import os
import time

# ВСТАВЬ СЮДА НОВЫЙ КЛЮЧ И ТОКЕН
TOKEN = '8576768180:AAGkqbo8V6XxsogC54W-dgIQG1JHdwSdqy0'
AI_KEY = 'AIzaSyBH6Sz4sqWwLhqGa1MC2GhuCg5UzuFKPZY'

genai.configure(api_key=AI_KEY)
bot = telebot.TeleBot(TOKEN)

# Список моделей для перебора
MODELS = ['gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-2.0-flash']

@bot.message_handler(func=lambda m: True)
def handle(m):
    success = False
    for model_name in MODELS:
        try:
            model = genai.GenerativeModel(model_name)
            res = model.generate_content(m.text)
            bot.reply_to(m, res.text)
            success = True
            break # Если получилось, выходим из цикла
        except Exception as e:
            print(f"Модель {model_name} не сработала: {e}")
            continue

    if not success:
        bot.reply_to(m, "❌ Все модели Google отказали. Твой ключ заблокирован (Лимит: 0). Создай НОВЫЙ ключ под VPN на другом аккаунте.")

print("Бот запущен. Если в Телеге тишина — смотри логи Render.")
bot.infinity_polling()
