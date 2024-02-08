import random
import DBModule
from lab14.generator import Generator


def create_customers(count):
    customers = []
    for i in range(count):
        customers.append(Generator.generate_customer())
    return customers


def create_executors(count):
    executors = []
    for i in range(count):
        executors.append(Generator.generate_customer())
    return executors


def create_commands(count_commands, mas_of_executors):
    commands = []
    for i in range(count_commands):
        commands.append((Generator.generate_command(), Generator.generate_executors_in_command(mas_of_executors)))
    return commands


def create_media(count_media, album_id):
    media = []
    for i in range(count_media):
        media.append(Generator.generate_media(0, album_id))
    return media


def create_albums(count_albums):
    albums = []
    for i in range(count_albums):
        albums.append(Generator.generate_album(0))
    return albums


def create_reports(count_reports, album_id):
    reports = []
    for i in range(count_reports):
        reports.append(Generator.generate_report(album_id))
    return reports


def create_orders(count_orders, report_id, mas_of_customers):
    orders = []
    for i in range(count_orders):
        orders.append(Generator.generate_order_from_customers(mas_of_customers, report_id))
    return orders


def create_sessions(count_sessions, mas_of_commands, mas_of_orders):
    sessions = []
    for i in range(count_sessions):
        sessions.append(Generator.generate_session(random.choice(mas_of_commands), random.choice(mas_of_orders)))
    return sessions


def append_customers_to_db(database, customers):
    for customer in customers:
        database.add_customer(customer[0], customer[1], customer[2], customer[3], customer[4])


def append_executors_to_db(database, executors):
    for executor in executors:
        database.add_executor(executor[0], executor[1], executor[2], executor[3])


def append_commands_to_db(database, commands):
    for command in commands:
        name = command[0]
        executors = command[1]
        command_id = database.add_command(name)
        for executor in executors:
            database.add_executor_command(executor, command_id)


def append_orders_and_albums_to_db(database, albums):
    customers = database.get_all_id_customers()
    for album in albums:
        album_id = database.add_album(album[0], album[1])
        media = create_media(random.randint(10, 100), album_id)
        for m in media:
            database.add_media(m[0], m[1], m[2], m[3])

        report = create_reports(1, album_id)[0]
        report_id = database.add_report(report[0], report[1])
        order = create_orders(1, report_id, customers)[0]
        database.add_order(order[0], order[1], order[2], order[3])


def append_sessions_to_db(database, count_sessions):
    orders = database.get_all_id_orders()
    for i in range(count_sessions):
        commands_without_sessions = database.get_all_id_commands_without_sessions()
        if len(commands_without_sessions) == 0:
            raise Exception('Not enough space')
        session = create_sessions(1, commands_without_sessions, orders)[0]
        database.add_session(session[0], session[1], session[2])


def create_random_database(database):
    append_customers_to_db(database, create_customers(random.randint(80, 160)))
    append_executors_to_db(database, create_executors(random.randint(30, 50)))
    append_commands_to_db(database, create_commands(random.randint(8, 12), database.get_all_id_executors()))
    append_orders_and_albums_to_db(database, create_albums(random.randint(50, 60)))
    count_available_commands = database.get_count_commands_without_sessions()
    append_sessions_to_db(database, random.randint(4, count_available_commands))

path = 'C:\\Users\\admin\\Desktop\\PythonReports\\MyDataBase.db'
db = DBModule.DB(path)
db.save_changes()