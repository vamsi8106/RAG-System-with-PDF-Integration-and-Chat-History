from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tempfile

def process_pdfs(uploaded_files):
    """Process and split PDFs into documents."""
    documents = []
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    for uploaded_file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_pdf_path = temp_file.name

        loader = PyPDFLoader(temp_pdf_path)
        docs = loader.load()
        documents.extend(docs)
    
    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=400)
    splits = text_splitter.split_documents(documents)
    
    # Create embeddings and vectorstore
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
    
    # Return both vectorstore and retriever
    retriever = vectorstore.as_retriever()
    return retriever
