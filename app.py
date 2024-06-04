from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.documents import Document
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

CORS(app)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")

output_parser = StrOutputParser()

embeddings = OpenAIEmbeddings()

text_splitter = RecursiveCharacterTextSplitter()

loader = WebBaseLoader("https://www.borntodev.com/online-course/")
docs = loader.load()
documents = text_splitter.split_documents(docs)

vector = FAISS.from_documents(documents, embeddings)
prompt = ChatPromptTemplate.from_template("""
ตอบคำถามต่อไปนี้ตามบริบทที่ให้ไว้เท่านั้น:

<context>
{context}
</context>

Question: {input}
""")

document_chain = create_stuff_documents_chain(llm, prompt)

@app.route("/ask", methods=["POST"])
def answer_question():
    user_question = request.json.get("question")
    
    combined_input = {"input": user_question, "context": docs}

    response = document_chain.invoke(combined_input)

    answer = output_parser.parse(response)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
