# -*- coding: utf-8 -*-
"""app.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1M8l-FKTy5KO4j3cueuZWQvlUxp21tcQj
"""

!pip install langchain
!pip install PyPDF2
!pip install openai
!pip install faiss-cpu
!pip install tiktoken
!pip install streamlit
!pip install flask-ngrok

# Commented out IPython magic to ensure Python compatibility.
# %%writefile streamlit_ui.py
# 
# import streamlit as st
# import requests
# 
# st.title("PDF Chatbot User Interface")
# user_input = st.text_input("Enter your question:")
# if st.button("Get Answer"):
#     response = requests.post("http://localhost:5000/generate_response", json={"user_input": user_input})
#     if response.status_code == 200:
#         st.write("Answer:", response.text)
#     else:
#         st.write("Error getting an answer.")
#

from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
import os

app = Flask(__name__)

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = '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'

@app.route('/')
def index():
    return "Welcome to the PDF Chatbot!"

@app.route('/generate_response', methods=['POST'])
def generate_response():
    user_input = request.json.get("user_input")

    # PDF processing and question-answering code
    pdfreader = PdfReader("unit1_1.pdf")
    raw = ''
    for i, page in enumerate(pdfreader.pages):
        content = page.extract_text()
        if content:
            raw += content

    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=850,
        chunk_overlap=200,
        length_function=len,
    )
    text = text_splitter.split_text(raw)

    embeddings = OpenAIEmbeddings()
    document_search = FAISS.from_texts(text, embeddings)

    # Question-answering code
    query = user_input
    docs = document_search.similarity_search(query)
    from langchain.chains.question_answering import load_qa_chain
    from langchain.llms import OpenAI
    chain = load_qa_chain(OpenAI(), chain_type="stuff")
    response = chain.run(input_documents=docs, question=query)

    return jsonify({"answer": response})

run_with_ngrok(app)  # Initialize ngrok for Flask

if __name__ == '__main__':
    app.run()

!python your_flask_app.py
!streamlit run streamlit_ui.py



