# 🛡️ Proactive Insurance Policy Guardian

Proactive Insurance Policy Guardian is an AI-powered web application that helps users **analyze, understand, and query their insurance policy documents in simple English.**

---

## ✨ Why This Project?

Insurance policies are often written in complex legal jargon. This tool makes them accessible to everyone by combining:

✅ PDF Upload & Parsing – Read your actual policy documents  
✅ AI Question Answering – Ask natural questions like “What is my deductible?”  
✅ Semantic Search– Retrieve the most relevant sections of your policy  
✅ Clear Explanations – Get easy-to-understand answers  
✅ Voice Input – Speak your questions  
✅ Chat History – See everything you’ve asked  
✅ Email Delivery – Receive results in your inbox

This project was built for the DSW Hackathon Challenge to showcase how AI can bring clarity to insurance.

---

## 🚀 Features Overview

- Upload Insurance PDF – Extracts all text content from your policy
- Semantic Search with FAISS – Finds the most relevant parts of the document
- Answer Generation with Mistral-7B – AI model composes clear responses
- Keyword Highlighting – Highlights relevant text in context
- Email Integration – Automatically emails answers if desired
- Voice Input – Ask questions by speaking into your microphone
- Persistent Chat History – Review past questions and answers
- Clear History Option – One click to reset your session
- Responsive UI – Tailwind CSS modern interface

---

## ⚙️ Tech Stack

| Layer              | Technology                                         |
| ------------------ | -------------------------------------------------- |
| Backend            | Python, Flask                                      |
| NLP & Embedding    | SentenceTransformer (`all-MiniLM-L6-v2`)           |
| Answer Generation  | Mistral-7B Instruct via Hugging Face Inference API |
| Vector Search      | FAISS                                              |
| PDF Processing     | PyPDF2                                             |
| Frontend           | HTML, Tailwind CSS, JavaScript                     |
| Email              | smtplib + Gmail SMTP                               |
| Environment Config | python-dotenv                                      |

---

## 🛠️ Setup Guide

Follow these steps to run the app locally:

---

### 1️⃣ Clone the Repository

git clone https://github.com/YOUR_USERNAME/Proactive_Insurance.git
cd Proactive_Insurance
2️⃣ Create and Activate Virtual Environment
Windows:

powershell
python -m venv venv
venv\Scripts\activate
macOS/Linux:

python3 -m venv venv
source venv/bin/activate
3️⃣ Install Dependencies

pip install -r requirements.txt
4️⃣ Configure Environment Variables
Create a .env file in the project root folder:

HF_TOKEN=your_huggingface_api_token
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
Important:

For Gmail, you must use an App Password. How to create one.

Your Hugging Face token must have Inference API access.

5️⃣ Start the Application

python app.py
Visit:

http://127.0.0.1:3000

🌐 Deployment
You can host this project on:

Render.com

Add gunicorn to requirements.txt

Set the start command: gunicorn app:app

Configure environment variables in the dashboard

💡 How It Works
Upload PDF

Text is extracted with PyPDF2

Chunking

The text splits into 300-character chunks

Embedding

SentenceTransformer encodes chunks into vectors

Semantic Search

FAISS finds the chunk most related to your question

Answer Generation

Mistral-7B generates a plain-English response

Extras

Highlights keywords in context

Stores chat history

Sends optional emails with the answer

Supports voice input for questions

📸 Screenshots
![Screenshot 2025-06-28 085310](https://github.com/user-attachments/assets/d07e3330-2176-47fe-8e06-ca2c7a27bbbc)

⚠️ Disclaimer
This project is for educational purposes only. It does not replace professional insurance advice. Always consult a qualified insurance advisor for policy guidance.

✨ Contact
Shivam Sharma

LinkedIn

Email:shivam3782@gmail.com
