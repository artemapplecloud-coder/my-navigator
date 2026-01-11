import telebot
import google.generativeai as genai
from google.generativeai.types import RequestOptions
import time
import sys

# ТВОИ КЛЮЧИ
TOKEN = '8576768180:AAEVylK96kRJgeesXBtcL0xUDd2-Gk54YZ4'
AI_KEY = 'AIzaSyAY4_hmshJr8gHvcZlmL9D_vvE_gbzJk20'

def start_bot():
    try:
        # Настройка ключа
        genai.configure(api_key=AI_KEY)
        
        # ЖЕСТКИЙ ФИКС 404: Явно указываем версию v1 в настройках модели
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash'
        )
        
        bot = telebot.TeleBot(TOKEN)

        @bot.message_handler(func=lambda m: True)
        def handle(m):
            try:
                print(f"Запрос: {m.text}")
                
                # Принудительно отправляем запрос через стабильный API v1
                # Это убирает ошибку "models/gemini-1.5-flash is not found for API version v1beta"
                res = model.generate_content(
                    m.text,
                    request_options=RequestOptions(api_version='v1')
                )
                
                if res.text:
                    bot.reply_to(m, res.text)
                else:
                    bot.reply_to(m, "ИИ вернул пустой ответ.")
            except Exception as e:
                err = str(e)
                print(f"Ошибка ИИ: {err}")
                bot.reply_to(m, f"Ошибка API: {err[:150]}")

        # Фикс конфликта 409
        print("Сброс сессий...")
        bot.delete_webhook()
        time.sleep(2) 
        
        print("--- БОТ ЗАПУЩЕН (ПРИНУДИТЕЛЬНАЯ ВЕРСИЯ V1) ---")
        bot.infinity_polling(skip_pending=True)

    except Exception as e:
        if "409" in str(e):
            print("Конфликт 409. Перезапуск...")
            time.sleep(5)
            return start_bot()
        else:
            print(f"Критический сбой: {e}")
            sys.exit(1)

if __name__ == "__main__":
    start_bot()
