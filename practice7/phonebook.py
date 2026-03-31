import csv
from connect import connect


def create_table():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS phonebook (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(100),
                    phone VARCHAR(20) UNIQUE
                )
            """)


def add_contact():
    username = input("Введите имя: ")
    phone = input("Введите телефон: ")

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO phonebook (username, phone) VALUES (%s, %s)",
                (username, phone)
            )

    print("Контакт добавлен")


def insert_from_csv():
    with connect() as conn:
        with conn.cursor() as cur:
            file = open("contacts.csv", "r")
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                cur.execute(
                    "INSERT INTO phonebook (username, phone) VALUES (%s, %s)",
                    (row[0], row[1])
                )

            file.close()

    print("Данные из CSV загружены")


def show_all_contacts():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM phonebook ORDER BY id")
            rows = cur.fetchall()

    if len(rows) == 0:
        print("Телефонная книга пуста")
    else:
        for row in rows:
            print(row)


def search_by_name():
    name = input("Введите имя: ")

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM phonebook WHERE username ILIKE %s",
                ("%" + name + "%",)
            )
            rows = cur.fetchall()

    for row in rows:
        print(row)


def search_by_phone_prefix():
    prefix = input("Введите начало номера: ")

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM phonebook WHERE phone LIKE %s",
                (prefix + "%",)
            )
            rows = cur.fetchall()

    for row in rows:
        print(row)


def update_contact():
    print("1 - Изменить имя")
    print("2 - Изменить телефон")
    choice = input("Выберите: ")

    with connect() as conn:
        with conn.cursor() as cur:
            if choice == "1":
                phone = input("Введите телефон: ")
                new_name = input("Введите новое имя: ")

                cur.execute(
                    "UPDATE phonebook SET username = %s WHERE phone = %s",
                    (new_name, phone)
                )
                print("Имя изменено")

            elif choice == "2":
                name = input("Введите имя: ")
                new_phone = input("Введите новый телефон: ")

                cur.execute(
                    "UPDATE phonebook SET phone = %s WHERE username = %s",
                    (new_phone, name)
                )
                print("Телефон изменен")

            else:
                print("Неверный выбор")


def delete_contact():
    print("1 - Удалить по имени")
    print("2 - Удалить по телефону")
    choice = input("Выберите: ")

    with connect() as conn:
        with conn.cursor() as cur:
            if choice == "1":
                name = input("Введите имя: ")
                cur.execute("DELETE FROM phonebook WHERE username = %s", (name,))
                print("Контакт удален")

            elif choice == "2":
                phone = input("Введите телефон: ")
                cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
                print("Контакт удален")

            else:
                print("Неверный выбор")


def menu():
    create_table()

    while True:
        print("\nPHONEBOOK")
        print("1 - Добавить контакт")
        print("2 - Загрузить из CSV")
        print("3 - Показать все контакты")
        print("4 - Найти по имени")
        print("5 - Найти по началу номера")
        print("6 - Изменить контакт")
        print("7 - Удалить контакт")
        print("0 - Выход")

        choice = input("Введите номер: ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            insert_from_csv()
        elif choice == "3":
            show_all_contacts()
        elif choice == "4":
            search_by_name()
        elif choice == "5":
            search_by_phone_prefix()
        elif choice == "6":
            update_contact()
        elif choice == "7":
            delete_contact()
        elif choice == "0":
            print("Выход")
            break
        else:
            print("Неверный ввод")


menu()