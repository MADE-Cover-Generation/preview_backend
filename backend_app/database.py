import os

from dotenv import load_dotenv

import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm

load_dotenv()

USERNAME = os.getenv('postgre_user')
PASSWORD = os.getenv('postgre_password')
DATABASE_NAME = os.getenv('postgre_database')

DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@postgres/{DATABASE_NAME}"

engine = _sql.create_engine(DATABASE_URL)

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = _declarative.declarative_base()



