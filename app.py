import os
from dotenv import load_dotenv
from MedicalBot.helper import load_pdf_file, text_split, download_hugging_face_embeddings
from MedicalBot.prompt import *
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

from flask import Flask, request, jsonify, render_template


app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

embeddings = download_hugging_face_embeddings()

index_name = "medicalbot"


# Embed each chunk and upsert the embeddings into your Pineceon index


docsearch = PineconeVectorStore.from_existing_index(
            index_name=index_name,
            embedding=embeddings
        )

# Creating the retriever and the LLM for the question-answering chain
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})


# Creating the language model
llm = OpenAI(model_name="gpt-4o-mini", openai_api_key=OPENAI_API_KEY, temperature=0, max_tokens=500)

# Creating the prompt template for the question-answering chain
prompt = ChatPromptTemplate.from_template([("system",system_prompt),("human", "{input}")])

# Creating the RAG Chain

question_answering_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answering_chain)



# Flask route for the home page

@app.route('/')
def index():
    return render_template('chat.html')


@app.route('/get', methods=['GET', 'POST'])
def chat():
    msg = request.form['msg']
    input= msg
    print(input)
    response = rag_chain.invoke({"input": msg})
    print("Response:", response["answer"])
    return str(response["answer"])


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)

# http://localhost:8080/