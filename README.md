# 🤖 Local LLM Chatbot — Version 0.1
Welcome to the v0 release of a lightweight chatbot powered by Streamlit and Ollama. This version is kept minimal, designed to run locally, and uses open-source language models like LLaMA, Mistral, etc.

## 💡 Features

* Chat with open-source LLMs (via Ollama)
* Easy-to-use UI built with Streamlit
* Switch between available local models
* Adjustable temperature and system prompts
* Avatars for user and bot

## 🚀 Getting Started
### 1. Install Dependencies
Create a virtual environment (optional but recommended), then install:

```pip install -r requirements.txt```

Or, install manually:

```pip install streamlit requests```

### 2. Set Up Ollama
Ensure Ollama is installed and running

```ollama serve```

Pull a model (skip if model exists)

```ollama pull llama3```

```ollama pull mistral```

```ollama pull gemma```

### 3. Run the App
Launch the chatbot

```streamlit run app.py```

Then open your browser to http://localhost:8501

## 🛠️ Configuration

All configurations are available in the sidebar

🔄 Change the model on the fly

🧠 Add a custom system prompt

🔥 Adjust the temperature (creativity level)

👤 Change avatars

🧹 Clear the chat if things get too weird