import sqlite3
from dotenv import load_dotenv
import os

def get_con():
    con = sqlite3.connect(os.getenv("DB_NAME")) 
    return con