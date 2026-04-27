import csv
import json
from datetime import datetime
from connect import get_connection


def run_sql_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        sql = f.read()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


def get_group_id(cur, group_name):
    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute("INSERT INTO groups(name) VALUES (%s) RETURNING id", (group_name,))
    return cur.fetchone()[0]


def add_contact():
    conn = get_connection()
    cur = conn.cursor()

    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group_name = input("Group: ")
    phone = input("Phone: ")
    phone_type = input("Phone type (home/work/mobile): ")

    group_id = get_group_id(cur, group_name)

    cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
    row = cur.fetchone()

    if row:
        contact_id = row[0]
        cur.execute(
            "UPDATE contacts SET email=%s, birthday=%s, group_id=%s WHERE id=%s",
            (email or None, birthday or None, group_id, contact_id)
        )
    else:
        cur.execute(
            "INSERT INTO contacts(name, email, birthday, group_id) VALUES (%s,%s,%s,%s) RETURNING id",
            (name, email or None, birthday or None, group_id)
        )
        contact_id = cur.fetchone()[0]

    cur.execute(
        "INSERT INTO phones(contact_id, phone, type) VALUES (%s,%s,%s)",
        (contact_id, phone, phone_type)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact added.")


def show_contact_rows(rows):
    for row in rows:
        print(f"\nID: {row[0]}")
        print(f"Name: {row[1]}")
        print(f"Email: {row[2]}")
        print(f"Birthday: {row[3]}")
        print(f"Group: {row[4]}")
        print(f"Created: {row[5]}")


def show_all_contacts():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name, c.created_at
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.name
    """)
    rows = cur.fetchall()
    show_contact_rows(rows)
    cur.close()
    conn.close()


def search_contacts():
    conn = get_connection()
    cur = conn.cursor()
    query = input("Search text: ")
    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    rows = cur.fetchall()
    show_contact_rows(rows)
    cur.close()
    conn.close()


def filter_by_group():
    conn = get_connection()
    cur = conn.cursor()
    group_name = input("Group name: ")
    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name, c.created_at
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name ILIKE %s
        ORDER BY c.name
    """, (group_name,))
    rows = cur.fetchall()
    show_contact_rows(rows)
    cur.close()
    conn.close()


