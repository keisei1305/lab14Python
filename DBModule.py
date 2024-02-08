import sqlite3


class DB:
    def __init__(self, path):
        con = sqlite3.connect(path)
        self.con = con
        self.cursor = con.cursor()

    def create_tables(self):
        self._create_table_humans()
        self._create_table_customers()
        self._create_table_executor_command()
        self._create_table_executors()
        self._create_table_commands()
        self._create_table_albums()
        self._create_table_media()
        self._create_table_reports()
        self._create_table_orders()
        self._create_table_sessions()

    def close_db(self):
        self.con.close()

    def _add_request_sql(func):
        def wrapper(self, *args, **kwargs):
            cursor_obj = self.con.cursor()
            cursor_obj.execute(func(self, *args, **kwargs))
            self.con.commit()
        return wrapper

    @_add_request_sql
    def _create_table_humans(self):
        return "CREATE TABLE IF NOT EXISTS Humans(id integer PRIMARY KEY AUTOINCREMENT, "\
            "FirstName text NOT NULL, "\
            "LastName text NOT NULL, "\
            "PhoneNumber text NOT NULL, "\
            "Gender text, "\
            "UNIQUE(id));"

    @_add_request_sql
    def _create_table_executors(self):
        return "CREATE TABLE IF NOT EXISTS Executors(id integer PRIMARY KEY AUTOINCREMENT,"\
            "HumanID integer NOT NULL, "\
            "UNIQUE(id));"

    @_add_request_sql
    def _create_table_customers(self):
        return "CREATE TABLE IF NOT EXISTS Customers(id integer PRIMARY KEY AUTOINCREMENT,"\
            "HumanID integer NOT NULL, "\
            "Status text, "\
            "FOREIGN KEY (HumanID) REFERENCES Humans (id) ON DELETE CASCADE, "\
            "UNIQUE(id, HumanID));"

    @_add_request_sql
    def _create_table_executor_command(self):
        return "CREATE TABLE IF NOT EXISTS ExecutorCommand(ExecutorID integer NOT NULL, "\
            "CommandID NOT NULL, "\
            "FOREIGN KEY (CommandID) REFERENCES Commands (id) ON DELETE CASCADE, "\
            "FOREIGN KEY (ExecutorID) REFERENCES Executors (id) ON DELETE CASCADE, "\
            "PRIMARY KEY(ExecutorID, CommandID));"

    @_add_request_sql
    def _create_table_albums(self):
        return "CREATE TABLE IF NOT EXISTS Albums(id integer PRIMARY KEY AUTOINCREMENT,"\
            "Name text, "\
            "Size integer, "\
            "UNIQUE(id));"

    @_add_request_sql
    def _create_table_media(self):
        return "CREATE TABLE IF NOT EXISTS Media(id integer PRIMARY KEY AUTOINCREMENT,"\
            "Type text, "\
            "Size integer, "\
            "Name text, "\
            "AlbumID integer NOT NULL, "\
            "FOREIGN KEY (AlbumID) REFERENCES Albums (id) ON DELETE CASCADE, " \
            "UNIQUE(id));"

    @_add_request_sql
    def _create_table_reports(self):
        return "CREATE TABLE IF NOT EXISTS Reports(id integer PRIMARY KEY AUTOINCREMENT,"\
            "StatusWork text, "\
            "AlbumID integer NOT NULL, " \
            "FOREIGN KEY (AlbumID) REFERENCES Albums (id) ON DELETE CASCADE, " \
            "UNIQUE(id));"


    @_add_request_sql
    def _create_table_orders(self):
        return "CREATE TABLE IF NOT EXISTS Orders(id integer PRIMARY KEY AUTOINCREMENT,"\
            "CustomerID integer NOT NULL, "\
            "RegistrationDate date, "\
            "Price integer, "\
            "ReportID integer NOT NULL, "\
            "FOREIGN KEY (ReportID) REFERENCES Reports (id) ON DELETE CASCADE, "\
            "FOREIGN KEY (CustomerID) REFERENCES Customers (id) ON DELETE CASCADE, "\
            "UNIQUE(id, ReportID));"

    @_add_request_sql
    def _create_table_commands(self):
        return "CREATE TABLE IF NOT EXISTS Commands(id integer PRIMARY KEY, "\
            "Name text);"

    @_add_request_sql
    def _create_table_sessions(self):
        return "CREATE TABLE IF NOT EXISTS Sessions(id integer PRIMARY KEY AUTOINCREMENT, "\
            "CommandID integer NOT NULL, "\
            "TypeWork text NOT NULL, "\
            "OrderID integer NOT NULL, "\
            "FOREIGN KEY (CommandID) REFERENCES Commands (id) ON DELETE CASCADE, " \
            "FOREIGN KEY (OrderID) REFERENCES Orders (id) ON DELETE CASCADE, "\
            "UNIQUE(id));"

    @_add_request_sql
    def manual_request(self, request):
        return request

    def add_human(self, first_name, last_name, phone_number, gender):
        entity = (first_name, last_name, phone_number, gender)
        cur = self.cursor.execute('INSERT OR IGNORE INTO Humans(FirstName, LastName, PhoneNumber, Gender)' \
                                  'VALUES (?,?,?,?) returning id', entity)
        id = next(cur)[0]
        return id

    def add_customer(self, first_name, last_name, phone_number, gender, status=None):
        human_id = self.add_human(first_name, last_name, phone_number, gender)
        entity = (human_id, status)
        cur = self.cursor.execute('INSERT OR REPLACE INTO Customers(HumanID, Status) VALUES (?, ?)'\
                                  'returning id', entity)
        id = next(cur)[0]
        return id

    def add_executor(self, first_name, last_name, phone_number, gender):
        human_id = self.add_human(first_name, last_name, phone_number, gender)
        cur = self.cursor.execute(f"INSERT OR REPLACE INTO Executors(HumanID) VALUES (\"{human_id}\")"\
                                  'returning id')
        id = next(cur)[0]
        return id

    def add_album(self, name, size, id = None):
        cur = self.cursor.execute('INSERT OR REPLACE INTO Albums(Name, Size, id) VALUES (?, ?, ?)'\
                                  'returning id', (name, size, id))
        id = next(cur)[0]
        return id

    def add_media(self, type, size, name, album_id = None, album_name = None):
        album = self.get_album(album_id)
        if (album != None):
            self.update_album_size(album_id, album[2]+size)
        else:
            if (album_name == None):
                 album_name = name
            album_id = self.add_album(album_name, size, album_id)
        cur = self.cursor.execute('INSERT OR REPLACE INTO Media(Type, Size, Name, AlbumID) VALUES(?, ?, ?, ?)'\
                                  'returning id', (type, size, name, album_id))
        id = next(cur)[0]
        return id

    def add_report(self, status_work, album_id=None, album_name=None, id=None):
        album = self.get_album(album_id)
        cur = None
        if (album == None):
            if (album_name == None):
                album_name = f"album{album_id}"
            album_id = self.add_album(album_name, 0, album_id)
        else:
            album_id = album[0]
        cur = self.cursor.execute('INSERT OR IGNORE INTO Reports(id, StatusWork, AlbumID) VALUES(?, ?, ?)'\
                                    'returning id', (id, status_work, album_id))
        id = next(cur)[0]
        return id

    def add_order(self, customer_id, registration_date, price, report_id = None):
        if (report_id == None):
            report_id = self.add_report("Запланировано")
        cur = self.cursor.execute('INSERT OR IGNORE INTO Orders(CustomerID, RegistrationDate, Price, ReportID)'\
                                    'VALUES (?, ?, ?, ?) returning id', (customer_id, registration_date, price, report_id))
        id = next(cur)[0]
        return id

    def add_command(self, name):
        cur = self.cursor.execute(f'INSERT OR REPLACE INTO Commands(Name) VALUES(\"{name}\") returning id')
        id = next(cur)[0]
        return id

    def add_session(self, command_id, type_work, order_id, id = None):
        cur = self.cursor.execute('INSERT OR REPLACE INTO Sessions(id, CommandID, TypeWork, OrderID)'\
                                  'VALUES(?, ?, ?, ?) returning id', (id, command_id, type_work, order_id))
        id = next(cur)[0]
        return id

    def add_executor_command(self, executor_id, command_id):
        cur = self.cursor.execute('INSERT OR REPLACE INTO ExecutorCommand(ExecutorID, CommandID)'\
                                  'VALUES(?, ?)', (executor_id, command_id))

    def update_album_size(self, id, size):
        self.cursor.execute(f"UPDATE Albums SET size = \"{size}\" where id = \"{id}\"")

    def update_status_report(self, id, status_work):
        self.cursor.execute(f"UPDATE Commands SET StatusWork=\"{status_work}\" where id =\"{id}\"")

    def get_all_executors_in_command(self, command_id):
        cur = self.cursor.execute("SELECT Commands.Name, Humans.FirstName, Humans.LastName "\
                            "FROM ExecutorCommand "\
                            "JOIN Executors ON Executors.id=ExecutorCommand.ExecutorID "\
                            "JOIN Humans ON Humans.id=Executors.HumanID "\
                            "JOIN Commands ON CommandID=Commands.id "\
                            f"WHERE Commands.id = \"{command_id}\"")
        return cur.fetchall()

    def get_all_executors(self):
        cur = self.cursor.execute("SELECT FirstName, LastName, PhoneNumber FROM Executors, Humans Where Executors.HumanID=Humans.id")
        return cur.fetchall()

    def get_all_customers(self):
        cur = self.cursor.execute("SELECT FirstName, LastName, PhoneNumber, Status FROM Customers, Humans Where Customers.HumanID=Humans.id")
        return cur.fetchall()

    def get_all_id_executors(self):
        cur = self.cursor.execute("SELECT id FROM Executors")
        all_id = cur.fetchall()
        return list(map(sum, all_id))

    def get_all_id_customers(self):
        cur = self.cursor.execute("SELECT id FROM Customers")
        all_id = cur.fetchall()
        return list(map(sum, all_id))

    def get_all_id_commands_without_sessions(self):
        cur = self.cursor.execute("SELECT id FROM Commands "\
                                  "EXCEPT SELECT Commands.id FROM Commands, Sessions WHERE Commands.id = Sessions.CommandID")
        all_id = cur.fetchall()
        return list(map(sum, all_id))

    def get_count_commands_without_sessions(self):
        cur = self.cursor.execute("SELECT COUNT(*) FROM (SELECT id FROM Commands EXCEPT SELECT COMMANDS.id FROM Commands, Sessions "\
                                  "WHERE Commands.id = Sessions.CommandID)")
        return cur.fetchone()[0]

    def get_all_media_by_id(self, album_id):
        cur = self.cursor.execute(f"SELECT * FROM Media WHERE id = \"{album_id}\"")
        return cur.fetchall()

    def get_all_media_by_type_media(self, type_media):
        cur = self.cursor.execute(f"SELECT * FROM Media WHERE Type = \"{type_media}\"")
        return cur.fetchall()

    def get_album(self, album_id):
        cur = self.cursor.execute(f"SELECT * FROM Albums WHERE id = \"{album_id}\"")
        return cur.fetchone()

    def get_all_id_orders(self):
        cur = self.cursor.execute(f"SELECT id FROM Orders")
        all_id = cur.fetchall()
        return list(map(sum, all_id))

    def get_all_orders_by_date(self, date):
        cur = self.cursor.execute(f"SELECT id, CustomerID, ReportID FROM Orders WHERE date = \"{date}\"")
        return cur.fetchall()

    def get_report_by_order_id(self, order_id):
        cur = self. cursor.execute(f"SELECT * From Reports WHERE id = \"{order_id}\"")
        return cur.fetchone()

    def get_all_orders_by_status_work(self, status_work):
        cur = self.cursor.execute(f"SELECT Orders.id, Reports.StatusWork, Orders.RegistrationDate FROM Reports, Orders "
                                  f"Where Orders.ReportID = Reports.id and Reports.StatusWork = \"{status_work}\"")
        return cur.fetchall()

    def get_all_orders_by_customer(self, customer_id):
        cur = self.cursor.execute(f"SELECT Humans.FirstName, Humans.LastName, Reports.StatusWork, Orders.RegistrationDate, Orders.Price "
                                  f"FROM Reports, Orders, Customers, Humans "
                                  f"Where Orders.ReportID = Reports.id "
                                  f"and Customers.HumanID = Humans.id "
                                  f"and Orders.CustomerID = \"{customer_id}\" "
                                  f"and Orders.CustomerID = Customers.id")
        return cur.fetchall()

    def get_all_rows(self, table_name):
        cur = self.cursor.execute(f"SELECT * FROM {table_name}")
        return cur.fetchall()

    def remove_one_media_from_album(self, media_id):
        cur = self.cursor.execute(f"SELECT id, Type, Size, Name, AlbumID From Media WHERE id =\"{media_id}\"")
        media = cur.fetchone()
        media_size = media[2]
        album_id = media[4]
        album_size = self.get_album(album_id)[2]
        cur = self.cursor.execute(f"DELETE From Media Where id = \"{media_id}\"")
        self.update_album_size(album_id, album_size - media_size)
        return media

    def remove_one_record(self, table_name, id_record):
        self.cursor.execute(f"DELETE FROM {table_name} Where id = \"{id_record}\"")

    def update_one_record(self, table_name, attribute_name, new_value, id_record):
        self.cursor.execute(f"UPDATE {table_name} SET {attribute_name} = \"{new_value}\" Where id = \"{id}\"")

    def append_or_insert(self, table_name, record):
        columns = self.get_columns(table_name)
        voprosy = ["?"]*len(record)
        self.cursor.execute(f"INSERT OR REPLACE INTO {table_name} ({','.join(columns)}) VALUES({','.join(voprosy)})", record)

    def get_one_record(self, table_name, id):
        cur = self.cursor.execute(f"SELECT * FROM '{table_name}' WHERE id = {id}")
        return cur.fetchone()

    def save_changes(self):
        self.con.commit()

    def get_columns(self, table_name):
        cur = self.cursor.execute(f"SELECT name FROM PRAGMA_TABLE_INFO(\'{table_name}\')")
        all_names = cur.fetchall()
        return list(map(lambda x:x[0], all_names))

    def drop_tables(self):
        self.manual_request("DROP TABLE IF EXISTS Albums;")
        self.manual_request("DROP TABLE IF EXISTS Media;")
        self.manual_request("DROP TABLE IF EXISTS ExecutorCommand")
        self.manual_request("DROP TABLE IF EXISTS Sessions")
        self.manual_request("DROP TABLE IF EXISTS Commands")
        self.manual_request("DROP TABLE IF EXISTS Executors")
        self.manual_request("DROP TABLE IF EXISTS Orders")
        self.manual_request("DROP TABLE IF EXISTS Reports")
        self.manual_request("DROP TABLE IF EXISTS Customers")
        self.manual_request("DROP TABLE IF EXISTS Humans")

    def clear_tables(self):
        self.manual_request("DELETE FROM Albums;")
        self.manual_request("DELETE FROM Media;")
        self.manual_request("DELETE FROM ExecutorCommand")
        self.manual_request("DELETE FROM Sessions")
        self.manual_request("DELETE FROM Commands")
        self.manual_request("DELETE FROM Executors")
        self.manual_request("DELETE FROM Orders")
        self.manual_request("DELETE FROM Reports")
        self.manual_request("DELETE FROM Customers")
        self.manual_request("DELETE FROM Humans")