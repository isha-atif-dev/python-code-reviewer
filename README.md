---
title: Python Code Reviewer
emoji: 🐍
colorFrom: purple
colorTo: pink
sdk: docker
sdk_version: "3.10"
app_file: app.py
pinned: false
---

# 🐍 Python Code Reviewer

An AI-powered Python code review tool that analyses your code across four dimensions.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b)
![Claude](https://img.shields.io/badge/Powered%20by-Claude%20AI-blueviolet)

## ✨ Features

- 🐛 **Bug Detection** — Finds bugs, edge cases and risky patterns with line numbers
- ⏱️ **Complexity Analysis** — Time and space complexity with plain English explanation
- 🏗️ **OOP Suggestions** — Design improvement recommendations
- ✨ **Auto Rewrite** — Clean, improved version of your code

## 🚀 Live Demo

👉 [Try it on HuggingFace Spaces](https://huggingface.co/spaces/ishaAtif/python-code-reviewer)

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Web interface |
| Claude API (Haiku) | AI code review |
| python-dotenv | Environment variable management |

## ⚙️ Run Locally
```bash
# Clone the repo
git clone https://github.com/isha-atif-dev/python-code-reviewer.git
cd python-code-reviewer

# Install dependencies
pip install -r requirements.txt

# Add your Claude API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# Run the app
streamlit run app.py
```

## 📁 Project Structure
```
python-code-reviewer/
├── app.py            # Streamlit frontend
├── reviewer.py       # Claude API logic
├── prompts.py        # Prompt templates
├── requirements.txt  # Dependencies
├── Dockerfile        # HuggingFace deployment
└── .gitignore        # Ignores .env file
```

## 🔒 Note

Never commit your `.env` file. Your API key is protected via `.gitignore`.