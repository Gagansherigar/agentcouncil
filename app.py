import streamlit as st
import asyncio
from debate import teamconfig, debate

st.title("Agent Council")

topic = st.text_input("Enter a topic of the debate", "Should India Buy Russian Oil?")
clicked = st.button("Start", type="primary")

chat = st.container()

async def run_debate():
    team = await teamconfig(topic)

    with chat:
        async for message in debate(team):
            if message.startswith("Host"):
                with st.chat_message(name="Host", avatar="🥸"):
                    st.write(message)

            elif message.startswith("Narendra"):
                with st.chat_message(name="Narendra", avatar="🫡"):
                    st.write(message)

            elif message.startswith("Rahul"):
                with st.chat_message(name="Rahul", avatar="🤔"):
                    st.write(message)


if clicked:
    chat.empty()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(run_debate())

    st.balloons()




