#!/usr/bin/env python3
import cgi
import DBModule
from form_handler import show_header
from form_handler import show_end


path = "C:\\Users\\admin\\Desktop\\PythonReports\\MyDataBase.db"
db =DBModule.DB(path)
form = cgi.FieldStorage()
table_name = form.getvalue('table_name', '')
count = len(db.get_columns(table_name))
record = []
for i in range(count):
    record.append(form.getvalue(f'val{i}', ''))
print("<br>")
try:
    db.append_or_insert(table_name, tuple(record))
    db.save_changes()
    message = "Успех"
except Exception:
    message = "Ошибка"
finally:
    print(f"""<p>{message}</p>""")