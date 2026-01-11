import telebot
import requests
import time
import sys

# ТВОИ КЛЮЧИ (ВСТАВЛЕНЫ)
TOKEN = '8576768180:AAEVylK96kRJgeesXBtcL0xUDd2-Gk54YZ4'
AI_KEY = 'AIzaSyAY4_hmshJr8gHvcZlmL9D_vvE_gbzJk20'

bot = telebot.TeleBot(TOKEN)

def get_ai_response(text):
    # ПРИНУДИТЕЛЬНО используем стабильный адрес v1, где нет ошибки 404
    url = f"generativelanguage.googleapis.com{AI_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [
            {
                "parts": [{"text": text}]
            }
        ]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        res_json = response.json()
        
        # Вытаскиваем текст из ответа Google
        if 'candidates' in res_json:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            error_msg = res_json.get('error', {}).get('message', 'Неизвестная ошибка')
            return f"Ошибка Google: {error_msg}"
    except Exception as e:
        return f"Ошибка связи: {str(e)}"

@bot.message_handler(func=lambda m: True)
def handle_message(m):
    try:
        print(f"Запрос в ИИ: {m.text}")
        answer = get_ai_response(m.text)
        bot.reply_to(m, answer)
    except Exception as e:
        print(f"Ошибка бота: {e}")

def run_bot():
    try:
        print("Сброс старых сессий...")
        bot.delete_webhook()
        time.sleep(2)
        print("--- БОТ ЗАПУЩЕН ЧЕРЕЗ ПРЯМОЙ ДОСТУП V1 ---")
        bot.infinity_polling(skip_pending=True)
    except Exception as e:
        if "409" in str(e):
            print("Конфликт 409. Ждем...")
            time.sleep(10)
            run_bot()
        else:
            print(f"Сбой: {e}")

if __name__ == "__main__":
    run_bot()
