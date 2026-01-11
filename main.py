import telebot
import google.generativeai as genai
from google.generativeai.types import RequestOptions
import time
import sys

# ==========================================
# КЛЮЧИ (УЖЕ ВСТАВЛЕНЫ)
# ==========================================
TOKEN = '8576768180:AAEVylK96kRJgeesXBtcL0xUDd2-Gk54YZ4'
AI_KEY = 'AIzaSyAY4_hmshJr8gHvcZlmL9D_vvE_gbzJk20'
# ==========================================

def start_bot():
    try:
        # Настройка Google AI
        genai.configure(api_key=AI_KEY)
        
        # Фикс 404: Используем модель через стабильный эндпоинт v1
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        bot = telebot.TeleBot(TOKEN)

        @bot.message_handler(func=lambda m: True)
        def handle(m):
            try:
                print(f"Принято: {m.text}")
                
                # ЖЕСТКИЙ ФИКС 404: Явно указываем api_version='v1'
                # Это запрещает библиотеке использовать v1beta, которая больше не работает
                response = model.generate_content(
                    m.text,
                    request_options=RequestOptions(api_version='v1')
                )
                
                if response.text:
                    bot.reply_to(m, response.text)
                else:
                    bot.reply_to(m, "ИИ прислал пустой ответ.")
                    
            except Exception as e:
                err = str(e)
                print(f"Ошибка при генерации: {err}")
                bot.reply_to(m, f"Ошибка от Google: {err[:150]}")

        # Фикс 409: Удаляем старые вебхуки и сессии
        print("Сброс старых подключений...")
        bot.delete_webhook()
        time.sleep(2) 
        
        print("--- БОТ ЗАПУЩЕН (ВЕРСИЯ V1) ---")
        # skip_pending=True игнорирует сообщения, присланные пока бот был оффлайн
        bot.infinity_polling(skip_pending=True)

    except Exception as e:
        if "409" in str(e):
            print("Конфликт 409: Бот еще запущен где-то. Ждем 10 сек...")
            time.sleep(10)
            return start_bot()
        else:
            print(f"Критический сбой запуска: {e}")
            sys.exit(1)

if __name__ == "__main__":
    start_bot()
