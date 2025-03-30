import streamlit as st
import array
import time
from supabase import create_client, Client,create_async_client
import datetime
import asyncio

st.set_page_config(page_title="locpoc")
# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    url = st.secrets["SUP_URL"]
    key = st.secrets["SUP_KEY"]
    return create_client(url, key)


supabase:Client = init_connection()

#with st.sidebar:
st.title("locpoc")
st.caption("anonymous public messager")

messages = st.container(height=500)

def draw_msgs():
    rows = supabase.table("messages").select("*").order("created_at").execute()

    last_n = ""
    for row in rows.data:
        c = messages.columns(2)
        #msg_c.chat_message(row["sender"]+":")
        
        if row["sender"] != last_n:
            
            if row["sender"] == "":
                c[0].badge("[unnamed]: ")
            else:
                c[0].badge(row["sender"]+": ")
                
        
        c[1].write(row["message"])
        last_n = row["sender"]

def write_msg():
    name = st.text_input("nickname",placeholder ="write your name")
    if prompt := st.chat_input("Say something"):
        d = {"sender":name,"message":prompt}
        supabase.table("messages").insert(d).execute()
    
if st.button("update"):
    st.rerun()

