import telebot
import google.generativeai as genai
import time
import sys

# KEYS HERE, DO NOT TOUCH
TOKEN = '8576768180:AAEVylK96kRJgeesXBtcL0xUDd2-Gk54YZ4'
AI_KEY = 'AIzaSyAY4_hmshJr8gHvcZlmL9D_vvE_gbzJk20'

def start_bot():
    try:
        # AI SETTINGS: FORCE REST and v1 to remove 404
        genai.configure(api_key=AI_KEY, transport='rest')

        # Use gemini-1.5-flash
        model = genai.GenerativeModel('gemini-1.5-flash')

        bot = telebot.TeleBot(TOKEN)

        @bot.message_handler(func=lambda m: True)
        def handle(m):
            try:
                print(f"Incoming: {m.text}")
                res = model.generate_content(m.text)

                if res.text:
                    bot.reply_to(m, res.text)
                else:
                    bot.reply_to(m, "AI returned an empty response.")
            except Exception as e:
                err_msg = str(e)
                print(f"Runtime error: {err_msg}")
                if "429" in err_msg:
                    bot.reply_to(m, "❌ Too many requests. Wait.")
                elif "404" in err_msg:
                    bot.reply_to(m, "❌ 404: Google is messing with the models again.")
                else:
                    bot.reply_to(m, f"Error: {err_msg}")

        # Reset old connections (Fix 409)
        print("Cleaning old sessions...")
        bot.delete_webhook()
        time.sleep(2)

        print("--- BOT IS ONLINE. CHECK TELEGRAM ---")
        bot.infinity_polling(skip_pending=True, timeout=60)

    except Exception as e:
        err = str(e)
        if "409" in err:
            print("409 again. Wait 10 seconds...")
            time.sleep(10)
            return start_bot()
        else:
            print(f"Critical error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    start_bot()
