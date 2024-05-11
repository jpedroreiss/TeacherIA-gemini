import streamlit as st 
import google.generativeai as genai 
import google.ai.generativelanguage as glm 
from dotenv import load_dotenv
import os 
from model import *

load_dotenv()

#API-KEY
API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

#MODELO e CONFIG DA API
def setup_model():
    return genai.GenerativeModel(
        model_name=MODEL_NAME,
        generation_config=GENERATION_CONFIG,
        safety_settings=SAFETY_SETTINGS,
        system_instruction=SYSTEM_INSTRUCTION,
    )

#StreamLit
def load_streamlit_header():
    st.set_page_config(
        page_title="TeacherIA",
        page_icon="👨‍🏫",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    st.markdown('### Olá, sou o TeacherIA, ensino e aplico provas para você sempre que quiser! 👨‍🏫')
    st.divider()


#Role
def role_to_streamlit(role):
  if role == "model":
    return "assistant"
  else:
    return role

model = setup_model()

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=HISTORY)


load_streamlit_header()

for message in st.session_state.chat.history:
    with st.chat_message(role_to_streamlit(message.role)):
        st.markdown(message.parts[0].text)

if prompt := st.chat_input("Qual assunto você quer estudar agora?"):
    st.chat_message("user").markdown(prompt)
    
    response = st.session_state.chat.send_message(prompt) 
    
    with st.chat_message("assistant"):
        st.markdown(response.text)



