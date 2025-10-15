import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase

load_dotenv()

engine = create_engine("sqlite:///SQLDatabase/sql_database.db")
sql_database = SQLDatabase(engine=engine)