#!/usr/bin/env python3
import DBModule
import cgi
def create_html_table(db, table_name):
    table_head = f"<thead>\n<tr><th>{'</th><th>'.join(db.get_columns(table_name))}</th></tr>\n</thead>"
    records = db.get_all_rows(table_name)
    table_body = "\n<tbody>\n"
    for record in records:
        record = tuple(map(str, record))
        table_body += f"<tr><td>{'</td><td>'.join(record)}</td></tr>\n"
    return f"<table>\n{table_head}{table_body}</table>"


def create_html_forms(db, table_name):
    form = f"<form action = adding.py>\n"
    columns = db.get_columns(table_name)
    for i in range(len(columns)):
        form+=(f"<div><input type='text' name='val{i}'></input>"
               f"\n<label>{columns[i]}</label></div>")
    return f"{form}<input type = 'submit' /></form>"



def show_html(html_text):
    print(html_text)


def show_header():
    print("Content-type: text/html\n")
    print("""<!DOCTYPE HTML>
    <html>
    <head>
    <meta charset = "utf-8"/>
    <title> Обработка данных форм</title>
    </head>
    <body>
    <a href="http://localhost:8000">Вернуться</a>
    """)


def show_end():
    print("""</body></html>""")


path = 'C:\\Users\\admin\\Desktop\\PythonReports\\MyDataBase.db'
db = DBModule.DB(path)
form = cgi.FieldStorage()
table_name = form.getvalue("table_name", "Humans")
action_name = form.getvalue("action_name", "")
show_header()
if (action_name=="Show"):
    show_html(create_html_table(db, table_name))
elif (action_name=="Append"):
    show_html(create_html_forms(db, table_name))


show_end()
