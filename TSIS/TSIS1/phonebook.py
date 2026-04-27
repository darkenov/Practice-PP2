import csv
import json
from connect import connect_db


def run_sql(filename):
    conn = connect_db()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as f:
        sql = f.read()
        cur.execute(sql)

    conn.commit()
    cur.close()
    conn.close()
    print("Done.")


def get_group_id(cur, group_name):
    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    row = cur.fetchone()

    if row:
        return row[0]

    cur.execute("INSERT INTO groups(name) VALUES (%s) RETURNING id", (group_name,))
    group_id = cur.fetchone()[0]
    return group_id


def add_contact():
    conn = connect_db()
    cur = conn.cursor()

    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group_name = input("Group: ")
    phone = input("Phone: ")
    phone_type = input("Type (home/work/mobile): ")

    group_id = get_group_id(cur, group_name)

    cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
    row = cur.fetchone()

    if row:
        contact_id = row[0]
        cur.execute("""
            UPDATE contacts
            SET email = %s, birthday = %s, group_id = %s
            WHERE id = %s
        """, (email or None, birthday or None, group_id, contact_id))
    else:
        cur.execute("""
            INSERT INTO contacts(name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (name, email or None, birthday or None, group_id))
        contact_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO phones(contact_id, phone, type)
        VALUES (%s, %s, %s)
    """, (contact_id, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()
    print("Contact saved.")


def show_contacts(rows):
    if not rows:
        print("No contacts.")
        return

    for row in rows:
        print("\nID:", row[0])
        print("Name:", row[1])
        print("Email:", row[2])
        print("Birthday:", row[3])
        print("Group:", row[4])


def show_all():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.name
    """)

    rows = cur.fetchall()
    show_contacts(rows)

    cur.close()
    conn.close()


def search_contacts():
    conn = connect_db()
    cur = conn.cursor()

    text = input("Search text: ")
    cur.execute("SELECT * FROM search_contacts(%s)", (text,))
    rows = cur.fetchall()

    show_contacts(rows)

    cur.close()
    conn.close()


def filter_by_group():
    conn = connect_db()
    cur = conn.cursor()

    group_name = input("Group name: ")

    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name ILIKE %s
        ORDER BY c.name
    """, (group_name,))

    rows = cur.fetchall()
    show_contacts(rows)

    cur.close()
    conn.close()


def search_by_email():
    conn = connect_db()
    cur = conn.cursor()

    text = input("Email text: ")

    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        WHERE c.email ILIKE %s
        ORDER BY c.name
    """, (f"%{text}%",))

    rows = cur.fetchall()
    show_contacts(rows)

    cur.close()
    conn.close()


def sort_contacts():
    conn = connect_db()
    cur = conn.cursor()

    print("1 - name")
    print("2 - birthday")
    choice = input("Choose sort: ")

    if choice == "2":
        order_field = "birthday"
    else:
        order_field = "name"

    cur.execute(f"""
        SELECT c.id, c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY {order_field} NULLS LAST
    """)

    rows = cur.fetchall()
    show_contacts(rows)

    cur.close()
    conn.close()


def paginate():
    conn = connect_db()
    cur = conn.cursor()

    page = 0
    limit = 3

    while True:
        offset = page * limit

        cur.execute("SELECT * FROM get_contacts_page(%s, %s)", (limit, offset))
        rows = cur.fetchall()

        print(f"\n--- Page {page + 1} ---")
        show_contacts(rows)

        cmd = input("next / prev / quit: ").lower()

        if cmd == "next":
            page += 1
        elif cmd == "prev":
            if page > 0:
                page -= 1
        elif cmd == "quit":
            break

    cur.close()
    conn.close()


def export_json():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.name
    """)

    contacts = cur.fetchall()
    result = []

    for row in contacts:
        contact_id = row[0]

        cur.execute("SELECT phone, type FROM phones WHERE contact_id = %s", (contact_id,))
        phones = cur.fetchall()

        item = {
            "name": row[1],
            "email": row[2],
            "birthday": str(row[3]) if row[3] else "",
            "group": row[4],
            "phones": []
        }

        for p in phones:
            item["phones"].append({
                "phone": p[0],
                "type": p[1]
            })

        result.append(item)

    with open("contacts_export.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    cur.close()
    conn.close()
    print("Exported to contacts_export.json")


def import_json():
    filename = input("JSON file: ")

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    conn = connect_db()
    cur = conn.cursor()

    for item in data:
        name = item["name"]
        email = item.get("email")
        birthday = item.get("birthday")
        group_name = item.get("group", "Other")

        group_id = get_group_id(cur, group_name)

        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        row = cur.fetchone()

        if row:
            answer = input(f"{name} exists. skip or overwrite? ")
            if answer == "skip":
                continue

            contact_id = row[0]

            cur.execute("""
                UPDATE contacts
                SET email = %s, birthday = %s, group_id = %s
                WHERE id = %s
            """, (email or None, birthday or None, group_id, contact_id))

            cur.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))
        else:
            cur.execute("""
                INSERT INTO contacts(name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (name, email or None, birthday or None, group_id))

            contact_id = cur.fetchone()[0]

        for p in item["phones"]:
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (contact_id, p["phone"], p["type"]))

    conn.commit()
    cur.close()
    conn.close()
    print("JSON imported.")


def import_csv():
    filename = input("CSV file: ")

    conn = connect_db()
    cur = conn.cursor()

    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            name = row["name"]
            email = row["email"]
            birthday = row["birthday"]
            group_name = row["group_name"]
            phone = row["phone"]
            phone_type = row["phone_type"]

            group_id = get_group_id(cur, group_name)

            cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
            old = cur.fetchone()

            if old:
                contact_id = old[0]
                cur.execute("""
                    UPDATE contacts
                    SET email = %s, birthday = %s, group_id = %s
                    WHERE id = %s
                """, (email or None, birthday or None, group_id, contact_id))
            else:
                cur.execute("""
                    INSERT INTO contacts(name, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (name, email or None, birthday or None, group_id))
                contact_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (contact_id, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()
    print("CSV imported.")


def add_phone():
    conn = connect_db()
    cur = conn.cursor()

    name = input("Contact name: ")
    phone = input("New phone: ")
    phone_type = input("Type (home/work/mobile): ")

    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()
    print("Phone added.")


def move_group():
    conn = connect_db()
    cur = conn.cursor()

    name = input("Contact name: ")
    group_name = input("New group: ")

    cur.execute("CALL move_to_group(%s, %s)", (name, group_name))

    conn.commit()
    cur.close()
    conn.close()
    print("Group changed.")


def menu():
    while True:
        print("\n1 - Create tables")
        print("2 - Create procedures")
        print("3 - Add contact")
        print("4 - Show all")
        print("5 - Search")
        print("6 - Filter by group")
        print("7 - Search by email")
        print("8 - Sort")
        print("9 - Pages")
        print("10 - Export JSON")
        print("11 - Import JSON")
        print("12 - Import CSV")
        print("13 - Add phone")
        print("14 - Move group")
        print("0 - Exit")

        choice = input("Choose: ")

        if choice == "1":
            run_sql("schema.sql")
        elif choice == "2":
            run_sql("procedures.sql")
        elif choice == "3":
            add_contact()
        elif choice == "4":
            show_all()
        elif choice == "5":
            search_contacts()
        elif choice == "6":
            filter_by_group()
        elif choice == "7":
            search_by_email()
        elif choice == "8":
            sort_contacts()
        elif choice == "9":
            paginate()
        elif choice == "10":
            export_json()
        elif choice == "11":
            import_json()
        elif choice == "12":
            import_csv()
        elif choice == "13":
            add_phone()
        elif choice == "14":
            move_group()
        elif choice == "0":
            break


menu()