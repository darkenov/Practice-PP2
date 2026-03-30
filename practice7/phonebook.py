import csv
from connect import connect


def create_table():
    query = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL UNIQUE
    )
    """

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query)

    print("Таблица phonebook создана или уже существует.")


def insert_from_console():
    username = input("Введите имя: ").strip()
    phone = input("Введите номер телефона: ").strip()

    if username == "" or phone == "":
        print("Имя и телефон не должны быть пустыми.")
        return

    query = """
    INSERT INTO phonebook (username, phone)
    VALUES (%s, %s)
    """

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (username, phone))

    print("Контакт добавлен.")


def insert_from_csv():
    query = """
    INSERT INTO phonebook (username, phone)
    VALUES (%s, %s)
    """

    with connect() as conn:
        with conn.cursor() as cur:
            with open("contacts.csv", "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)

                for row in reader:
                    username = row[0].strip()
                    phone = row[1].strip()

                    if username != "" and phone != "":
                        cur.execute(query, (username, phone))

    print("Данные из CSV загружены.")


def show_all_contacts():
    query = "SELECT * FROM phonebook ORDER BY id"

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

    if rows:
        print("\nВсе контакты:")
        for row in rows:
            print(row)
    else:
        print("Телефонная книга пуста.")


def search_by_name():
    name = input("Введите имя или часть имени: ").strip()

    if name == "":
        print("Поле поиска не должно быть пустым.")
        return

    query = """
    SELECT * FROM phonebook
    WHERE username ILIKE %s
    ORDER BY id
    """

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query, ("%" + name + "%",))
            rows = cur.fetchall()

    if rows:
        print("\nРезультаты поиска:")
        for row in rows:
            print(row)
    else:
        print("Ничего не найдено.")


def search_by_phone_prefix():
    prefix = input("Введите начало номера: ").strip()

    if prefix == "":
        print("Префикс не должен быть пустым.")
        return

    query = """
    SELECT * FROM phonebook
    WHERE phone LIKE %s
    ORDER BY id
    """

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (prefix + "%",))
            rows = cur.fetchall()

    if rows:
        print("\nРезультаты поиска:")
        for row in rows:
            print(row)
    else:
        print("Ничего не найдено.")


def update_contact():
    print("1 - Изменить имя")
    print("2 - Изменить телефон")
    choice = input("Выберите действие: ").strip()

    with connect() as conn:
        with conn.cursor() as cur:
            if choice == "1":
                phone = input("Введите телефон контакта: ").strip()
                new_name = input("Введите новое имя: ").strip()

                if phone == "" or new_name == "":
                    print("Телефон и новое имя не должны быть пустыми.")
                    return

                query = """
                UPDATE phonebook
                SET username = %s
                WHERE phone = %s
                """
                cur.execute(query, (new_name, phone))

                if cur.rowcount > 0:
                    print("Имя обновлено.")
                else:
                    print("Контакт не найден.")

            elif choice == "2":
                name = input("Введите имя контакта: ").strip()
                new_phone = input("Введите новый телефон: ").strip()

                if name == "" or new_phone == "":
                    print("Имя и новый телефон не должны быть пустыми.")
                    return

                query = """
                UPDATE phonebook
                SET phone = %s
                WHERE username = %s
                """
                cur.execute(query, (new_phone, name))

                if cur.rowcount > 0:
                    print("Телефон обновлён.")
                else:
                    print("Контакт не найден.")

            else:
                print("Неверный выбор.")


def delete_contact():
    print("1 - Удалить по имени")
    print("2 - Удалить по телефону")
    choice = input("Выберите действие: ").strip()

    with connect() as conn:
        with conn.cursor() as cur:
            if choice == "1":
                name = input("Введите имя: ").strip()

                if name == "":
                    print("Имя не должно быть пустым.")
                    return

                query = "DELETE FROM phonebook WHERE username = %s"
                cur.execute(query, (name,))

                if cur.rowcount > 0:
                    print("Контакт удалён.")
                else:
                    print("Контакт не найден.")

            elif choice == "2":
                phone = input("Введите телефон: ").strip()

                if phone == "":
                    print("Телефон не должен быть пустым.")
                    return

                query = "DELETE FROM phonebook WHERE phone = %s"
                cur.execute(query, (phone,))

                if cur.rowcount > 0:
                    print("Контакт удалён.")
                else:
                    print("Контакт не найден.")

            else:
                print("Неверный выбор.")


def menu():
    create_table()

    while True:
        print("\n===== PHONEBOOK =====")
        print("1 - Добавить контакт вручную")
        print("2 - Загрузить контакты из CSV")
        print("3 - Показать все контакты")
        print("4 - Найти по имени")
        print("5 - Найти по началу номера")
        print("6 - Обновить контакт")
        print("7 - Удалить контакт")
        print("0 - Выход")

        choice = input("Введите номер действия: ").strip()

        if choice == "1":
            insert_from_console()
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
            print("Программа завершена.")
            break
        else:
            print("Неправильный ввод. Попробуйте снова.")


menu()