import sqlite3


class DB:
    def __init__(self):
        con = sqlite3.connect('MyDataBase.db')
        self.con = con

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

    def _add_create_table(func):
        def wrapper(self):
            cursor_obj = self.con.cursor()
            cursor_obj.execute(func(self))
            self.con.commit()
        return wrapper

    @_add_create_table
    def _create_table_humans(self):
        return "CREATE TABLE IF NOT EXISTS Humans(id integer PRIMARY KEY AUTOINCREMENT, "\
            "FirstName text NOT NULL, "\
            "LastName text NOT NULL, "\
            "PhoneNumber text NOT NULL, "\
            "Gender text);"

    @_add_create_table
    def _create_table_executors(self):
        return "CREATE TABLE IF NOT EXISTS Executors(id integer PRIMARY KEY AUTOINCREMENT,"\
            "HumanDataID integer NOT NULL, "\
            "AvailableTypeWork NOT NULL, "\
            "FOREIGN KEY (AvailableTypeWork) REFERENCES WorkTypes (id) ON DELETE CASCADE, "\
            "FOREIGN KEY (HumanDataID) REFERENCES Humans (id) ON DELETE CASCADE);"

    @_add_create_table
    def _create_table_customers(self):
        return "CREATE TABLE IF NOT EXISTS Customers(id integer PRIMARY KEY AUTOINCREMENT,"\
            "HumanDataID integer NOT NULL, "\
            "Status text, "\
            "FOREIGN KEY (HumanDataID) REFERENCES Humans (id) ON DELETE CASCADE);"

    @_add_create_table
    def _create_table_work_types(self):
        return "CREATE TABLE IF NOT EXISTS WorkTypes(id integer PRIMARY KEY AUTOINCREMENT, "\
            "Name text);"\


    @_add_create_table
    def _create_table_albums(self):
        return "CREATE TABLE IF NOT EXISTS Albums(id integer PRIMARY KEY AUTOINCREMENT,"\
            "Name text, "\
            "Size integer);"

    @_add_create_table
    def _create_table_media(self):
        return "CREATE TABLE IF NOT EXISTS Media(id integer PRIMARY KEY AUTOINCREMENT,"\
            "Type text, "\
            "Size integer, "\
            "Name text, "\
            "AlbumID integer, "\
            "FOREIGN KEY (AlbumID) REFERENCES Albums (id) ON DELETE CASCADE);"

    @_add_create_table
    def _create_table_reports(self):
        return "CREATE TABLE IF NOT EXISTS Reports(id integer PRIMARY KEY AUTOINCREMENT,"\
            "StatusWork text, "\
            "AlbumID integer, " \
            "FOREIGN KEY (AlbumID) REFERENCES Albums (id) ON DELETE CASCADE);"

    @_add_create_table
    def _create_table_orders(self):
        return "CREATE TABLE IF NOT EXISTS Orders(id integer PRIMARY KEY AUTOINCREMENT,"\
            "CustomerID integer, "\
            "RegistrationDate date, "\
            "Price integer, "\
            "ReportID integer, "\
            "FOREIGN KEY (ReportID) REFERENCES Reports (id) ON DELETE CASCADE, "\
            "FOREIGN KEY (CustomerID) REFERENCES Customers (id) ON DELETE CASCADE);"

    @_add_create_table
    def _create_table_commands(self):
        return "CREATE TABLE IF NOT EXISTS Commands(id integer PRIMARY KEY AUTOINCREMENT, "\
            "ExecutorID integer, "\
            "FOREIGN KEY (ExecutorID) REFERENCES Executors (id) ON DELETE CASCADE);"

    @_add_create_table
    def _create_table_sessions(self):
        return "CREATE TABLE IF NOT EXISTS Sessions(id integer PRIMARY KEY AUTOINCREMENT, "\
            "CommandID integer, "\
            "TypeWorkID integer, "\
            "OrderID integer, "\
            "FOREIGN KEY (CommandID) REFERENCES Commands (id) ON DELETE CASCADE, " \
            "FOREIGN KEY (TypeWorkID) REFERENCES TypeWorks (id) ON DELETE CASCADE, " \
            "FOREIGN KEY (OrderID) REFERENCES Orders (id) ON DELETE CASCADE);"