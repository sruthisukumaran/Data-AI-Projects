#This file is created to test whether google generative ai package is is working or not
import google.generativeai as genai

API_KEY = "AIzaSyCYt_I3Ib-5crAbCdEYzo5fC5OUzz73YxQ"

genai.configure(api_key=API_KEY)

#Access gemini model

model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat()
res = chat.send_message("What is the capital of India?")
print(res)
