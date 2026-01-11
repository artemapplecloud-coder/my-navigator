import telebot
import requests
import time

# --- НАСТРОЙКИ ---
TOKEN = '8576768180:AAEVylK96kRJgeesXBtcL0xUDd2-Gk54YZ4'
AI_KEY = 'AIzaSyAY4_hmshJr8gHvcZlmL9D_vvE_gbzJk20'

# Используем актуальную модель Gemini 1.5 Flash (быстрая и эффективная)
API_URL = f"generativelanguage.googleapis.com{AI_KEY}"

bot = telebot.TeleBot(TOKEN)

def get_ai_response(text):
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [
            {
                "parts": [{"text": text}]
            }
        ]
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        res_json = response.json()
        
        # Глубокая проверка структуры ответа Google
        if 'candidates' in res_json and len(res_json['candidates']) > 0:
            candidate = res_json['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content'] and len(candidate['content']['parts']) > 0:
                return candidate['content']['parts'][0]['text']
        
        # Вывод ошибки, если API что-то не нравится (например, ключ или лимиты)
        if 'error' in res_json:
            return f"Ошибка API: {res_json['error'].get('message')}"
        
        return "Google прислал пустой ответ или структуру, которую я не узнаю."
        
    except Exception as e:
        return f"Ошибка связи (Network Error): {str(e)}"

@bot.message_handler(func=lambda m: True)
def handle_message(m):
    try:
        print(f"--- НОВЫЙ ЗАПРОС ---")
        print(f"От пользователя: {m.text}")
        
        # Отправляем визуальный статус "печатает", чтобы юзер не скучал
        bot.send_chat_action(m.chat.id, 'typing')
        
        answer = get_ai_response(m.text)
        bot.reply_to(m, answer)
        
        print(f"Ответ отправлен.")
    except Exception as e:
        print(f"Ошибка в обработчике: {e}")

def run_bot():
    while True:
        try:
            print("Сброс вебхуков и запуск...")
            bot.delete_webhook()
            time.sleep(1)
            print("--- БОТ 'PROTOCOL RESONANCE' ЗАПУЩЕН ---")
            bot.infinity_polling(skip_pending=True, timeout=60)
        except Exception as e:
            print(f"Критический сбой цикла: {e}")
            time.sleep(5) # Пауза перед перезапуском при вылете интернета

if __name__ == "__main__":
    run_bot()
