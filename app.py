import os
import dotenv
import streamlit as st
from huggingface_hub import InferenceClient

# === === === === DECLARATION === === === ===

LIMIT = 15   # Max no. of user messages

defaults = {
	"hf_token": None,
	"model_edit": "HuggingFaceTB/SmolLM3-3B",
	"model": None,
	"model_valid": False,
	"client": None,
	"system": "",
	"messages": [],
	"num_messages": 0
}

for k, v in defaults.items():
	st.session_state.setdefault(k, v)

st.set_page_config(page_title="ChatBot", page_icon=":material/smart_toy:", layout="wide")
dotenv.load_dotenv()

st.markdown(
	"""
		<style>
			[data-testid="stChatMessageAvatarUser"] {
				display: none;
			}
			[data-testid="stChatMessageAvatarAssistant"] {
				display: none;
			}
		</style>
	""",
	unsafe_allow_html=True
)
# === === === === FUNCTIONS === === === ===

def display_message(role,msg,num):
	with st.container(horizontal=True, horizontal_alignment=("right" if role == "user" else "left")):
		with st.chat_message(role, avatar=None, width="content"):
			st.markdown(msg)
			if role == "user":
				st.caption(f"{num}/{LIMIT}")

def validate_model():
	try:
		client = InferenceClient(
			provider="hf-inference",
			api_key=st.session_state.hf_token or os.environ["HF_TOKEN"]
		)
		completion = client.chat.completions.create(
			model=st.session_state.model_edit,
			messages=[{"role": "user", "content": "Hi!"}]
		)
		if completion.choices[0].message:
			st.session_state.model_valid = True
			st.session_state.model = st.session_state.model_edit
			st.session_state.client = client
			st.toast("Model and token validated", icon=":material/check_box:")
		else:
			st.toast("Validation failed! Please try again.", icon=":material/warning:")
	except Exception as e:
		st.toast(f"Validation failed! {e}", icon=":material/warning:")

def clear_chat():
	st.session_state.messages = []
	st.session_state.num_messages = 0
	st.toast("Chat history cleared!", icon=":material/mop:")

# === === === === DISPLAY PREVIOUS CHATS IN SESSION === === === ===

def display_all_msgs():
	i = 1
	for message in st.session_state.messages:
		display_message(message["role"],message["content"],i)
		if message["role"] == "user":
			i += 1

display_all_msgs()

# === === === === SIDEBAR === === === ===

def sidebar():
	with st.sidebar:
		# HF token input
		with st.popover("HF Token", icon=":material/vpn_key:", help="Enter HF token here"):
			st.text_input("Token", type="password", key="hf_token", label_visibility="collapsed")
		st.header("", divider=True)
		# Model input
		with st.expander(f"Model `{st.session_state.model}`", icon=":material/network_intelligence:" ,expanded=True):
			st.text_input("Model", key="model_edit", label_visibility="collapsed")
			st.button("Validate", on_click=validate_model, icon=":material/check_box:", help="Click on it to validate the above model")
		st.header("", divider=True)
		# System input
		with st.expander("Behavior", icon=":material/smart_toy:"):
			st.text_area(label="System", key="system", disabled=(not st.session_state.model_valid), label_visibility="collapsed")
		st.header("", divider=True)
		# Clear chat
		st.button(
			"Clear Chat",
			on_click=clear_chat,
			disabled=(st.session_state.num_messages == 0),
			icon=":material/mop:",
			type="tertiary"
		)

sidebar()

#  === === === === CHAT MECHANISM === === === ===

if not st.session_state.model_valid:
	st.caption("Enter your __:material/vpn_key: Hugging Face token__, enter __:material/network_intelligence: Model__ identifier, and click __:material/check_box: Validate__ to continue...")
# User input
new_message = st.chat_input("Say something...", max_chars=500, disabled=((not st.session_state.model_valid) or st.session_state.num_messages >= LIMIT))
if new_message:
	st.session_state.num_messages += 1
	display_message("user", new_message, st.session_state.num_messages)
	st.session_state.messages.append({"role": "user", "content": new_message})

	# Send request
	with st.spinner("Typing..."):
		completion = st.session_state.client.chat.completions.create(
			model=st.session_state.model,
			messages=([{"role": "system", "content": st.session_state.system}] if len(st.session_state.system) > 0 else []) + st.session_state.messages,
		)

	# Handle response
	if bot_response := completion["choices"][0]["message"]["content"]:
		if "<think>" in bot_response:
			bot_response = bot_response[(bot_response.find("</think>") + 8):]
		display_message("assistant",bot_response,0)
		st.session_state.messages.append({"role": "assistant", "content": bot_response})
	else:
		st.toast("Message not received", icon=":material/warning:")

if st.session_state.num_messages >= LIMIT:
	st.error("You've reached your limit")
