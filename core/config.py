from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_USERNAME = 'postgres'
DATABASE_PASSWORD = '111111'
DATABASE_HOST = 'localhost'
DATABASE_PORT = '5432'
DATABASE_DBNAME = 'task_manager'
DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DBNAME}"

ENGINE = create_engine(DATABASE_URL)

SESSION = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)

# TODO: use env variables in alembic.ini for db connection

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
