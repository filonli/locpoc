import streamlit as st
import array
import time
from supabase import create_client, Client
import datetime

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    url = st.secrets["SUP_URL"]
    key = st.secrets["SUP_KEY"]
    return create_client(url, key)


supabase:Client = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
#@st.cache_вфеф(ttl=20)
def run_query():
    return supabase.table("messages").select("*").order("created_at").execute()

rows = run_query()


st.set_page_config(page_title="locpoc")



with st.sidebar:
    st.title("locpoc")
    st.caption("anonymous public messanger")
    
    
    name = st.text_input("write your name")

    refresh_time = st.select_slider(
        "Refresh rate",
        options=[
            0.5,
            1,
            2,
            5
        ],
    )

messages = st.container()

for row in rows.data:
    
    messages.chat_message(row["sender"]+":").caption(row["sender"]+": ").write(row["message"])


if prompt := st.chat_input("Say something"):
    d = {"sender":name,"message":prompt}
    supabase.table("messages").insert(d).execute()
    messages.chat_message('human').caption(name).write(prompt)

    




time.sleep(refresh_time)
st.rerun()