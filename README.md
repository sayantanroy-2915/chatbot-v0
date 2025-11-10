# Streamlit LLM Application - Single-turn Interaction Interface 

This repository contains the source code for the chatbot application explained in the following article:

👉🏻 [Read the article on Hashnode](https://roysntnwr0.hashnode.dev/streamlit-llm-app#heading-application-a-single-turn-interaction-interface)

## How to run it

1. Setup `Ollama`. (refer to the article for more detail)
2. Clone the repository and checkout branch `hashnode_article_1a`
3. Create virtual environment, activate it, and install requirements \ 
For Windows
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
For Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```
4. Run the app
```bash
streamlit run app.py
```