import telebot
import google.generativeai as genai
import os
import sys

# ВСТАВЬ СВОИ ДАННЫЕ СЮДА
TOKEN = '8576768180:AAGkqbo8V6XxsogC54W-dgIQG1JHdwSdqy0'
AI_KEY = 'AIzaSyAY4_hmshJr8gHvcZlmL9D_vvE_gbzJk20'

try:
    genai.configure(api_key=AI_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    bot = telebot.TeleBot(TOKEN)

    @bot.message_handler(func=lambda m: True)
    def handle(m):
        try:
            print(f"Принято: {m.text}")
            res = model.generate_content(m.text)
            
            if res.text:
                bot.reply_to(m, res.text)
            else:
                bot.reply_to(m, "ИИ ничего не ответил.")
        except Exception as e:
            print(f"Ошибка в handle: {e}")
            if "429" in str(e):
                bot.reply_to(m, "❌ Ошибка 429: Лимит всё еще 0. Google блокирует запросы от Render.")
            else:
                bot.reply_to(m, f"Ошибка: {e}")

    print("--- БОТ ЗАПУЩЕН И ЖДЕТ СООБЩЕНИЙ ---")
    bot.infinity_polling()

except Exception as e:
    print(f"Ошибка запуска: {e}")
