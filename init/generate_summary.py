import os
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from init.extract_doc import tab
from langchain_google_genai import GoogleGenerativeAI,ChatGoogleGenerativeAI
import base64
from langchain_core.messages import HumanMessage
import time

load_dotenv()

def encode_image(image_path):
    """Getting the base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
def image_summarize(img_base64, prompt):
    """Make image summary"""
    chat =ChatGoogleGenerativeAI(model="gemini-1.5-flash",temperature=0)

    msg = chat.invoke(
        [
            HumanMessage(
                content=[
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"},
                    },
                ]
            )
        ]
    )
    return msg.content


def generate_img_summaries(path):
    """
    Generate summaries and base64 encoded strings for images
    path: Path to list of .jpg files extracted by Unstructured
    """

    image_summaries = []

    prompt = """You are an assistant tasked with summarizing images for retrieval. \
    These summaries will be embedded and used to retrieve the raw image. \
    Give a concise summary of the image that is well optimized for retrieval."""

    for img_file in sorted(os.listdir(path)):
        if img_file.endswith(".jpg"):
            img_path = os.path.join(path, img_file)
            base64_image = encode_image(img_path)
            image_summaries.append(image_summarize(base64_image, prompt))
            time.sleep(3)

    return image_summaries

def get_summaries_all():
    
    prompt_text = """You are an assistant tasked with summarizing tables for retrieval. \
        These summaries will be embedded and used to retrieve the raw table elements. \
        Explain and give a summary of the table that is well optimized for retrieval. Table {element} """
        
    prompt = PromptTemplate(template=prompt_text, input_variables=["element"])
    summarize_chain = {"element": lambda x: x} | prompt | GoogleGenerativeAI(model="models/text-bison-001", temperature=0) | StrOutputParser()
    print("Sumarizing table data...")
    table_summaries = summarize_chain.batch(tab,{"max_concurrency": 9})
    print("Sumarizing image data...")
    image_summaries = generate_img_summaries("./extracted_data")
    return table_summaries,image_summaries

    
        
        
    
    
