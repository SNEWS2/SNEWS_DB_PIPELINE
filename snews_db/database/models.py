from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func

Base = declarative_base()

class Table1(Base):
    __tablename__ = 'table1'

    int_attr = Column(Integer, primary_key=True)
    string_attr = Column(String(50), unique=True, nullable=False)
    longer_attr = Column(String(100), unique=True, nullable=False)
    date_attr = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<Table1(string_attr='{self.username}', longer_attr='{self.email}')>"

class Table2(Base):
    __tablename__ = 'table2'

    id = Column(Integer, primary_key=True)
    int_attr = Column(Integer, nullable=False)
    date_attr = Column(DateTime, default=func.now())
    other_int_attr = Column(Integer)

    def __repr__(self):
        return f"<Table2(date_attr='{self.date_attr}', int_attr={self.int_attr})>"

def create_db_engine(database_url):
    return create_engine(database_url)

def create_session(engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()