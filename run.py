from dotenv import load_dotenv
import os
from compile import unprocess
from variable_functions import save_variable, get_variable
from sqlite_functions import get_con
con = get_con()
cur = con.cursor()
program = os.getenv("PROGRAM_NAME")
variables = os.getenv("VARIABLES_NAME")
cur.execute(f"DELETE FROM {variables}")
con.commit()
cur.execute(f"SELECT program FROM {program} WHERE name = 'main'")
exec(unprocess(cur.fetchone()[0]))