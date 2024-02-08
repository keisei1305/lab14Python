#!/usr/bin/env python3
import DBModule
import cgi
from form_handler import show_header
from form_handler import show_end


def create_html_forms(db, table_name, record):
    form = f"<form action = update.py>\n"
    columns = db.get_columns(table_name)
    for i in range(1, len(columns)):
        form+=(f"<div><input type='text' name='val{i-1}' value='{record[i]}'>"
               f"\n<label>{columns[i]}</label></div>\n")
    return f"{form}<input type = 'submit' value='Изменить'/><input style='display:none' type ='text' name = 'table_name' value ='{table_name}'><input style='display:none' type ='text' name = 'id' value ='{record[0]}'></form>"


path= 'C:\\Users\\admin\\Desktop\\PythonReports\\MyDataBase.db'
db = DBModule.DB(path)
form = cgi.FieldStorage()
info = form.getvalue("record")
info = info.split(';')
id = info[0]
table_name = info[1]
print("<br>")
record = db.get_one_record(table_name, id)
text = create_html_forms(db, table_name, record)
print(text)