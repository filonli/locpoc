import streamlit as st
import array
from supabase import create_client, Client
import datetime

sup:Client = create_client(st.secrets["SUP_URL"],st.secrets["SUP_KEY"])


def insert_message(sender, message):
    """Inserts a message into the Supabase database."""
    data, count = sup.table("messages").insert({"sender": sender, "message": message}).execute()
    return data, count

def fetch_messages():
    """Fetches all messages from the Supabase database."""
    data, count = sup.table("messages").select("*").order("timestamp").execute()
    return data, count


st.set_page_config(page_title="locpoc")

st.title("locpoc")
st.markdown("anonymous public messanger")


name = st.text_input("write your name")

messages = st.container(height=300)
if prompt := st.chat_input("Say something"):
    insert_message(name,prompt)

 # Fetch and display messages
data, count = fetch_messages()
if data and data.data:
    for message_data in data.data:
        timestamp = datetime.datetime.fromisoformat(message_data["timestamp"].replace('Z', '+00:00'))
        st.write(f"**{message_data['sender']}** ({timestamp.strftime('%Y-%m-%d %H:%M:%S')}): {message_data['message']}")
else:
    st.write("No messages yet.")

for m in sta.chat:
    
    messages.chat_message(m["name"]+":").write(m["name"]+": "+m["text"])