import telebot
import google.generativeai as genai
import os
import sys

# Получение ключей из настроек Render
TOKEN = os.getenv('TELEGRAM_TOKEN')
AI_KEY = os.getenv('GEMINI_KEY')

if not TOKEN or not AI_KEY:
    print("КРИТИЧЕСКАЯ ОШИБКА: Ключи не найдены!")
    sys.exit(1)

try:
    # Явно указываем версию v1 в конфигурации (фикс для 2026 года)
    genai.configure(api_key=AI_KEY)
    
    # Используем стабильный идентификатор модели
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
    
    bot = telebot.TeleBot(TOKEN)
    
    @bot.message_handler(func=lambda m: True)
    def handle(m):
        try:
            print(f"Получено: {m.text}")
            # Прямой вызов генерации
            res = model.generate_content(m.text)
            bot.reply_to(m, res.text)
        except Exception as e:
            print(f"Ошибка API: {e}")
            bot.reply_to(m, f"Проблема с частотой: {e}")

    print("--- НАВИГАТОР В ЭФИРЕ. ЧАСТОТА 52 ГЦ СТАБИЛЬНА ---")
    bot.infinity_polling()

except Exception as e:
    print(f"Критический сбой: {e}")
