import streamlit as st
import requests as req

st.set_page_config("Single Interaction", page_icon=":material/network_intel_node")

API_URL = "http://127.0.0.1:11434/api/"

defaults = {
	"model": None,
	"models": [],
	"prompt": "",
	"response": ""
}

for k, v in defaults.items():
	st.session_state.setdefault(k, v)


def lookup_models():
	res = req.get(API_URL + "tags")
	if res.status_code == 200:
		st.session_state.models = [model["name"] for model in res.json()["models"]]
		if st.session_state.model not in st.session_state.models:
			st.session_state.model = st.session_state.models[0]
	else:
		st.toast("No LLM found, check if Ollama is running", icon=":material/error:")


def generate():
	try:
		with st.spinner("Please wait...", show_time=True):
			res = req.post(
				API_URL + "generate",
				json={
					"model": st.session_state.model,
					"prompt": st.session_state.prompt,
					"stream": False
				})
		json = res.json()
		if "response" in json:
			st.session_state.response = res.json()["response"]
		elif "error" in res.json():
			st.toast(f"Error occurred: {res.json()['error']}", icon=':material/error:')
	except Exception as e:
		st.toast(f"Error occurred: {e}", icon=':material/error:')


def render_ui():
	c11, c12 = st.columns((4, 1), vertical_alignment="bottom")
	with c11:
		st.selectbox("Model", st.session_state.models, key="model")
	with c12:
		st.button("Refresh", on_click=lookup_models)
	c21, c22 = st.columns((4, 1), vertical_alignment="bottom")
	with c21:
		st.text_input("Prompt", key="prompt", disabled=(st.session_state.model is None))
	with c22:
		st.button("Generate", on_click=generate, disabled=(len(st.session_state.prompt) == 0))
	st.markdown(st.session_state.response)


if __name__ == "__main__":
	lookup_models()
	render_ui()
