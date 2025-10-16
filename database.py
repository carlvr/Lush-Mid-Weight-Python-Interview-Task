from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

# Create an engine
engine = create_engine("sqlite:///tasks.db")

# Define a base class
Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)
