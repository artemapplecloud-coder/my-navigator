import telebot
import google.generativeai as genai
import time
import sys

# Вставленные ключи
TOKEN = '8576768180:AAEVylK96kRJgeesXBtcL0xUDd2-Gk54YZ4'
AI_KEY = 'AIzaSyAY4_hmshJr8gHvcZlmL9D_vvE_gbzJk20'

def start_bot():
    try:
        # Настройка нейронки
        genai.configure(api_key=AI_KEY, transport='rest')
        # В 2026 году flash-latest — самая стабильная
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        bot = telebot.TeleBot(TOKEN)

        @bot.message_handler(func=lambda m: True)
        def handle(m):
            try:
                print(f"Принято: {m.text}")
                res = model.generate_content(m.text)
                
                if res.text:
                    bot.reply_to(m, res.text)
                else:
                    bot.reply_to(m, "Нейронка промолчала, попробуй еще раз.")
            except Exception as e:
                print(f"Ошибка нейронки: {e}")
                if "429" in str(e):
                    bot.reply_to(m, "У Google закончились бесплатные токены. Подожди немного.")
                else:
                    bot.reply_to(m, "Произошла ошибка при генерации ответа.")

        # Фикс ошибки 409: принудительно сбрасываем старые сессии
        print("Очистка старых сессий... Жди 5 секунд...")
        bot.delete_webhook()
        time.sleep(5) 
        
        print("--- БОТ ЗАПУЩЕН. СЕРВЕР В ТБИЛИСИ ---")
        # skip_pending=True игнорирует сообщения, присланные пока бот спал
        bot.infinity_polling(skip_pending=True, timeout=60)

    except Exception as e:
        err = str(e)
        if "409" in err:
            print("Конфликт 409: Старая копия бота еще жива. Ждем 15 секунд...")
            time.sleep(15)
            return start_bot()
        elif "401" in err:
            print("Ошибка 401: Проверь токен, Телеграм его не принимает.")
        else:
            print(f"Критический сбой: {e}")
            sys.exit(1)

if __name__ == "__main__":
    start_bot()
