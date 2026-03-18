import streamlit as st
import asyncio
from debate import teamconfig, debate

st.title("Agent Council")

topic = st.text_input("Enter a topic of the debate", "Should India Buy Russian Oil?")
clicked = st.button("Start", type="primary")

chat_placeholder = st.empty()


def parse_message(msg: str):
    # Expected: "Message:Host:content"
    if msg.startswith("Message:"):
        _, source, content = msg.split(":", 2)
        return source.strip(), content.strip()
    return "System", msg


async def run_debate_stream(topic, placeholder):
    team = await teamconfig(topic)

    with placeholder.container():
        async for message in debate(team):
            source, content = parse_message(message)

            if source == "Host":
                with st.chat_message("Host", avatar="🥸"):
                    st.write(content)

            elif source == "Narendra":
                with st.chat_message("Narendra", avatar="🫡"):
                    st.write(content)

            elif source == "Rahul":
                with st.chat_message("Rahul", avatar="🤔"):
                    st.write(content)

            else:
                st.write(content)


if clicked:
    chat_placeholder.empty()

    asyncio.run(run_debate_stream(topic, chat_placeholder))

    st.balloons()