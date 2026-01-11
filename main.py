import telebot
import google.generativeai as genai
import time
import sys

# ТВОИ КЛЮЧИ ВСТАВЛЕНЫ
TOKEN = '8576768180:AAEVylK96kRJgeesXBtcL0xUDd2-Gk54YZ4'
AI_KEY = 'AIzaSyAY4_hmshJr8gHvcZlmL9D_vvE_gbzJk20'

def start_bot():
    try:
        # Настройка Google AI: принудительно REST и стабильная версия v1
        genai.configure(api_key=AI_KEY, transport='rest')
        
        # Попробуем gemini-1.5-pro, она стабильнее в 2026 году
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        bot = telebot.TeleBot(TOKEN)

        @bot.message_handler(func=lambda m: True)
        def handle(m):
            try:
                print(f"Запрос от пользователя: {m.text}")
                res = model.generate_content(m.text)
                
                if res.text:
                    bot.reply_to(m, res.text)
                else:
                    bot.reply_to(m, "ИИ прислал пустой ответ.")
            except Exception as e:
                # ВЫВОДИМ РЕАЛЬНУЮ ОШИБКУ В ТЕЛЕГУ ДЛЯ ДИАГНОСТИКИ
                error_text = str(e)
                print(f"Ошибка ИИ: {error_text}")
                bot.reply_to(m, f"Ошибка от Google: {error_text[:200]}") # первые 200 символов ошибки

        # Фикс 409: Очистка старых сессий
        print("Удаляем старые подключения...")
        bot.delete_webhook()
        time.sleep(3) 
        
        print("--- БОТ ЗАПУЩЕН И ГОТОВ К ТЕСТУ ---")
        bot.infinity_polling(skip_pending=True)

    except Exception as e:
        err = str(e)
        if "409" in err:
            print("Конфликт 409. Ждем 10 секунд...")
            time.sleep(10)
            return start_bot()
        else:
            print(f"Критический сбой: {e}")
            sys.exit(1)

if __name__ == "__main__":
    start_bot()
