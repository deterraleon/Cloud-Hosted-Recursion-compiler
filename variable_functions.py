import os
import sqlite3
from dotenv import load_dotenv

def process(value)->str:
    load_dotenv()
    sp = os.getenv("SP")
    value = str(value)
    value = value.replace('"', sp)
    value = value.replace("'", sp)
    return value

def unprocess(value:str):
    load_dotenv()
    sp = os.getenv("SP")
    value = str(value)
    value = value.replace(sp, '\"')
    try:
        return eval(value)
    except:
        return value

def new_hash(name:str):
    load_dotenv()
    if name == os.getenv("RECURSION"):
        return hash(name)
    else:
        return hash(name) + get_variable(os.getenv("RECURSION"))

def get_variable(name:str):
    load_dotenv()
    inner_name = new_hash(name)
    con = sqlite3.connect(os.getenv("DB_NAME")) 
    cur = con.cursor()
    program = os.getenv("PROGRAM_NAME")
    variables = os.getenv("VARIABLES_NAME")
    cur.execute(f"SELECT value FROM {variables} WHERE name = '{inner_name}'")
    out = cur.fetchall()
    if len(out) > 1:
        raise Exception(f"2 instances of a variable '{name}'")
    if len(out) == 1:
        out = unprocess(out[0][0])
        return out
    if len(out) == 0:
        if name == os.getenv("RECURSION"):
            save_variable(0, os.getenv("RECURSION"))
            return 0
        raise Exception(f"No such variable as '{name}'")
    

def save_variable(value, name:str):
    load_dotenv()
    inner_name = new_hash(name)
    con = sqlite3.connect(os.getenv("DB_NAME")) 
    cur = con.cursor()
    program = os.getenv("PROGRAM_NAME")
    variables = os.getenv("VARIABLES_NAME")
    cur.execute(f"SELECT value FROM {variables} WHERE name = '{inner_name}'")
    out = cur.fetchall()
    if len(out) > 1:
        raise Exception(f"2 instances of a variable '{name}'")
    if len(out) == 1:
        out = value
        print(f"UPDATE {variables} SET value = '{process(out)}' WHERE name = '{inner_name}'    name={name}")
        cur.execute(f"UPDATE {variables} SET value = '{process(out)}' WHERE name = '{inner_name}'")
        con.commit()
        return
    if len(out) == 0:
        print(f"INSERT INTO {variables} (name, value) VALUES ('{inner_name}', '{process(value)}')    name={name}")
        cur.execute(f"INSERT INTO {variables} (name, value) VALUES ('{inner_name}', '{process(value)}')")
        con.commit()
    return
