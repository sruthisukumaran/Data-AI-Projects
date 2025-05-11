import streamlit as st
from libs.llm_utils import send_message_to_llm, start_session
from libs.menu_loader import load_menu

#Menu 
CAKE_MENU = load_menu()

#UI
st.title("Home Bakery AI Assistant")
st.markdown("Serving Dubai & Sharjah | Home made Cakes | Cash on Delivery")

if "messages" not in st.session_state:
    start_session()
    welcome_message = ("Hi there,"
    "Welcome to Habibi Cakes\n\n"
    "Here is our Menu\n"+ CAKE_MENU + "\n\n"
    "Would you like to order today?")
    st.session_state.messages = [{"role":"ai", "content": welcome_message}]

user_input = st.chat_input("Enter your message..")

if user_input:
    #Adding user message to chat memmory
    st.session_state.messages.append({
        "role" : "user",
        "content" : user_input
     })
    #Storing llm response to chat history
    llm_resp = send_message_to_llm(user_input)
    st.session_state.messages.append({
        "role" : "ai",
        "content" : llm_resp
     })
    


#Below will the structure of messages in session.state
# [{
#     "role":"user",
#     "message":"What is the capotal of India"
# },
# {
#     "role":"assistant",
#     "message":"New Delhi"
# }
# ]
#Print messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

