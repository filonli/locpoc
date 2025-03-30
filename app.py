import streamlit as st
import array

st.set_page_config(page_title="locpoc")

st.title("locpoc")
st.markdown("anonymous public messanger")

sta = st.session_state

if 'chat' not in st.session_state:
    sta.chat = []

name = st.text_input("write your name")

messages = st.container(height=300)
if prompt := st.chat_input("Say something"):
    msg = {}
    msg["name"] = name
    msg["text"] = prompt
    sta.chat.append(msg)

for m in sta.chat:
    
    messages.chat_message(m["name"]+":").write(m["name"]+": "+m["text"])