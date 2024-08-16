from db.database import Base
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import String,Integer

class ImageSummary(Base):
    __tablename__ = "ImageSummary"
    id = Column(Integer,primary_key=True,index=True)
    summary = Column(String)


class TableSummary(Base):
    __tablename__ = "TableSummary"
    id = Column(Integer,primary_key=True,index=True)
    summary = Column(String)
    
class TableDocs(Base):
    __tablename__ = "TableDocs"
    id = Column(Integer,primary_key=True,index=True)
    docs = Column(String)
    
class TextDocs(Base):
    __tablename__ = "TextDocs"
    id = Column(Integer,primary_key=True,index=True)
    docs = Column(String)