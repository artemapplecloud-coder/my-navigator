import telebot
import google.generativeai as genai
import sys

# ==========================================
# ВСТАВЬ СВОИ ДАННЫЕ СЮДА:
# ==========================================
TOKEN = '8576768180:AAEVylK96kRJgeesXBtcL0xUDd2-Gk54YZ4'
AI_KEY = 'AIzaSyAY4_hmshJr8gHvcZlmL9D_vvE_gbzJk20'
# ==========================================

# Простая проверка, чтобы ты не забыл вставить ключи
if 'ТВОЙ_' in TOKEN or 'ТВОЙ_' in AI_KEY:
    print("КРИТИЧЕСКАЯ ОШИБКА: Ты не заменил шаблонные ключи на свои реальные данные!")
    sys.exit(1)

try:
    # Настройка Google Gemini (фикс 404 через transport='rest')
    genai.configure(api_key=AI_KEY, transport='rest')
    # Самая стабильная модель на начало 2026 года
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    # Инициализация бота
    bot = telebot.TeleBot(TOKEN)

    # Обработчик всех текстовых сообщений
    @bot.message_handler(func=lambda m: True)
    def handle_message(m):
        try:
            print(f"Принял запрос: {m.text}")
            
            # Генерация ответа через ИИ
            response = model.generate_content(m.text)
            
            if response and response.text:
                bot.reply_to(m, response.text)
            else:
                bot.reply_to(m, "ИИ не смог сформировать текст ответа.")
                
        except Exception as e:
            error_str = str(e)
            print(f"Ошибка при обработке: {error_str}")
            
            if "429" in error_str:
                bot.reply_to(m, "❌ Ошибка квот: у Google закончились бесплатные запросы. Попробуй позже.")
            elif "401" in error_str:
                bot.reply_to(m, "❌ Ошибка авторизации: проверь токен Телеграм!")
            else:
                bot.reply_to(m, f"Произошла ошибка: {error_str}")

    # Фикс ошибки 409: удаляем старые соединения и пропускаем накопившиеся сообщения
    print("--- БОТ ЗАПУСКАЕТСЯ... ---")
    bot.remove_webhook()
    
    # skip_pending=True игнорирует сообщения, присланные пока бот был выключен
    print("--- СИСТЕМА В ЭФИРЕ ---")
    bot.infinity_polling(skip_pending=True)

except Exception as e:
    print(f"Критический сбой при старте: {e}")
