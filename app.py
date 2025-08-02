from langchain_openai import ChatOpenAI
import streamlit as st
import os


# Load From .env File
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")


cloud_llm=ChatOpenAI(
    model='qwen/qwen3-235b-a22b:free',
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)


local_llm=ChatOpenAI(
    model='ai/gemma3:1B-Q4_K_M',
    api_key="nope",
    base_url='http://172.17.0.1:12434/engines/llama.cpp/v1'
)

response = local_llm.invoke("How are you?")


print(response.content)


###############
st.title('Talk to me....')
think_harder=st.checkbox(
    "Think harder...",
    value=False
)


st.session_state.setdefault("messages",[])

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

    
 
prompt = st.chat_input("Type your message...")

if prompt:
    st.session_state["messages"].append(
       { "role":"user",
        "content":prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    context=""

    for msg in st.session_state["messages"]:
        context += msg["role"] + ": " + msg["content"]

    if think_harder==False:
        llm=local_llm
    elif think_harder==True:
        llm=cloud_llm

    response = llm.invoke(context)
    st.session_state["messages"].append(
       { "role":"assistant",
        "content":response.content}
    )

    with st.chat_message("assistant"):
        st.write(response.content)    