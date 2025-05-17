from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import DATABASE_URL


ENGINE = create_engine(DATABASE_URL, echo=True)
SESSION = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)


def get_db():
    db = SESSION()
    try:
        yield db
    finally:
        db.close()
