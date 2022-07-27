from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import dotenv_values

config_env = {
    **dotenv_values(".env"),  # load local file development variables
    **os.environ,  # override loaded values with system environment variables
}

DATABASE_URL = config_env["DATABASE_URL"]

engine = create_engine(DATABASE_URL,
                       connect_args={"connect_timeout": 10},
                       pool_size=20, max_overflow=30,
                       pool_recycle=3600, pool_pre_ping=True, pool_timeout=10)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
