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
    return create_async_client(url, key)


supabase:Client = init_connection()



async def subscribe_to_changes():
    """Subscribes to changes in the Supabase table and updates Streamlit."""

    try:
        # Correct way to subscribe to changes using the RealtimeClient
        realtime_client = supabase.realtime.channel(f"realtime:{"messages"}")

        def handle_event(event):
            st.experimental_rerun()

        realtime_client.on("UPDATE", handle_event).on("INSERT", handle_event).on("DELETE", handle_event).subscribe()

        while True:
            await asyncio.sleep(0.2)

    except Exception as e:
        st.error(f"Error subscribing to changes: {e}")




#with st.sidebar:
st.title("locpoc")
st.caption("anonymous public messanger")

messages = st.container(height=500)

async def draw_msgs():
    rows = await supabase.table("messages").select("*").order("created_at").execute()

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
    


async def main():
    await draw_msgs()
    await subscribe_to_changes()

    write_msg()

if __name__ == "__main__":
    asyncio.run(main())