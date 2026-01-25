import sqlite3
from dotenv import load_dotenv
import os

def process(func)->str:
    load_dotenv()
    sp = os.getenv("SP")
    sp1 = os.getenv("SP1")
    func = str(func)
    func = func.replace('"', sp)
    func = func.replace("'", sp1)
    return func

def unprocess(func):
    load_dotenv()
    sp = os.getenv("SP")
    sp1 = os.getenv("SP1")
    func = str(func)
    func = func.replace(sp, '"')
    func = func.replace(sp1, "'")
    return func

def parce_functions(text: list[str]):
    infunc = 0
    functions = []
    main = []
    for line in text:
        if line[:4].count("def") > 0:
            newfunc = [line]
            infunc = 1
            continue
        if infunc:
            if line[0:4] == "    ":
                newfunc.append(line)
            else:
                functions.append(newfunc)
                infunc = ""
                newfunc = []
        if not infunc:
            main.append(line)
    if newfunc != []:
        functions.append(newfunc)
    return [functions, main]

def process_function_initial(text:list[str]):
    global functoreq
    name = ""
    i = 4
    for char in text[0][4:]:
        if char != '(':
            name += char
            i += 1
        else:
            name += "("
            i += 1
            break
    vars = [""]
    read = 1
    for j in range(i, len(text[0])):
        if text[0][j] == " ":
            continue
        if text[0][j] == ",":
            vars.append("")
            read = 1
            continue
        if text[0][j] == ")":
            break
        if text[0][j] == ":":
            read = 0
        if read:
            vars[-1] += text[0][j]
    functoreq[name] = vars
    return name

def get_indent(line):
    output = ""
    for char in line:
        if char == " ":
            output += char
        else:
            break
    return output

def process_function_calls(text:list[str], names):
    global functoreq
    beg = 0
    if text[0].count("def") > 0:
        beg = 1
    newtext = []
    for line in text[beg:]:
        if line.count("[functions[i][0], *process_function_calls(functions[i], names)"):
            pass
        for name in names:
            if line.count(name) > 0:
                inputs = [""]
                write = 0
                for char in line[line.find(name):]:
                    if char == " ":
                        continue
                    if char == ",":
                        inputs.append("")
                        continue
                    if char == ")":
                        break
                    if char == "(":
                        write = 1
                        continue
                    if write:
                        inputs[-1] += char
                reqs = functoreq[name]
                if len(inputs) != len(reqs):
                    raise Exception(f"{len(inputs)} variables recieved, but expected {len(reqs)}")
                indent = get_indent(line)
                for i in range(len(inputs)):
                    newtext.append(f"{indent}save_variable(get_variable('{inputs[i]}'), '{reqs[i]}', 1)\n")
                start = line.find(name)
                line = line[:start] + f"exec({name[:-1]})" + line[start + line[start:].find(")")+1:]
        newtext.append(line)
    return newtext
        

        


load_dotenv()

con = sqlite3.connect(os.getenv("DB_NAME")) 
cur = con.cursor()
program = os.getenv("PROGRAM_NAME")
variables = os.getenv("VARIABLES_NAME")
cur.execute(f"CREATE TABLE IF NOT EXISTS {variables} (name str, value TEXT)")
cur.execute(f"CREATE TABLE IF NOT EXISTS {program} (name, value TEXT)")
with open("input.py", "r") as input:
    text = input.readlines()
    functions, main = parce_functions(text)
    functoreq = {}
    names = []
    for func in functions:
        names.append(process_function_initial(func))
    for i in range(len(functions)):
        functions[i] = [functions[i][0], *process_function_calls(functions[i], names)]
    main = process_function_calls(main, names)
    with open("output.py", "w") as output:
        for func in functions:
            for line in func:
                output.write(line)
            output.write("\n\n")
        for line in main:
            output.write(line)
    