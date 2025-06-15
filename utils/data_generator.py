import random
import string

from faker import Faker


faker = Faker("ru_RU")


class DataGenerator:
    @staticmethod
    def generate_random_email():
        random_string = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        return f"kek{random_string}@gmail.com"

    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()} {faker.last_name()}"

    @staticmethod
    def generate_random_password():
        letters = random.choice(string.ascii_letters)
        digits = random.choice(string.digits)

        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)
        remaining_chars = "".join(random.choices(all_chars, k=remaining_length))

        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return "".join(password)

    @staticmethod
    def generate_random_movie_title():
        adjectives = [
            "Последний",
            "Тёмный",
            "Секретный",
            "Затерянный",
            "Огненный",
            "Холодный",
            "Железный",
            "Безмолвный",
        ]
        nouns = ["Рыцарь", "Город", "Взрыв", "Лабиринт", "Код", "Контракт", "Шанс", "Сигнал"]

        adjective = random.choice(adjectives)
        noun = random.choice(nouns)
        suffix = faker.word().capitalize()

        return f"{adjective} {noun}: {suffix}"

    @staticmethod
    def generate_random_movie_description():
        hero = faker.first_name()
        profession = random.choice(
            ["детектив", "хакер", "учёный", "солдат", "пилот", "беглец", "программист", "журналист"]
        )
        goal = random.choice(
            [
                "раскрыть заговор",
                "спасти мир",
                "найти пропавшего брата",
                "избежать катастрофы",
                "остановить вирус",
                "взломать систему",
                "найти древний артефакт",
                "изменить прошлое",
            ]
        )
        setting = random.choice(
            [
                "в разрушенном будущем",
                "в параллельной реальности",
                "во время мировой войны",
                "на далёкой планете",
                "в мегаполисе будущего",
                "в виртуальном мире",
                "в постапокалипсисе",
            ]
        )

        return f"{hero}, {profession}, должен {goal} {setting}."

    @staticmethod
    def generate_random_genre():
        genres = [
            "драма",
            "комедия",
            "боевик",
            "триллер",
            "ужасы",
            "фантастика",
            "фэнтези",
            "детектив",
            "приключения",
            "мелодрама",
            "анимация",
            "документальный",
        ]
        return random.choice(genres) + " " + faker.word()
