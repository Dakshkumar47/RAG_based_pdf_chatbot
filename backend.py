import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnableParallel,RunnablePassthrough
from dotenv import load_dotenv
from io import BytesIO
from langchain_core.documents import Document
from pypdf import PdfReader
load_dotenv()
import os

# from pathlib import Path
# import os
# from langchain_community.document_loaders import PyPDFLoader
# the code above is needed if we save the file to disk and then access it


"""Instead of putting network clients or machine learning models into st.session_state, you should use Streamlit's @st.cache_resource decorator. This is explicitly designed for things like database connections, API clients, and ML models so they safely persist across reruns without their connections closing."""
# @st.cache_resource
# def get_llm():
#     return ChatGroq(model='openai/gpt-oss-120b')

@st.cache_resource
def get_embedding_model():
    return HuggingFaceEmbeddings(model='sentence-transformers/all-MiniLM-L6-v2')



# def save_uploaded_file(uploaded_file):
#     if uploaded_file is not None:
#         save_dir = Path("temp_storage/documents")
#         if not os.path.exists(save_dir):
#             save_dir.mkdir(parents=True, exist_ok=True)

#         pdf_path = save_dir / uploaded_file.name
#         st.session_state['pdf_path'] = pdf_path
#         with open(pdf_path, "wb") as f:
#             f.write(uploaded_file.getbuffer())

#         return "file saved"

    # the code above is needed if we save the file to disk and then access it

@st.cache_resource
def get_llm():
    # groq_api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
    # gemini_api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
    # primary_llm = ChatGroq(model='openai/gpt-oss-120b',api_key=groq_api_key)
    # secondary_llm = ChatGoogleGenerativeAI(model='gemini-3.5-flash',api_key=gemini_api_key)
    # # it will ensure that same structure can be used either we are loading api key from local machine or from streamlit cloud secrets


    primary_llm = ChatGroq(model='openai/gpt-oss-120b')
    secondary_llm = ChatGoogleGenerativeAI(model='gemini-3.5-flash')
    llm_with_fallbacks = primary_llm.with_fallbacks([secondary_llm])
    # the items inside the list are the options treated in the same priority as order provided

    return llm_with_fallbacks


def prepare_to_chat():
    if st.session_state['loaded_pdf'] == '' :  
         #to ensure we don't redundantly load the pdf into the document loader
        # pdf_loader = PyPDFLoader(file_path=st.session_state['pdf_path'])
        # st.session_state['loaded_pdf'] = pdf_loader.load()
        # the code above is needed if we save the file to disk and then access it

        # load the pdf directly from RAM
        # 1. Get the bytes directly from the Streamlit UploadedFile in RAM
        file_bytes = st.session_state['file_object'].getvalue()
        
        # 2. Read the PDF from memory
        pdf_reader = PdfReader(BytesIO(file_bytes))
        
        # 3. Extract text and convert them into LangChain Document objects
        docs = []
        for i, page in enumerate(pdf_reader.pages):
            text = page.extract_text()
            if text:
                docs.append(Document(page_content=text, metadata={"page": i}))
                
        st.session_state['loaded_pdf'] = docs


    embedding_model = get_embedding_model()


    if st.session_state['vector_store'] == '':
        # chunking the extracted text & 
        # creating a vector store from the chunks

        # it is here bcs we need chunks only when we don't have the vector store
        chunker = SemanticChunker(embeddings=embedding_model)
        chunks = chunker.split_documents(st.session_state['loaded_pdf'])
        # print(type(chunks))       # <class list>
        # print(type(chunks[0]))        #<class 'langchain_core.documents.base.Document'>


        # it ensures that if we have vector store for a chat then we don't create it again and again
        st.session_state['vector_store'] = FAISS.from_documents(documents = chunks,embedding = embedding_model)

        st.session_state['retriever'] = st.session_state['vector_store'].as_retriever(search_type="similarity", search_kwargs={"k": 2})


    #------------- setting up prompt template---------------------------
    st.session_state['prompt_template'] = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful study assistant. Answer the user's question using ONLY the provided context.\n\nContext:\n{context}"),
        ("human", "{question}")
    ])

    st.session_state['output_parser'] = StrOutputParser()


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def chat_to_llm():
    
    llm = get_llm()
    retriever = st.session_state['retriever']

    # Update this specific block:
    setup_and_retrieval = RunnableParallel(
        {
            "context": retriever | format_docs,  # Extract text from Documents here
            "question": RunnablePassthrough()
        }
    )
    
    final_chain = setup_and_retrieval | st.session_state['prompt_template'] | llm | st.session_state['output_parser']

    try:
        response = final_chain.invoke(st.session_state['user_query'])

    except Exception as e:
        raise e

    return response


# def remove_temp_files():
#     import shutil 
#     folder_to_remove = Path("temp_storage")
#     shutil.rmtree(folder_to_remove)
# the code above is needed if we save the file to disk and then access it