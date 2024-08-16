from sqlalchemy.orm.session import Session
from fastapi import Depends
from db.database import get_db
from init.generate_summary import get_summaries_all
from init.extract_doc import tab,NarrativeText
from db.models import ImageSummary,TableDocs,TableSummary,TextDocs

def upload_to_db(db:Session = Depends(get_db)):
    table_summaries,image_summaries = get_summaries_all()
    summary_entry = None
    doc_entry = None
    print(len(table_summaries))
    for summary in image_summaries + table_summaries:
        if summary in image_summaries:
            summary_entry = ImageSummary(summary=summary)
        else:
            summary_entry = TableSummary(summary=summary)
        db.add(summary_entry)
        
    for doc in tab + NarrativeText:
        if doc in tab:
            doc_entry = TableDocs(docs=doc)
        else:
            doc_entry = TextDocs(docs=doc)
        db.add(doc_entry)
    db.commit()