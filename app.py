import streamlit as st
import array
import time
from supabase import create_client, Client
import datetime
import asyncio

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

async def subscribe_to_changes():
    """Subscribes to changes in the Supabase table and updates Streamlit."""

    try:
        def handle_event(event):
            st.rerun()

        supabase.table("messages").on("*", handle_event).subscribe()

        while True:
            await asyncio.sleep(0.2)

    except Exception as e:
        st.error(f"Error subscribing to changes: {e}")

asyncio.create_task(subscribe_to_changes())

st.set_page_config(page_title="locpoc")



#with st.sidebar:
st.title("locpoc")
st.caption("anonymous public messanger")




    #refresh_time = st.select_slider(
    #    "Refresh rate",
    #    options=[
    #        0.5,
    #        1,
    #        2,
    #        5
    #    ],
    #)

messages = st.container(height=500)

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

name = st.text_input("nickname",placeholder ="write your name")
if prompt := st.chat_input("Say something"):
    d = {"sender":name,"message":prompt}
    supabase.table("messages").insert(d).execute()
    

    #c = messages.columns(2)
    #msg_c.chat_message('human')
    #c[0].caption(name)
    #c[1].write(prompt)

    




#time.sleep(refresh_time)
#st.rerun()