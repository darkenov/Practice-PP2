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


def call_upsert_contact():
    username = input("Введите имя: ").strip()
    phone = input("Введите телефон: ").strip()

    if username == "" or phone == "":
        print("Имя и телефон не должны быть пустыми.")
        return

    query = "CALL upsert_contact(%s, %s)"

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (username, phone))

    print("Контакт добавлен или обновлён.")


def search_contacts():
    pattern = input("Введите шаблон для поиска: ").strip()

    if pattern == "":
        print("Шаблон не должен быть пустым.")
        return

    query = "SELECT * FROM search_contacts(%s)"

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (pattern,))
            rows = cur.fetchall()

    if rows:
        print("\nРезультаты поиска:")
        for row in rows:
            print(row)
    else:
        print("Ничего не найдено.")


def show_paginated_contacts():
    limit_value = input("Введите LIMIT: ").strip()
    offset_value = input("Введите OFFSET: ").strip()

    if not limit_value.isdigit() or not offset_value.isdigit():
        print("LIMIT и OFFSET должны быть числами.")
        return

    query = "SELECT * FROM get_contacts_paginated(%s, %s)"

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (int(limit_value), int(offset_value)))
            rows = cur.fetchall()

    if rows:
        print("\nКонтакты:")
        for row in rows:
            print(row)
    else:
        print("Ничего не найдено.")


def call_delete_contact():
    value = input("Введите имя или номер для удаления: ").strip()

    if value == "":
        print("Поле не должно быть пустым.")
        return

    query = "CALL delete_contact(%s)"

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (value,))

    print("Контакт удалён.")


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


def menu():
    create_table()

    while True:
        print("\n===== PHONEBOOK PRACTICE 8 =====")
        print("1 - Добавить или обновить контакт")
        print("2 - Поиск по шаблону")
        print("3 - Показать контакты с пагинацией")
        print("4 - Удалить контакт")
        print("5 - Показать все контакты")
        print("0 - Выход")

        choice = input("Введите номер действия: ").strip()

        if choice == "1":
            call_upsert_contact()
        elif choice == "2":
            search_contacts()
        elif choice == "3":
            show_paginated_contacts()
        elif choice == "4":
            call_delete_contact()
        elif choice == "5":
            show_all_contacts()
        elif choice == "0":
            print("Программа завершена.")
            break
        else:
            print("Неправильный ввод.")


menu()