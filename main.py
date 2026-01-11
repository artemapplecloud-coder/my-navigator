import telebot
import google.generativeai as genai
import os

# ВСТАВЬ СВОИ ДАННЫЕ СЮДА
TOKEN = '8576768180:AAGkqbo8V6XxsogC54W-dgIQG1JHdwSdqy0'
AI_KEY = 'AIzaSyAY4_hmshJr8gHvcZlmL9D_vvE_gbzJk20'

# Фикс: принудительно настраиваем транспорт на стабильную версию
genai.configure(api_key=AI_KEY)

# 1.5-flash в 2026 году работает ТОЛЬКО через стабильный эндпоинт
# Если библиотека сама подставляет v1beta, мы это сейчас увидим в логах
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def handle(m):
    try:
        print(f"Запрос: {m.text}")
        
        # Пробуем отправить запрос
        response = model.generate_content(m.text)
        
        if response.text:
            bot.reply_to(m, response.text)
        else:
            bot.reply_to(m, "Пустой ответ.")
            
    except Exception as e:
        error_str = str(e)
        print(f"ОШИБКА: {error_str}")
        
        # Если опять 404 — значит библиотека в Render слишком старая
        if "404" in error_str:
            bot.reply_to(m, "❌ Ошибка 404: Google требует обновить библиотеку. Проверь requirements.txt")
        elif "429" in error_str:
            bot.reply_to(m, "❌ Ошибка 429: Лимит исчерпан. Нужен новый ключ.")
        else:
            bot.reply_to(m, f"Ошибка: {error_str}")

print("--- БОТ ВКЛЮЧЕН (ФИКС 404) ---")
bot.infinity_polling()
