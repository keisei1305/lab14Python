import sqlite3


class DB:
    def __init__(self):
        con = sqlite3.connect('MyDataBase.db')
        self.con = con
        self.cursor = con.cursor()

    def create_tables(self):
        self._create_table_humans()
        self._create_table_customers()
        self._create_table_work_types()
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
    def _create_table_work_types(self):
        return "CREATE TABLE IF NOT EXISTS WorkTypes(id integer PRIMARY KEY AUTOINCREMENT, "\
            "Name text, "\
            "UNIQUE(id));"


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
        return "CREATE TABLE IF NOT EXISTS Commands(id integer PRIMARY KEY AUTOINCREMENT, "\
            "ExecutorID integer NOT NULL, "\
            "FOREIGN KEY (ExecutorID) REFERENCES Executors (id) ON DELETE CASCADE, "\
            "UNIQUE(id));"

    @_add_request_sql
    def _create_table_sessions(self):
        return "CREATE TABLE IF NOT EXISTS Sessions(id integer PRIMARY KEY AUTOINCREMENT, "\
            "CommandID integer NOT NULL, "\
            "TypeWorkID integer NOT NULL, "\
            "OrderID integer NOT NULL, "\
            "FOREIGN KEY (CommandID) REFERENCES Commands (id) ON DELETE CASCADE, " \
            "FOREIGN KEY (TypeWorkID) REFERENCES TypeWorks (id) ON DELETE CASCADE, " \
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

    def add_report(self, status_work, album_id = None, album_name = None, id = None):
        album = self.get_album(album_id)
        cur = None
        if (album == None):
            if (album_name == None):
                album_name = f"album{album_id}"
            album_id = self.add_album(album_name, 0, album_id)
        else:
            album_id = album[0]
        cur = self.cursor.execute('INSERT OR IGNORE INTO Reports(id, Status, AlbumID) VALUES(?, ?, ?'\
                                    'returning id', (id, status_work, album_id))
        id = next(cur)[0]
        return id

    def add_order(self, customer_id, registration_date, price, report_id = None):
        if (report_id == None):
            report_id = self.add_report("Registred")
        cur = self.cursor.execute('INSERT OR IGNORE INTO Orders(CustomerID, RegistrationDate, Price, ReportID)'\
                                    'VALUES (?, ?, ?, ?) returning id', (customer_id, registration_date, price, report_id))
        id = next(cur)[0]
        return id

    def add_command(self, id, customer_id):
        cur = self.cursor.execute('INSERT OR REPLACE INTO Commands(id, ExecutorID) VALUES(?,?) returning id', id, customer_id)
        id = next(cur)[0]
        return id

    def add_work_type(self, name, id = None):
        cur = self.cursor.execute('INSERT OR REPLACE INTO Commands(id, Name) VALUES(?,?) returning id', id, name)
        id = next(cur)[0]
        return id

    def add_session(self, command_id, type_work_id, order_id, id = None):
        cur = self.cursor.execute('INSERT OR REPLACE INTO Commands(id, CommandID, TypeWorkID, OrderID)'\
                                  'VALUES(?, ?, ?, ?) returning id', id, command_id, type_work_id, order_id)
        id = next(cur)[0]
        return id


    def update_album_size(self, id, size):
        self.cursor.execute(f"UPDATE Albums SET size = \"{size}\" where id = \"{id}\"")

    def update_command_executor(self, old_id, new_id):
        self.cursor.execute(f"UPDATE Commands SET id=\"{new_id}\" where id = \"{old_id}\"")

    def update_status_report(self, id, status_work):
        self.cursor.execute(f"UPDATE Commands SET StatusWork=\"{status_work}\" where id =\"{id}\"")

    def get_all_media_by_id(self, album_id):
        cur = self.cursor.execute(f"SELECT * FROM Media WHERE id = \"{album_id}\"")
        return cur.fetchall()

    def get_all_media_by_type_media(self, type_media):
        cur = self.cursor.execute(f"SELECT * FROM Media WHERE Type = \"{type_media}\"")
        return cur.fetchall()

    def get_album(self, album_id):
        cur = self.cursor.execute(f"SELECT * FROM Albums WHERE id = \"{album_id}\"")
        return cur.fetchone()

    def get_all_orders_id(self):
        cur = self.cursor.execute(f"SELECT * FROM Orders")
        return cur.fetchall()

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

    def remove_one_media_from_album(self, media_id):
        cur = self.cursor.execute(f"SELECT id, Type, Size, Name, AlbumID From Media WHERE id =\"{media_id}\"")
        media = cur.fetchone()
        media_size = media[2]
        album_id = media[4]
        album_size = self.get_album(album_id)[2]
        cur = self.cursor.execute(f"DELETE From Media Where id = \"{media_id}\"")
        self.update_album_size(album_id, album_size - media_size)
        return media

    def save_changes(self):
        self.con.commit()

    def drop_tables(self):
        self.manual_request("DROP TABLE IF EXISTS Albums;")
        self.manual_request("DROP TABLE IF EXISTS Media;")
        self.manual_request("DROP TABLE IF EXISTS Sessions")
        self.manual_request("DROP TABLE IF EXISTS WorkTypes")
        self.manual_request("DROP TABLE IF EXISTS Commands")
        self.manual_request("DROP TABLE IF EXISTS Executors")
        self.manual_request("DROP TABLE IF EXISTS Orders")
        self.manual_request("DROP TABLE IF EXISTS Reports")
        self.manual_request("DROP TABLE IF EXISTS Customers")
        self.manual_request("DROP TABLE IF EXISTS Humans")

    def clear_tables(self):
        self.manual_request("DELETE FROM Albums;")
        self.manual_request("DELETE FROM Media;")
        self.manual_request("DELETE FROM Sessions")
        self.manual_request("DELETE FROM WorkTypes")
        self.manual_request("DELETE FROM Commands")
        self.manual_request("DELETE FROM Executors")
        self.manual_request("DELETE FROM Orders")
        self.manual_request("DELETE FROM Reports")
        self.manual_request("DELETE FROM Customers")
        self.manual_request("DELETE FROM Humans")