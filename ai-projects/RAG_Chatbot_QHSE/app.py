import streamlit as st
import os
from dotenv import load_dotenv

st.set_page_config(
    page_title="QHSE Navigator",
    layout="wide",
    initial_sidebar_state="expanded"
)
from langchain_groq.chat_models import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
#from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.document_loaders import PyPDFDirectoryLoader
#from torch import embedding


load_dotenv()

# Load API keys from environment variables
groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(api_key=groq_api_key, model="gemma2-9b-it")

openai_api_key = os.getenv("OPENAI_API_KEY")
embedding = OpenAIEmbeddings(openai_api_key=openai_api_key)

prompt = ChatPromptTemplate.from_template(
    """
    You are a helpful assistant that answers questions based on the provided context only.
    Please provide most accurate response based on the question asked.
    <context>
    {context}
    </context>

    Question: {input}
     
    """  
)

def create_vector_embedding():
    if "vectors" not in st.session_state:
        st.session_state.embeddings = embedding # Initialize embeddings
        st.session_state.loader = PyPDFDirectoryLoader("QHSE") # Data Ingestion
        st.session_state.documents = st.session_state.loader.load() # complete doc loading
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=1000)
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.documents) # split docs into chunks
        st.session_state.vectors = Chroma.from_documents(st.session_state.final_documents,
                                                         st.session_state.embeddings) # create vector store
    return st.session_state.vectors

# Create sidebar with document list
with st.sidebar:

    # Get list of PDF files in QHSE folder
    qhse_folder = "QHSE"
    if os.path.exists(qhse_folder):
        pdf_files = [f for f in os.listdir(qhse_folder) if f.lower().endswith('.pdf')]
        
        if pdf_files:
            st.markdown("## You are Chatting with")
            for pdf_file in sorted(pdf_files):
                # Clean up filename for display (remove timestamps and extensions)
                display_name = pdf_file.replace('_', ' ').replace('.pdf', '')
                st.markdown(f"📄 {display_name}")
        else:
            st.warning("No PDF files found in QHSE folder")
    else:
        st.error("QHSE folder not found")

st.title("QHSE Navigator")
user_prompt = st.text_input("Enter your query on Aries QHSE")

if user_prompt:
    vectors = create_vector_embedding()
    document_chain = create_stuff_documents_chain(llm, prompt) # create chain for passing a list of documents to a model
    retriever = vectors.as_retriever() #Finds the most relevant text chunks
    retrieval_chain = create_retrieval_chain(retriever, document_chain) # create retrieval chain

    response = retrieval_chain.invoke({"input": user_prompt}) # invoke the chain with user input

    st.write(response["answer"]) # display the response
