#Upto chat =model.start_chat() is model initializa
import google.generativeai as genai
import os
from libs.menu_loader import load_menu
from dotenv import load_dotenv

load_dotenv()
#Menu

CAKE_MENU = load_menu()


SYSTEM_INSTRUCTIONS =(f"You are a friendly assistant for homemade cake business based in Dubai and Sharjah. Your name is Habibi Cakes"
                      f"Here is the Cake Menu:\n{CAKE_MENU}\n\n"
                      "Help the customer through the following steps:\n"
                      "1. Greet customer and show the menu\n"
                      "2. Ask what cake they want and confirm that exists in the menu\n"
                      "3. Ask for their delivery location (Only Dubai and Sharjah)\n"
                      "4. Ask for preferred delivery time\n"
                      "5. Ask for the Occassion eg: Birthday, Anniversary etc.\n"
                      "6. Ask if they need special decoration like name or other requests\n"
                      "7. Once all ifo is collected, generate a clear and cheerful order summary:\n"
                      "Cake name\n - Price (AED)\n - Location\n - Delivery Location\n - Occassion\n - Decorations\n - Total\n"
                       "8. End by reminding them that payment is offline\n"
                        "Use emojis for making experience fun and friendly" )


#Setting up LLM

API_KEY = os.getenv("LLM_API_KEY")
genai.configure(api_key=API_KEY)

#Access gemini model
chat = None
model = genai.GenerativeModel("gemini-2.0-flash")
def start_session():
    global chat
    chat = model.start_chat() #This creates or initiates new chat session
    chat.send_message(SYSTEM_INSTRUCTIONS)
    print("LLM Config Completed")


def send_message_to_llm(message):
    res = chat.send_message(message)
    text = res.text
    return text

