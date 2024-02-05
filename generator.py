import random


def get_random(func):
    def wrapper():
        return random.choice(func())
    return wrapper


class Generator:

    names = ["Евгений", "Егор", "Сергей", "Иван", "Начын", "Кирилл", "Михаил", "Самба"]
    lastnames = ["Татарян", "Парфинцов", "Минкеев", "Петроченко", "Биче-Оол", "Гурин", "Ховенмей", "Ховалыг"]
    genders = ["М", "Ж", "Хеликоптер"]
    customer_status = ["Заблокирован", "Постоянный клиент", "Клиент", "Важная персона"]
    work_types = ["Фотография", "Видеография"]
    work_statuses = ["Выполнено", "В работе", "Отложено", "Запланировано", "Заблокировано"]
    media_types = ["Фото", "Видео", "Аудио"]

    @staticmethod
    def take_random_seed():
        random.seed()

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
        return Generator.customer_status

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
    def __generate_number_phone():
        numbers = [8, 9]
        for i in range(9):
            num = random.randint(0, 9)
            numbers.append(num)
        return ''.join(map(str, numbers))

    @staticmethod
    def generate_human():
        return (Generator.__get_random_name(), Generator.__get_random_lastname(), Generator.__generate_number_phone(),
                Generator.__get_random_gender())

    @staticmethod
    def generate_customer():
        return *Generator.generate_human(), Generator.__get_random_customer_status

    @staticmethod
    def generate_executor():
        return Generator.generate_human()

    @staticmethod
    def generate_order(customer_id):
        year = str(random.randint(2020, 2024))
        month = random.randint(1, 12)
        day = random.randint(1 ,31)
        if month < 10:
            month = '0'.join(str(month))
        if day < 10:
            day = '0'.join(str(day))
        dates = [year, '-', month, '-', day]
        return ''.join(dates)

