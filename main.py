import DBModule

db = DBModule.DB()
try:
    db.create_tables()
except Exception:
    print(Exception.__name__)


n = db.clear_tables()
print(n)
db.save_changes()