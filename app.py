import streamlit as st
import array
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
#@st.cache_data(ttl=600)
def run_query():
    return supabase.table("messages").select("*").execute()

rows = run_query()


st.set_page_config(page_title="locpoc")

st.title("locpoc")
st.markdown("anonymous public messanger")


name = st.text_input("write your name")

messages = st.container(height=300)
if prompt := st.chat_input("Say something"):
    d = {"sender":name,"message":prompt}
    supabase.table("messages").insert(d).execute()


for row in rows.data:
    
    messages.chat_message(row["sender"]+":").write(row["sender"]+": "+row["message"])