def search_by_email():
    conn = get_connection()
    cur = conn.cursor()
    email_text = input("Email text: ")
    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name, c.created_at
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        WHERE c.email ILIKE %s
        ORDER BY c.name
    """, (f"%{email_text}%",))
    rows = cur.fetchall()
    show_contact_rows(rows)
    cur.close()
    conn.close()


def sort_contacts():
    conn = get_connection()
    cur = conn.cursor()
    print("1 - name")
    print("2 - birthday")
    print("3 - created_at")
    choice = input("Sort by: ")

    field = "name"
    if choice == "2":
        field = "birthday"
    elif choice == "3":
        field = "created_at"

    cur.execute(f"""
        SELECT c.id, c.name, c.email, c.birthday, g.name, c.created_at
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY {field} NULLS LAST
    """)
    rows = cur.fetchall()
    show_contact_rows(rows)
    cur.close()
    conn.close()


def paginate_contacts():
    conn = get_connection()
    cur = conn.cursor()

    page = 0
    limit = 3

    while True:
        offset = page * limit
        cur.execute("SELECT * FROM get_contacts_page(%s, %s)", (limit, offset))
        rows = cur.fetchall()

        if not rows:
            print("No more contacts.")
        else:
            print(f"\n--- Page {page + 1} ---")
            show_contact_rows(rows)

        cmd = input("\nnext / prev / quit: ").lower()
        if cmd == "next":
            page += 1
        elif cmd == "prev" and page > 0:
            page -= 1
        elif cmd == "quit":
            break

    cur.close()
    conn.close()


def export_json():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name, c.created_at
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.name
    """)
    contacts = cur.fetchall()

    result = []
    for c in contacts:
        cur.execute("SELECT phone, type FROM phones WHERE contact_id = %s", (c[0],))
        phones = cur.fetchall()

        result.append({
            "name": c[1],
            "email": c[2],
            "birthday": str(c[3]) if c[3] else None,
            "group": c[4],
            "phones": [{"phone": p[0], "type": p[1]} for p in phones]
        })

    with open("contacts_export.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    print("Exported to contacts_export.json")
    cur.close()
    conn.close()


def import_json():
    filename = input("JSON file name: ")
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    conn = get_connection()
    cur = conn.cursor()

    for item in data:
        name = item["name"]
        email = item.get("email")
        birthday = item.get("birthday")
        group_name = item.get("group", "Other")

        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        row = cur.fetchone()

        if row:
            action = input(f"{name} exists. skip / overwrite? ").lower()
            if action == "skip":
                continue
            contact_id = row[0]
            group_id = get_group_id(cur, group_name)
            cur.execute("""
                UPDATE contacts
                SET email=%s, birthday=%s, group_id=%s
                WHERE id=%s
            """, (email, birthday, group_id, contact_id))
            cur.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))
        else:
            group_id = get_group_id(cur, group_name)
            cur.execute("""
                INSERT INTO contacts(name, email, birthday, group_id)
                VALUES (%s,%s,%s,%s)
                RETURNING id
            """, (name, email, birthday, group_id))
            contact_id = cur.fetchone()[0]

        for p in item.get("phones", []):
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s,%s,%s)
            """, (contact_id, p["phone"], p["type"]))

    conn.commit()
    cur.close()
    conn.close()
    print("JSON import complete.")


def import_csv():
    filename = input("CSV file name: ")
    conn = get_connection()
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

            cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
            existing = cur.fetchone()

            if existing:
                contact_id = existing[0]
                cur.execute("""
                    UPDATE contacts
                    SET email=%s, birthday=%s, group_id=%s
                    WHERE id=%s
                """, (email or None, birthday or None, group_id, contact_id))
            else:
                cur.execute("""
                    INSERT INTO contacts(name, email, birthday, group_id)
                    VALUES (%s,%s,%s,%s)
                    RETURNING id
                """, (name, email or None, birthday or None, group_id))
                contact_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s,%s,%s)
            """, (contact_id, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()
    print("CSV import complete.")


def add_phone_proc():
    conn = get_connection()
    cur = conn.cursor()
    name = input("Contact name: ")
    phone = input("New phone: ")
    ptype = input("Type (home/work/mobile): ")
    cur.execute("CALL add_phone(%s,%s,%s)", (name, phone, ptype))
    conn.commit()
    cur.close()
    conn.close()
    print("Phone added.")


def move_group_proc():
    conn = get_connection()
    cur = conn.cursor()
    name = input("Contact name: ")
    group_name = input("New group: ")
    cur.execute("CALL move_to_group(%s,%s)", (name, group_name))
    conn.commit()
    cur.close()
    conn.close()
    print("Moved to group.")


def menu():
    while True:
        print("\n1. Init schema")
        print("2. Init procedures")
        print("3. Add contact")
        print("4. Show all")
        print("5. Search all fields")
        print("6. Filter by group")
        print("7. Search by email")
        print("8. Sort contacts")
        print("9. Paginate")
        print("10. Export JSON")
        print("11. Import JSON")
        print("12. Import CSV")
        print("13. Add phone")
        print("14. Move to group")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            run_sql_file("schema.sql")
            print("Schema ready.")
        elif choice == "2":
            run_sql_file("procedures.sql")
            print("Procedures ready.")
        elif choice == "3":
            add_contact()
        elif choice == "4":
            show_all_contacts()
        elif choice == "5":
            search_contacts()
        elif choice == "6":
            filter_by_group()
        elif choice == "7":
            search_by_email()
        elif choice == "8":
            sort_contacts()
        elif choice == "9":
            paginate_contacts()
        elif choice == "10":
            export_json()
        elif choice == "11":
            import_json()
        elif choice == "12":
            import_csv()
        elif choice == "13":
            add_phone_proc()
        elif choice == "14":
            move_group_proc()
        elif choice == "0":
            break


if __name__ == "__main__":
    menu()