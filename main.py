import telebot
import google.generativeai as genai
import os
import sys

# Получение ключей из переменных окружения Render
TOKEN = os.getenv('8576768180:AAGkqbo8V6XxsogC54W-dgIQG1JHdwSdqy0')
AI_KEY = os.getenv('AIzaSyDeoUa39KMZCLnaXITvUZTORBCAjbsZjms')

if not TOKEN or not AI_KEY:
    print("ОШИБКА: Проверь TELEGRAM_TOKEN и GEMINI_KEY в настройках Render!")
    sys.exit(1)

try:
    # Инициализация с актуальной моделью 2026 года
    genai.configure(api_key=AI_KEY)
    
    # Меняем 1.5-flash (404) на 2.0-flash
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    bot = telebot.TeleBot(TOKEN)
    
    @bot.message_handler(func=lambda m: True)
    def handle(m):
        try:
            print(f"Вход: {m.text}")
            res = model.generate_content(m.text)
            
            # Проверка, что ответ не пустой
            if res.text:
                bot.reply_to(m, res.text)
            else:
                bot.reply_to(m, "ИИ промолчал. Попробуй другой запрос.")
                
        except Exception as e:
            print(f"Ошибка при генерации: {e}")
            bot.reply_to(m, f"Ошибка API: Скорее всего, модель недоступна. {e}")

    print("--- БОТ ЗАПУЩЕН НА МОДЕЛИ 2.0-FLASH ---")
    bot.infinity_polling()

except Exception as e:
    print(f"Критическая ошибка запуска: {e}")
