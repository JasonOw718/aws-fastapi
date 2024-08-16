from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm.session import Session
from db.database import get_db
from db.models import ImageSummary,TableSummary,TextDocs,TableDocs
from init.extract_doc import extract_doc
import os
from db.database_operation import upload_to_db

router = APIRouter(
    prefix="/initialize",
    tags=["initialization"]
)

img_s = []
tab_s = []
table=[]
text = []
img_base64_list = []

@router.post("/extract_docs")
def extract_docs():
    try:
        extract_doc()
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Extracting document fails")
    return "ok"

@router.post("/store_db")
def store_db(db:Session = Depends(get_db)):
    try:
        upload_to_db(db)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Database storing fail")
    return "ok"

@router.get("/get_summary")
def load_summary(db:Session = Depends(get_db)):
    from init.generate_summary import encode_image
    
    img_obj_list = db.query(ImageSummary).filter().all()
    tab_obj_list = db.query(TableSummary).filter().all()
    t_doc_list = db.query(TableDocs).filter().all()
    text_obj_list = db.query(TextDocs).filter().all()

    
    for obj in img_obj_list:
        img_s.append(obj.summary)
    for obj in tab_obj_list:
        tab_s.append(obj.summary)
    for obj in t_doc_list:
        table.append(obj.docs)
    for obj in text_obj_list:
        text.append(obj.docs)
    
    path = "./extracted_data"
    for img_file in sorted(os.listdir(path)):
        if img_file.endswith(".jpg"):
            img_path = os.path.join(path, img_file)
            base64_image = encode_image(img_path)
            img_base64_list.append(base64_image)
    
    return {
        "Image_Summary":img_s,
        "Table_Summary":tab_s,
        "Table_Document":table,
        "Text_Document":text,
        "Images_list":img_base64_list
    }
    
    
@router.post("/vectorize")
def vectorize():
    from init.vectorize import create_vectorstore
    try:
        create_vectorstore()
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Vectorstore is not created")
    return "ok"
    

@router.post("/create_chain")
def create_chain():
    from init.create_chain import create_chain
    create_chain()
    return "ok"
    