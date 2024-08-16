from fastapi import APIRouter
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from fastapi.websockets import WebSocket,WebSocketDisconnect
from schema import Conversation,Message
from datetime import datetime
from config.database import collection_name
load_dotenv()
router = APIRouter(
    prefix = "/chatbot",
    tags=["chatbot"]
)

@router.websocket("/chat")
async def streaming_chatbot(websocket: WebSocket):
    from init.create_chain import chain_multimodal_rag,split_image_text_types
    from init.vectorize import retriever_multi_vector_img
    
    await websocket.accept()
    conversation = Conversation(user_id="", messages=[])
    
    try:
        while True:
            data = await websocket.receive_json()
            message = data.get("message", "")
            # Check if there's an image to process
            if 'image' in data:
                image_data = data['image']
                llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
                response = llm.invoke(
                    [
                        HumanMessage(
                            content=[
                                {
                                    "type": "text",
                                    "text": f"""
                                    
                                        Generate a detailed context based on the images provided by the user. 
                                        The context should be clear and relevant to the user's query, 
                                        which will be passed to another LLM for retrieval purposes. 
                                        Craft a concise query and context that accurately reflects the user's input and the content of the images, 
                                        ensuring optimal results in the subsequent retrieval process.

                                        User's query: {message}
                                    """,   
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
                                },
                            ]
                        )
                    ]
                )
                message = response.content
            
            print(message)
            if message:
                conversation.messages.append(Message(
                    role="user",
                    content=message,
                    timestamp=datetime.now()
                ))

                full_response = ""
                
                for chunk in chain_multimodal_rag.stream(message):
                    await websocket.send_json({"text": chunk})
                    full_response += chunk
                
                conversation.messages.append(Message(
                    role="assistant",
                    content=full_response,
                    timestamp=datetime.now()
                ))
                
                docs = retriever_multi_vector_img.get_relevant_documents(message, limit=10)
                source_docs = split_image_text_types(docs)
                
                # Send images one by one
                for image in source_docs["images"]:
                    print(len(source_docs["images"]))
                    await websocket.send_json({"images": [image]})
    
    except WebSocketDisconnect:
        print("Client disconnected")
    
    finally:
        conversation_dict = conversation.to_dict()
        collection_name.insert_one(conversation_dict)