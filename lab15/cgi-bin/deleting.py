#!/usr/bin/env python3
import DBModule
import cgi
from form_handler import show_header
from form_handler import show_end


path = "C:\\Users\\admin\\Desktop\\PythonReports\\MyDataBase.db"
db =DBModule.DB(path)
form = cgi.FieldStorage()
info = form.getvalue("record")
id = form.getvalue('id')
info = info.split(';')
id = info[0]
table_name = info[1]

print("<br>")
try:
    db.remove_one_record(table_name, id)
    db.save_changes()
    message = "Успех"
except Exception:
    message = "Ошибка"
finally:
    print(f"""<p>{message}</p>""")