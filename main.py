import DBModule

db = DBModule.DB()
try:
    db.create_tables()
except Exception:
    print(Exception.__name__)