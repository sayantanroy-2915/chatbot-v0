import streamlit as st
import requests as req
from time import sleep
import json

# === === === === DECLARATION === === === ===
TEMP_MIN = 0.0
TEMP_DEF = 1.0
TEMP_MAX = 2.0
STREAM_MIN = 0.01
STREAM_DEF = 0.1
STREAM_MAX = 1.0
API_URL = "http://127.0.0.1:11434/api/"

defaults = {
	"model": None,
	"models": [],
	"system": "",
	"temp": TEMP_DEF,
	"stream": False,
	"stream_delay": STREAM_DEF,
	"messages": [],
	"avatar_user": "👨🏻",
	"avatar_bot": "🤖"
}

for k, v in defaults.items():
	st.session_state.setdefault(k, v)

st.set_page_config(page_title="ChatBot", page_icon="🤖")

# === === === === DISPLAY PREVIOUS CHATS IN SESSION === === === ===
for message in st.session_state.messages:
	with st.chat_message("user", avatar=(st.session_state.avatar_bot if message["role"] == "assistant" else st.session_state.avatar_user), width="content"):
		st.markdown(message["content"])

# === === === === SIDEBAR === === === ===
with st.sidebar:
	# Model Selector
	def lookup_models():
		res = req.get(API_URL + "tags")
		if res.status_code == 200:
			st.session_state.models = [model["name"] for model in res.json()["models"]]
		else:
			st.toast("No LLM found, check if Ollama is running", icon="🚨")

	lookup_models()
	st.selectbox("Model", st.session_state.models, key="model")
	st.button("Refresh", on_click=lookup_models, icon="🔃", type="tertiary")

	st.divider()
	# System input
	st.text_area(label="Chatbot Behavior (System)", key="system", disabled=(st.session_state.model is None))

	st.divider()

	# Stream option
	st.toggle("Streaming", key="stream", disabled=(st.session_state.model is None))
	st.session_state.stream_delay = st.slider("Delay (seconds)", STREAM_MIN, STREAM_MAX, st.session_state.stream_delay, disabled=(not st.session_state.stream))

	st.divider()

	# Temperature slider
	st.session_state.temp = st.slider("Creativity (Temperature)", TEMP_MIN, TEMP_MAX, st.session_state.temp, disabled=(st.session_state.model is None))

	st.divider()

	# Avatar selector
	st.selectbox("User Avatar", ["👨🏻", "👩🏻", "👨🏻‍💻", "👩🏻‍💻", "👤"], index=0, key="avatar_user", accept_new_options=True)
	st.selectbox("Bot Avatar", ["🤖", "💻", "🖥️", "📱", "🦙"], index=0, key="avatar_bot", accept_new_options=True)

	st.divider()

	# Clear chat
	def clear_chat():
		st.session_state.messages = []
		st.toast("Chat history cleaned!", icon="✨")

	st.button("Clear Chat", on_click=clear_chat, disabled=(len(st.session_state.messages) == 0), icon="🧹", type="tertiary")

#  === === === === CHAT MECHANISM === === === ===
# User input
new_message = st.chat_input("Say something...", max_chars=512, disabled=(st.session_state.model is None))
if new_message:
	with st.chat_message("user", avatar=st.session_state.avatar_user, width="content"):
		st.markdown(new_message)
	st.session_state.messages.append({"role": "user", "content": new_message})

	# Send request
	req_body = {
		"model": st.session_state.model,
		"messages": ([{"role": "system", "content": st.session_state.system}] if len(st.session_state.system) > 0 else [
			None]) + st.session_state.messages,
		"stream": st.session_state.stream,
		"options": {"temperature": st.session_state.temp}
	}

	with st.spinner("Typing..."):
		res = req.post(API_URL + "chat", json=req_body)

	# Handle response
	if res.status_code == 200:
		if st.session_state.stream:
			with st.chat_message("user", avatar=st.session_state.avatar_bot, width="content"):
				full_message = ""
				placeholder = st.empty()
				for chunk in res.iter_lines():
					if chunk:
						full_message += json.loads(chunk)["message"]["content"]
						placeholder.markdown(full_message)
						sleep(st.session_state.stream_delay)
				st.session_state.messages.append({"role": "assistant", "content": full_message})
		else:
			with st.chat_message("user", avatar=st.session_state.avatar_bot, width="content"):
				if new_message := res.json().get("message", {}).get("content", ""):
					st.markdown(new_message)
					st.session_state.messages.append({"role": "assistant", "content": new_message})
				elif err := res.json().get("error", {}):
					st.markdown(err)
					st.session_state.messages.append({"role": "assistant", "content": err})
	else:
		st.toast(f"{res.status_code}", icon="🚨")
