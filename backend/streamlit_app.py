from io import BytesIO
from typing import Set

import requests
import streamlit as st
from PIL import Image

from utils.core import run_llm

st.set_page_config(
    page_title="RAG Documentation Helper",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Add this function to get a profile picture
def get_profile_picture(email):
    # This uses Gravatar to get a profile picture based on email
    # You can replace this with a different service or use a default image
    gravatar_url = f"https://www.gravatar.com/avatar/{hash(email)}?d=identicon&s=200"
    response = requests.get(gravatar_url)
    img = Image.open(BytesIO(response.content))
    return img


# Custom CSS for dark theme and modern look
st.markdown(
    """
<style>
    .stApp {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .stTextInput > div > div > input {
        background-color: #2D2D2D;
        color: #FFFFFF;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: #FFFFFF;
    }
    .stSidebar {
        background-color: #252526;
    }
    .stMessage {
        background-color: #2D2D2D;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Set page config at the very beginning

# Sidebar user information
with st.sidebar:
    st.title("User Profile")

    # You can replace these with actual user data
    user_name = "John Doe"
    user_email = "john.doe@example.com"

    profile_pic = get_profile_picture(user_email)
    st.image(profile_pic, width=150)
    st.write(f"**Name:** {user_name}")
    st.write(f"**Email:** {user_email}")

st.header("LangChain🦜🔗 RAG LangChain Documentation Helper")

# persist in the memory user input history and what the chat answers
# because this file is running infinitely, we need to have a way to store the messages
if (
        "chat_answers_history" not in st.session_state
        and "user_prompt_history" not in st.session_state
        and "chat_history" not in st.session_state
):
    st.session_state["chat_answers_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []


def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"- {source}\n"
    return sources_string


# Create two columns for a more modern layout
col1, col2 = st.columns([2, 1])

with col1:
    prompt = st.text_input("Prompt", placeholder="Enter your message here...")

with col2:
    if st.button("Submit", key="submit"):
        prompt = prompt or "Hello"  # Default message if input is empty

if prompt:
    with st.spinner("Generating response.."):
        generated_response = run_llm(query=prompt,
                                     chat_history=st.session_state["chat_history"])
        # receives also a list of tuples (chat_history) with the role and the content
        sources = set([doc.metadata["source"] for doc in generated_response["source_documents"]])  # remove duplicates

        formatted_response = f"{generated_response['result']} \n\n {create_sources_string(sources)}"

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_response)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(("ai", generated_response["result"]))
        # tuple that represents the structure that LangChain likes
        # first -> role, human or ai (LLM)
        # second -> content, prompt the user sends or the message backf rom the LLM

if st.session_state["chat_answers_history"]:
    for user_query, generated_response in zip(st.session_state["user_prompt_history"],
                                              st.session_state["chat_answers_history"]):
        st.chat_message("user").write(user_query)
        st.chat_message("assistant").write(generated_response)

# Add a footer
st.markdown("---")
st.markdown("Powered by LangChain and Streamlit")
