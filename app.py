import streamlit as st
import requests as req
from langchain_ollama import ChatOllama

st.set_page_config("Chat", page_icon=":material/network_intel_node:")

API_URL = "http://127.0.0.1:11434/api/"

defaults = {
	"model": "",
	"models": [],
	"instruction": "",
	"messages": [],
	"llm": None
}

for k, v in defaults.items():
	st.session_state.setdefault(k, v)


def init_llm():
	st.session_state.llm = ChatOllama(model=st.session_state.model)


def lookup_models():
	res = req.get(API_URL + "tags")
	if res.status_code == 200:
		st.session_state.models = [model["name"] for model in res.json()["models"]]
		if st.session_state.model not in st.session_state.models:
			st.session_state.model = st.session_state.models[0]
			init_llm()
	else:
		st.toast("No LLM found, check if Ollama is running", icon=":material/error:")


def generate():
	if st.session_state.instruction:
		messages = [("system", st.session_state.instruction)]
	else:
		messages = []
	messages.extend(st.session_state.messages)
	with st.spinner("Typing...", show_time=True):
		new_message = st.session_state.llm.invoke(messages)
	with st.chat_message("ai"):
		st.markdown(new_message.content)
	st.session_state.messages.append(("ai", new_message.content))


def sidebar():
	with st.sidebar:
		c1, c2 = st.columns((3, 1), vertical_alignment="bottom")
		with c1:
			st.selectbox("Model", st.session_state.models, key="model", on_change=init_llm)
		with c2:
			st.button("", help="Sync models", icon=":material/sync:", on_click=lookup_models)
		st.text_area("Instructions", key="instruction")


def load_msgs():
	for message in st.session_state.messages:
		with st.chat_message(message[0], width="content"):
			st.markdown(message[1])


def msg_sender():
	if message := st.chat_input("Ask anything..."):
		st.session_state.messages.append(("user", message))
		with st.chat_message("user", width="content"):
			st.markdown(message)
		generate()


def render_ui():
	sidebar()
	load_msgs()
	msg_sender()


if __name__ == "__main__":
	try:
		lookup_models()
		render_ui()
	except Exception as e:
		st.error(e)
