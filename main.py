import telebot
import google.generativeai as genai
import os

# ТВОИ ДАННЫЕ
TOKEN = '8576768180:AAGkqbo8V6XxsogC54W-dgIQG1JHdwSdqy0'
AI_KEY = 'AIzaSyAY4_hmshJr8gHvcZlmL9D_vvE_gbzJk20'

# Настройка: транспорт 'rest' — это лекарство от 404 на облачных хостингах
genai.configure(api_key=AI_KEY, transport='rest')

# В 2026 году пробуем версию 'flash-latest'
model = genai.GenerativeModel('gemini-1.5-flash-latest')

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def handle(m):
    try:
        print(f"Принято сообщение: {m.text}")
        res = model.generate_content(m.text)
        
        if res.text:
            bot.reply_to(m, res.text)
        else:
            bot.reply_to(m, "ИИ вернул пустой ответ.")
            
    except Exception as e:
        error_msg = str(e)
        print(f"ЛОГ ОШИБКИ: {error_msg}")
        
        if "404" in error_msg:
            # Если опять 404, выводим список доступных моделей прямо в консоль Render
            print("--- ДОСТУПНЫЕ ТЕБЕ МОДЕЛИ: ---")
            try:
                for m_info in genai.list_models():
                    print(m_info.name)
            except:
                print("Не удалось получить список моделей.")
            
            bot.reply_to(m, "❌ Ошибка 404. Я вывел список доступных моделей в логи Render. Посмотри их там.")
        else:
            bot.reply_to(m, f"Проблема: {error_msg}")

print("--- БОТ ВКЛЮЧЕН. ЕСЛИ БУДЕТ 404 — СМОТРИ ЛОГИ RENDER ---")
bot.infinity_polling()
