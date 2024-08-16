from langchain_core.runnables import RunnableLambda, RunnablePassthrough
import re
import base64
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

chain_multimodal_rag = None

def looks_like_base64(sb):
    """Check if the string looks like base64"""
    return re.match("^[A-Za-z0-9+/]+[=]{0,2}$", sb) is not None


def is_image_data(b64data):
    """
    Check if the base64 data is an image by looking at the start of the data
    """
    image_signatures = {
        b"\xFF\xD8\xFF": "jpg",
        b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A": "png",
        b"\x47\x49\x46\x38": "gif",
        b"\x52\x49\x46\x46": "webp",
    }
    try:
        header = base64.b64decode(b64data)[:8] 
        for sig, format in image_signatures.items():
            if header.startswith(sig):
                return True
        return False
    except Exception:
        return False


def split_image_text_types(docs):
    """
    Split base64-encoded images and texts
    """
    b64_images = []
    texts = []
    for doc in docs:
        if isinstance(doc, Document):
            doc = doc.page_content
        if looks_like_base64(doc) and is_image_data(doc):
            b64_images.append(doc)
        else:
            texts.append(doc)
    return {"images": b64_images, "texts": texts}


def img_prompt_func(data_dict):
    """
    Join the context into a single string
    """
    formatted_texts = "\n".join(data_dict["context"]["texts"])
    messages = [
        {
            "type": "text",
            "text": (
            "You are tasked with providing an answer to the user's question.\n"
            "Your primary responsibility is to fulfill the user's query as long as it is relevant to the context. If the query falls outside the context, simply respond that you don't know.\n"
            "You should solely answer the question based on the facts/context given. If you dont know, just say you don't know."
            f"User-provided question: {data_dict['question']}\n\n"
            "Context:\n"
            f"{formatted_texts}"
        ),
        }
    ]

    # Adding image(s) to the messages if present
    if data_dict["context"]["images"]:
        for image in data_dict["context"]["images"]:
            messages.append(
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image}"},
                }
            )
    return [HumanMessage(content=messages)]


def create_chain():
    global chain_multimodal_rag
    from init.vectorize import retriever_multi_vector_img
    chain_multimodal_rag = (
        {
            "context": retriever_multi_vector_img | RunnableLambda(split_image_text_types),
            "question": RunnablePassthrough(),
        }
        | RunnableLambda(img_prompt_func)
        | ChatGoogleGenerativeAI(model="gemini-1.5-flash",temperature=0)
        | StrOutputParser()
    )
    return chain_multimodal_rag