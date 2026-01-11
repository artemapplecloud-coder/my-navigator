import telebot
import requests
import time
import sys

# ТВОИ КЛЮЧИ
TOKEN = '8576768180:AAEVylK96kRJgeesXBtcL0xUDd2-Gk54YZ4'
AI_KEY = 'AIzaSyAY4_hmshJr8gHvcZlmL9D_vvE_gbzJk20'

bot = telebot.TeleBot(TOKEN)

def get_ai_response(text):
    # МАКСИМАЛЬНО ТУПОЙ И ПРЯМОЙ URL
    base_url = "generativelanguage.googleapis.com"
    full_url = base_url + "?key=" + AI_KEY
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [
            {
                "parts": [{"text": text}]
            }
        ]
    }

    try:
        response = requests.post(full_url, json=payload, headers=headers)
        res_json = response.json()
        
        # Жесткая проверка структуры ответа (с индексами [0])
        if 'candidates' in res_json and len(res_json['candidates']) > 0:
            candidate = res_json['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content']:
                return candidate['content']['parts'][0]['text']
        
        # Если что-то не так, выводим ошибку от самого Google
        error_msg = res_json.get('error', {}).get('message', 'Неизвестная ошибка API')
        return "Ошибка от Google: " + str(error_msg)
        
    except Exception as e:
        return "Ошибка связи: " + str(e)

@bot.message_handler(func=lambda m: True)
def handle_message(m):
    try:
        print("Запрос: " + str(m.text))
        answer = get_ai_response(m.text)
        bot.reply_to(m, answer)
    except Exception as e:
        print("Ошибка бота: " + str(e))

def run_bot():
    try:
        print("Сброс сессий...")
        bot.delete_webhook()
        time.sleep(2)
        print("--- БОТ ЗАПУЩЕН (ФИНАЛЬНЫЙ ФИКС URL) ---")
        bot.infinity_polling(skip_pending=True)
    except Exception as e:
        if "409" in str(e):
            time.sleep(10)
            run_bot()
        else:
            print("Сбой: " + str(e))

if __name__ == "__main__":
    run_bot()
