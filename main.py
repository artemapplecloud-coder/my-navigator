import telebot
import google.generativeai as genai
import time
import sys

# ТВОИ КЛЮЧИ ВСТАВЛЕНЫ
TOKEN = '8576768180:AAEVylK96kRJgeesXBtcL0xUDd2-Gk54YZ4'
AI_KEY = 'AIzaSyAY4_hmshJr8gHvcZlmL9D_vvE_gbzJk20'

def start_bot():
    try:
        # Настройка: принудительно стабильный протокол REST
        genai.configure(api_key=AI_KEY, transport='rest')
        
        # Пробуем модель gemini-1.5-flash (самая базовая)
        # Если будет 404, бот пришлет список рабочих имен в логи Render
        current_model = 'gemini-1.5-flash'
        model = genai.GenerativeModel(current_model)
        
        bot = telebot.TeleBot(TOKEN)

        @bot.message_handler(func=lambda m: True)
        def handle(m):
            try:
                print(f"Входящий текст: {m.text}")
                res = model.generate_content(m.text)
                bot.reply_to(m, res.text)
            except Exception as e:
                err_msg = str(e)
                print(f"Ошибка генерации: {err_msg}")
                # Выводим реальную ошибку в Telegram
                bot.reply_to(m, f"Ошибка {current_model}: {err_msg[:100]}")

        # АВТОПОИСК РАБОЧИХ МОДЕЛЕЙ (выведет список в консоль Render)
        print("--- ИЩЕМ ДОСТУПНЫЕ МОДЕЛИ ДЛЯ ТВОЕГО КЛЮЧА ---")
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    print(f"РАБОЧАЯ МОДЕЛЬ НАЙДЕНА: {m.name}")
        except Exception as e:
            print(f"Не удалось получить список: {e}")

        # Фикс 409: сброс старых подключений
        bot.delete_webhook()
        time.sleep(2)
        print(f"--- БОТ ВКЛЮЧЕН (МОДЕЛЬ {current_model}) ---")
        bot.infinity_polling(skip_pending=True)

    except Exception as e:
        if "409" in str(e):
            print("Конфликт 409. Ждем 10 секунд...")
            time.sleep(10)
            return start_bot()
        else:
            print(f"Критический сбой: {e}")
            sys.exit(1)

if __name__ == "__main__":
    start_bot()
