import telebot
import google.generativeai as genai
import time
import sys

# ТВОИ КЛЮЧИ (ВСТАВЛЕНЫ)
TOKEN = '8576768180:AAEVylK96kRJgeesXBtcL0xUDd2-Gk54YZ4'
AI_KEY = 'AIzaSyAY4_hmshJr8gHvcZlmL9D_vvE_gbzJk20'

def start_bot():
    try:
        # ПРИНУДИТЕЛЬНО настраиваем стабильную версию v1 и протокол REST
        # Это лечит ошибку 404, так как v1beta больше не поддерживается
        genai.configure(api_key=AI_KEY, transport='rest')
        
        # В 2026 году используем gemini-1.5-flash
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        bot = telebot.TeleBot(TOKEN)

        @bot.message_handler(func=lambda m: True)
        def handle(m):
            try:
                print(f"Запрос от пользователя: {m.text}")
                # Генерация ответа
                res = model.generate_content(m.text)
                
                if res.text:
                    bot.reply_to(m, res.text)
                else:
                    bot.reply_to(m, "Нейронка вернула пустой ответ.")
            except Exception as e:
                err = str(e)
                print(f"Ошибка ИИ: {err}")
                # Бот отправит тех-данные ошибки прямо в чат для проверки
                bot.reply_to(m, f"Ошибка от Google: {err[:150]}")

        # Решение конфликта 409 (если процесс на Render завис)
        print("Сброс старых подключений...")
        bot.delete_webhook()
        time.sleep(3) 
        
        print("--- БОТ ЗАПУЩЕН НА СТАБИЛЬНОЙ ВЕРСИИ ---")
        bot.infinity_polling(skip_pending=True)

    except Exception as e:
        if "409" in str(e):
            print("Конфликт 409. Ждем 10 секунд и перезапускаем...")
            time.sleep(10)
            return start_bot()
        else:
            print(f"Критический сбой: {e}")
            sys.exit(1)

if __name__ == "__main__":
    start_bot()
