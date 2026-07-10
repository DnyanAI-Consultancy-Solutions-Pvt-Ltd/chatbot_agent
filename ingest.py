# ingest.py
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

URLS = ["https://dnyanai.co.in/"]

def scrape_website(urls):
    documents = []
    for url in urls:
        try:
            print(f"Scraping {url}...")
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            for element in soup(["script", "style", "footer", "nav"]):
                element.decompose()
            text = soup.get_text(separator=" ")
            clean_text = " ".join(text.split())
            documents.append(Document(page_content=clean_text, metadata={"source": url}))
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")
    return documents

if __name__ == "__main__":
    raw_docs = scrape_website(URLS)
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    splits = text_splitter.split_documents(raw_docs)
    print(f"Created {len(splits)} text chunks.")
    
    # Using local, free HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    
    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=embeddings, 
        persist_directory="./database"
    )
    print("Vector database successfully built locally via HuggingFace inside ./database.")