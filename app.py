from flask import Flask, render_template, request, session, redirect, url_for

import os
import PyPDF2
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from huggingface_hub import InferenceClient
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask
app = Flask(__name__)
app.secret_key = "super_secret_key"  # Needed for session
app.config["UPLOAD_FOLDER"] = "uploads"

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Load embedding model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize Hugging Face Inference Client
client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    token=os.getenv("HF_TOKEN")
)

# Helper to clean text
def clean_text(text):
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        line = line.strip()
        if line:
            cleaned.append(line)
    return " ".join(cleaned)

# Helper to highlight keywords
def highlight_context(context, keywords):
    for word in keywords:
        context = context.replace(
            word, f"<mark>{word}</mark>"
        )
    return context

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    retrieved_context = ""
    filename = ""

    if "history" not in session:
        session["history"] = []

    if request.method == "POST":
        pdf = request.files.get("pdf")
        question = request.form.get("question")
        email = request.form.get("email")
        filename = request.form.get("filename", "")

        # If new PDF uploaded
        if pdf:
            filename = pdf.filename
            pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            pdf.save(pdf_path)

            text = ""
            reader = PyPDF2.PdfReader(pdf_path)
            for page in reader.pages:
                text += page.extract_text() or ""

            text_path = os.path.join(app.config["UPLOAD_FOLDER"], f"{filename}.txt")
            with open(text_path, "w", encoding="utf-8") as f:
                f.write(text)

        # Q&A processing
        if filename and question:
            # Load schedule text
            text_path = os.path.join(app.config["UPLOAD_FOLDER"], f"{filename}.txt")
            with open(text_path, "r", encoding="utf-8") as f:
                schedule_text = f.read()

            # Load policy wording text
            wording_path = os.path.join(app.config["UPLOAD_FOLDER"], "wording.pdf")
            wording_text = ""
            wording_reader = PyPDF2.PdfReader(wording_path)
            for page in wording_reader.pages:
                wording_text += page.extract_text() or ""

            # Combine both texts
            full_text = schedule_text + "\n" + wording_text

            # Chunk
            chunk_size = 500
            chunks = [full_text[i:i + chunk_size] for i in range(0, len(full_text), chunk_size)]

            embeddings = embed_model.encode(chunks).astype("float32")
            index = faiss.IndexFlatL2(embeddings.shape[1])
            index.add(embeddings)

            q_embedding = embed_model.encode([question]).astype("float32")
            _, I = index.search(q_embedding, k=3)
            retrieved_chunks = [chunks[i] for i in I[0]]
            raw_context = " ".join([clean_text(chunk) for chunk in retrieved_chunks])

            # Highlight keywords
            keywords = question.lower().split()
            retrieved_context = highlight_context(raw_context, keywords)

            prompt = (
                "You are an Indian insurance policy expert. Based only on the policy text below, answer the user's question. "
                "If the answer is not specified, reply exactly: 'Not specified in the policy.'\n\n"
                f"<<<POLICY>>>\n{raw_context}\n<<<END_POLICY>>>\n\n"
                f"Question: {question}\n\n"
                "Answer in clear, short plain English."
            )

            messages = [
                {"role": "system", "content": "You are a helpful insurance policy expert."},
                {"role": "user", "content": prompt}
            ]

            response = client.chat_completion(
                messages,
                max_tokens=200,
                temperature=0.0
            )
            answer = response.choices[0].message.content.strip()

            # Save chat history
            session["history"].append({"question": question, "answer": answer})

            # Email if needed
            if email:
                send_email(email, question, answer)

        elif not pdf and not question:
            answer = "Please upload a PDF and/or provide a question."

    return render_template(
        "index.html",
        answer=answer,
        retrieved_context=retrieved_context,
        filename=filename,
        history=session.get("history", [])
    )


# Email sending helper
def send_email(to_email, question, answer):
    from_email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEText(f"Question:\n{question}\n\nAnswer:\n{answer}")
    msg["Subject"] = "Your Insurance Policy Answer"
    msg["From"] = from_email
    msg["To"] = to_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(from_email, password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()
    
@app.route("/clear_history", methods=["POST"])
def clear_history():
    session["history"] = []
    return redirect(url_for("index"))

if __name__ == "__main__":

    # Default to 8082 which also works on many platforms (but overridden by $PORT if set)
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
