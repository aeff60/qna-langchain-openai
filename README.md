โค้ดนี้เป็นตัวอย่างของการสร้างเว็บแอปพลิเคชันด้วย Flask ที่ใช้บริการจาก OpenAI และไลบรารี Langchain ในการประมวลผลและตอบคำถาม โดยมีการใช้งาน CORS เพื่อรองรับการเข้าถึงจากโดเมนต่าง ๆ ได้ โดยรวมแล้วโค้ดนี้ทำงานดังนี้:

1. **การตั้งค่าและการนำเข้าไลบรารี:**

   ```python
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
   ```

2. **โหลดตัวแปรสิ่งแวดล้อม:**

   ```python
   load_dotenv()
   ```

3. **ตั้งค่า Flask แอปพลิเคชันและ CORS:**

   ```python
   app = Flask(__name__)
   CORS(app)
   ```

4. **กำหนดค่า API key ของ OpenAI:**

   ```python
   OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
   ```

5. **การตั้งค่าโมเดลและส่วนต่าง ๆ ของ Langchain:**

   ```python
   llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o")
   output_parser = StrOutputParser()
   embeddings = OpenAIEmbeddings()
   text_splitter = RecursiveCharacterTextSplitter()
   ```

6. **การโหลดและเตรียมเอกสารจากเว็บไซต์:**

   ```python
   loader = WebBaseLoader("https://www.borntodev.com/online-course/")
   docs = loader.load()
   documents = text_splitter.split_documents(docs)
   ```

7. **การสร้าง vector store ด้วย FAISS:**

   ```python
   vector = FAISS.from_documents(documents, embeddings)
   ```

8. **การสร้าง prompt template:**

   ```python
   prompt = ChatPromptTemplate.from_template("""
   ตอบคำถามต่อไปนี้ตามบริบทที่ให้ไว้เท่านั้น:

   <context>
   {context}
   </context>

   Question: {input}
   """)
   ```

9. **การสร้าง document chain:**

   ```python
   document_chain = create_stuff_documents_chain(llm, prompt)
   ```

10. **การสร้าง route สำหรับการรับคำถามและตอบคำถาม:**

    ```python
    @app.route("/ask", methods=["POST"])
    def answer_question():
        user_question = request.json.get("question")

        combined_input = {"input": user_question, "context": docs}

        response = document_chain.invoke(combined_input)

        answer = output_parser.parse(response)
        return jsonify({"answer": answer})
    ```

11. **การรันแอปพลิเคชัน:**
    ```python
    if __name__ == "__main__":
        app.run(debug=True)
    ```

### สรุปการทำงาน:

1. โหลดคอนฟิกและตั้งค่า Flask
2. โหลดเอกสารจาก URL ที่กำหนด
3. เตรียมเอกสารและสร้าง embeddings
4. สร้าง vector store สำหรับการค้นคืนข้อมูล
5. ตั้งค่า chain สำหรับการรวมเอกสารและตอบคำถาม
6. สร้าง API endpoint `/ask` ที่รับคำถามจากผู้ใช้และตอบกลับด้วยคำตอบที่ได้จากโมเดล OpenAI

เมื่อผู้ใช้ส่งคำถามมายัง endpoint `/ask` ผ่านคำขอแบบ POST แอปพลิเคชันจะนำคำถามนั้นไปประมวลผลกับโมเดลและส่งคำตอบกลับไปยังผู้ใช้ในรูปแบบ JSON.
