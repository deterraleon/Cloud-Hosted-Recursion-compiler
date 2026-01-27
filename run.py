import sqlite3
from dotenv import load_dotenv
import os
from compile import unprocess
from variable_functions import save_variable, get_variable
con = sqlite3.connect(os.getenv("DB_NAME")) 
cur = con.cursor()
program = os.getenv("PROGRAM_NAME")
variables = os.getenv("VARIABLES_NAME")
cur.execute(f"DELETE FROM {variables}")
con.commit()
cur.execute(f"SELECT program FROM {program} WHERE name = 'main'")
exec(unprocess(cur.fetchone()[0]))