import streamlit as st
import re

from chatbot import build_chain

st.set_page_config(
    page_title="YouTube Chatbot",
    page_icon="🎥"
)

st.title("🎥 YouTube Chatbot")


def extract_video_id(url):

    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url):
        return url

    match = re.search(
        r"(?:v=|youtu\.be/|shorts/|embed/)([A-Za-z0-9_-]{11})",
        url,
    )

    if match:
        return match.group(1)

    return None


if "chain" not in st.session_state:
    st.session_state.chain = None

video_input = st.text_input(
    "Paste YouTube URL or Video ID"
)

if st.button("Load Video"):

    video_id = extract_video_id(video_input)

    if video_id is None:
        st.error("Invalid YouTube URL or Video ID.")
        st.stop()

    try:

        with st.spinner("Loading transcript and building vector database..."):

            st.session_state.chain = build_chain(video_id)

        st.success("Video Loaded Successfully!")

        st.video(
            f"https://www.youtube.com/watch?v={video_id}"
        )

    except Exception as e:

        st.error(str(e))


question = st.chat_input(
    "Ask anything about the video..."
)

if question:

    if st.session_state.chain is None:

        st.warning("Please load a video first.")

    else:

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                answer = st.session_state.chain.invoke(question)

            st.write(answer)