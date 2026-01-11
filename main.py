import telebot
import google.generativeai as genai
import time
import sys

# ТВОИ КЛЮЧИ
TOKEN = '8576768180:AAEVylK96kRJgeesXBtcL0xUDd2-Gk54YZ4'
AI_KEY = 'AIzaSyAY4_hmshJr8gHvcZlmL9D_vvE_gbzJk20'

def start_bot():
    try:
        # ФИКС 404: Настраиваем транспорт на 'rest' в самом начале. 
        # Это заставляет библиотеку использовать стабильные пути v1.
        genai.configure(api_key=AI_KEY, transport='rest')
        
        # Используем модель gemini-1.5-flash
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        bot = telebot.TeleBot(TOKEN)

        @bot.message_handler(func=lambda m: True)
        def handle(m):
            try:
                print(f"Запрос ИИ: {m.text}")
                
                # Обычный вызов без лишних наворотов, так как транспорт уже настроен
                response = model.generate_content(m.text)
                
                if response.text:
                    bot.reply_to(m, response.text)
                else:
                    bot.reply_to(m, "ИИ не выдал текста.")
                    
            except Exception as e:
                err = str(e)
                print(f"Ошибка ИИ: {err}")
                bot.reply_to(m, f"Ошибка от Google: {err[:150]}")

        # Фикс конфликта 409
        print("Чистим сессии...")
        bot.delete_webhook()
        time.sleep(2) 
        
        print("--- БОТ В ЭФИРЕ ---")
        bot.infinity_polling(skip_pending=True)

    except Exception as e:
        if "409" in str(e):
            print("Конфликт 409. Ждем...")
            time.sleep(10)
            return start_bot()
        else:
            print(f"Критический сбой: {e}")
            sys.exit(1)

if __name__ == "__main__":
    start_bot()
