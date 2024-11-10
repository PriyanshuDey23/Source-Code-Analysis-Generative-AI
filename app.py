from src.helper import  * 
import os
from langchain.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationSummaryMemory # Creating memory
from langchain.chains import ConversationalRetrievalChain
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request


app = Flask(__name__)

# Load th api key
load_dotenv()

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

# Embedding
embeddings = load_embedding()


# Db is created in research
# Check store_index for vector embedding creating process andstoring in Db


# Now we can load the persisted database from disk, and use it as normal.
persist_directory = "db"
vectordb = Chroma(persist_directory=persist_directory,
                  embedding_function=embeddings)



# LLm
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-002",temperature=0.3, max_tokens=500)


memory = ConversationSummaryMemory(llm=llm, memory_key = "chat_history", return_messages=True)

qa = ConversationalRetrievalChain.from_llm(llm, retriever=vectordb.as_retriever(search_type="mmr", search_kwargs={"k":8}), memory=memory)


# Default
@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')


# Repo ingestion
@app.route('/chatbot', methods=["GET", "POST"])
def gitRepo():

    if request.method == 'POST':
        user_input = request.form['question']
        repo_ingestion(user_input) # clone any github repositories 
        os.system("python store_index.py") # It will execute store index.py

    return jsonify({"response": str(user_input) })



# Chat operation
@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"] # User message
    input = msg
    print(input)

    if input == "clear": # Clear the previous repository
        os.system("rm -rf repo")

    result = qa(input) # qa operation
    print(result['answer'])
    return str(result["answer"])


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080,debug=True)
