import telebot
import google.generativeai as genai
import time
import sys

# KEYS INSERTED
TOKEN = '8576768180:AAEVylK96kRJgeesXBtcL0xUDd2-Gk54YZ4'
AI_KEY = 'AIzaSyAY4_hmshJr8gHvcZlmL9D_vvE_gbzJk20'

def start_bot():
    try:
        # FIX 404: Configure the client to avoid v1beta
        # In 2026, this is done via the transport='rest' parameter
        genai.configure(api_key=AI_KEY, transport='rest')
        
        # Use model 1.5-flash
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        bot = telebot.TeleBot(TOKEN)

        @bot.message_handler(func=lambda m: True)
        def handle(m):
            try:
                print(f"AI Request: {m.text}")
                
                # Normal call without extra arguments, since the version
                # is already fixed in genai.configure above
                response = model.generate_content(m.text)
                
                if response.text:
                    bot.reply_to(m, response.text)
                else:
                    bot.reply_to(m, "AI did not produce text.")
                    
            except Exception as e:
                err = str(e)
                print(f"AI Error: {err}")
                bot.reply_to(m, f"Error from Google: {err[:150]}")

        # Fix 409 conflict
        print("Clearing sessions...")
        bot.delete_webhook()
        time.sleep(2) 
        
        print("--- BOT IS LIVE ---")
        bot.infinity_polling(skip_pending=True)

    except Exception as e:
        if "409" in str(e):
            print("Conflict 409. Waiting...")
            time.sleep(10)
            return start_bot()
        else:
            print(f"Critical failure: {e}")
            sys.exit(1)

if __name__ == "__main__":
    start_bot()
