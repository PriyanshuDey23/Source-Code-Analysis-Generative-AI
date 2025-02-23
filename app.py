import os
import streamlit as st
from langchain.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain
from dotenv import load_dotenv
from src.helper import load_embedding, repo_ingestion

# Load API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("⚠️ GOOGLE_API_KEY is missing! Please set it in your environment variables.")
    st.stop()

# Embedding
embeddings = load_embedding()

# Load persisted database
persist_directory = "db"
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

# LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

# Memory
memory = ConversationSummaryMemory(llm=llm, memory_key="chat_history", return_messages=True)

# Conversational Chain
qa = ConversationalRetrievalChain.from_llm(
    llm, retriever=vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 8}), memory=memory
)

# Streamlit UI
st.set_page_config(page_title="Source Code Analysis", page_icon="🤖", layout="wide")

st.title("🤖 Source Code Analysis")

# Sidebar for GitHub Repository Ingestion
with st.sidebar:
    st.header("📂 Ingest a GitHub Repository")
    repo_url = st.text_input("🔗 Enter GitHub Repository URL:", key="repo_input")

    if st.button("🚀 Ingest Repo"):
        if repo_url:
            try:
                repo_ingestion(repo_url)
                os.system("python store_index.py")
                st.success("✅ Repository ingested successfully! You can now ask questions.")
                st.session_state.repo_ingested = True
            except Exception as e:
                st.error(f"❌ Failed to ingest repository: {e}")

# Main Chat Interface
st.header("💬 Chat with GitHub Repository")

if "repo_ingested" not in st.session_state:
    st.session_state.repo_ingested = False

if st.session_state.repo_ingested:
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("💡 Ask me anything:", key="chat_input")

    if st.button("💬 Send"):
        if user_input.lower() == "clear":
            if os.path.exists("repo"):
                os.system("rm -rf repo")
                st.session_state.chat_history = []
                st.success("🧹 Repository cleared!")
            else:
                st.warning("⚠️ No repository found to clear.")
        elif user_input:
            result = qa(user_input)
            st.session_state.chat_history.append((user_input, result["answer"]))

    # Display chat history
    for query, response in st.session_state.chat_history:
        with st.container():
            st.markdown(f"**🧑‍💻 You:** {query}")
            st.markdown(f"**🤖 AI:** {response}")
