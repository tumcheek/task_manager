from core.config import SESSION


def get_db():
    db = SESSION()
    try:
        yield db
    finally:
        db.close()
