import random


def get_random(func):
    def wrapper():
        return random.choice(func())
    return wrapper


class Generator:

    names = ["Евгений", "Егор", "Сергей", "Иван", "Начын", "Кирилл", "Михаил", "Самба"]
    lastnames = ["Татарян", "Парфинцов", "Минкеев", "Петроченко", "Биче-Оол", "Гурин", "Ховенмей", "Ховалыг"]
    genders = ["М", "Ж", "Хеликоптер"]
    customer_statuses = ["Заблокирован", "Постоянный клиент", "Клиент", "Важная персона"]
    work_types = ["Фотография", "Видеография"]
    work_statuses = ["Выполнено", "В работе", "Отложено", "Запланировано", "Заблокировано"]
    media_types = ["Фото", "Видео", "Аудио"]
    album_names = ["Лето", "Зима", "Выпускной", "День рождение"]
    cools = ["Круто", "Весело", "Стыдно", "Грустно", "Вот это да"]
    command_names = ["Ромашка", "Васильки", "Металл", "Музыканты"]

    @staticmethod
    def take_random_seed():
        random.seed()

    @staticmethod
    @get_random
    def __get_random_command_name():
        return Generator.command_names

    @staticmethod
    @get_random
    def __get_random_name():
        return Generator.names

    @staticmethod
    @get_random
    def __get_random_lastname():
        return Generator.lastnames

    @staticmethod
    @get_random
    def __get_random_gender():
        return Generator.genders

    @staticmethod
    @get_random
    def __get_random_customer_status():
        return Generator.customer_statuses

    @staticmethod
    @get_random
    def __get_random_work_type():
        return Generator.work_types

    @staticmethod
    @get_random
    def __get_random_work_status():
        return Generator.work_statuses

    @staticmethod
    @get_random
    def __get_random_media_type():
        return Generator.work_types

    @staticmethod
    def __generate_date():
        year = str(random.randint(2020, 2024))
        month = random.randint(1, 12)
        day = random.randint(1, 31)
        if month < 10:
            month = '0'.join(str(month))
        if day < 10:
            day = '0'.join(str(day))
        dates = [year, '-', month, '-', day]
        return ''.join(dates)

    @staticmethod
    def __generate_number_phone():
        numbers = [8, 9]
        for i in range(9):
            num = random.randint(0, 9)
            numbers.append(num)
        return ''.join(map(str, numbers))

    @staticmethod
    def __generate_album_name():
        strings = [random.choice(Generator.album_names), '-', str(random.randint(2000, 2024)), ' ', random.choice(Generator.cools)]
        return ''.join(strings)

    @staticmethod
    def generate_human():
        return (Generator.__get_random_name(), Generator.__get_random_lastname(), Generator.__generate_number_phone(),
                Generator.__get_random_gender())

    @staticmethod
    def generate_customer():
        return *(Generator.generate_human()), Generator.__get_random_customer_status()

    @staticmethod
    def generate_executor():
        return Generator.generate_human()

    @staticmethod
    def generate_order(customer_id, report_id=None):
        return customer_id, Generator.__generate_date(), random.randint(500, 3500), report_id

    @staticmethod
    def generate_album(size=0):
        if size is None:
            size = random.randint(1, 1000)
        return Generator.__generate_album_name(), size

    @staticmethod
    def generate_report(album_id=None):
        return Generator.__get_random_work_status, album_id

    @staticmethod
    def generate_media(size=0, album_id=None):
        if size == 0:
            size=random.randint(1, 100)
        return (Generator.__get_random_media_type(), size,
                Generator.__generate_album_name()+' '+(str(random.randint(1, 100))), album_id)

    @staticmethod
    def generate_sessions(command_id, order_id):
        return command_id, Generator.__get_random_work_type, order_id

    @staticmethod
    def generate_executors_in_command(mas_of_executors):
        return random.choices(mas_of_executors, k=random.randint(1, 4))

    @staticmethod
    def generate_command():
        return ''.join([Generator.__get_random_command_name(), str(random.randint(1, 100))])
