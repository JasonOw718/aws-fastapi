from langchain.storage import InMemoryStore
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
import uuid
from dotenv import load_dotenv
from langchain_community.vectorstores import Qdrant
import os
import qdrant_client
from qdrant_client import models

load_dotenv()
retriever_multi_vector_img = None

def create_vectorstore():
    global retriever_multi_vector_img
    from router.initialize import tab_s,img_s,img_base64_list,text,table
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    client = qdrant_client.QdrantClient(
        os.getenv("QDRANT_HOST"),
        api_key=os.getenv("QDRANT_API_KEY")
    )

    client.recreate_collection(
        collection_name="chatbot",
        vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
    )
    
    vectorstore = Qdrant(
        client=client,
        collection_name="chatbot",
        embeddings=embeddings
    )
    
    docstore = InMemoryStore()
    id_key = "doc_id"
    
    retriever_multi_vector_img = MultiVectorRetriever(
        vectorstore=vectorstore,
        docstore=docstore,
        id_key=id_key,
    )
    
    doc_contents = text + table + img_base64_list
    doc_ids = [str(uuid.uuid4()) for _ in doc_contents]
    summary_docs = [
        Document(page_content=s, metadata={id_key: doc_ids[i]})
        for i, s in enumerate(text + tab_s + img_s)
    ]
    retriever_multi_vector_img.docstore.mset(list(zip(doc_ids, doc_contents)))

    retriever_multi_vector_img.vectorstore.add_documents(summary_docs)