import streamlit as st
import asyncio
from supabase import create_async_client, Client

st.set_page_config(page_title="locpoc")

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    url = st.secrets["SUP_URL"]
    key = st.secrets["SUP_KEY"]
    return create_async_client(url, key)

supabase: Client = init_connection()

async def subscribe_to_changes():
    """Subscribes to changes in the Supabase table and updates Streamlit."""

    try:
        realtime_client = supabase.realtime.channel(f"realtime:messages")

        def handle_event(event):
            st.experimental_rerun()

        realtime_client.on("UPDATE", handle_event).on("INSERT", handle_event).on("DELETE", handle_event).subscribe()

        while True:
            await asyncio.sleep(0.2)

    except Exception as e:
        st.error(f"Error subscribing to changes: {e}")


st.title("locpoc")
st.caption("anonymous public messanger")

messages = st.container(height=500)

async def draw_msgs():
    try:
        rows = await supabase.table("messages").select("*").order("created_at").execute()

        last_n = ""
        if rows.data:
            for row in rows.data:
                c = messages.columns(2)
                if row["sender"] != last_n:
                    if row["sender"] == "":
                        c[0].badge("[unnamed]: ")
                    else:
                        c[0].badge(row["sender"] + ": ")
                c[1].write(row["message"])
                last_n = row["sender"]
        else:
            st.write("No messages found.")
    except Exception as e:
        st.error(f"Error drawing messages: {e}")

def write_msg():
    name = st.text_input("nickname", placeholder="write your name")
    if prompt := st.chat_input("Say something"):
        d = {"sender": name, "message": prompt}
        asyncio.create_task(supabase.table("messages").insert(d).execute())
        st.experimental_rerun()

async def main():
    asyncio.create_task(subscribe_to_changes())
    await draw_msgs()
    write_msg()

if __name__ == "__main__":
    asyncio.run(main())