import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_USERNAME = os.getenv('DATABASE_USERNAME', 'postgres')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'postgres')
DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
DATABASE_PORT = os.getenv('DATABASE_PORT', 5432)
DATABASE_DBNAME = os.getenv('DATABASE_DBNAME', 'task_manager')
DATABASE_URL = (f"postgresql://{DATABASE_USERNAME}:"
                f"{DATABASE_PASSWORD}@{DATABASE_HOST}:"
                f"{DATABASE_PORT}/{DATABASE_DBNAME}")

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 30
TEST_DATABASE_URL = 'sqlite:///:memory:'
SENTRY_DSN = os.getenv('SENTRY_DSN')
SENTRY_ENVIRONMENT = os.getenv('SENTRY_ENVIRONMENT')

PROFILING = os.getenv('PROFILING')
PROFILE_DIR = "profiles"
