import csv
import json
from pathlib import Path

from connect import get_connection


def run_sql_file(filename):
    conn = get_connection()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        cur.execute(file.read())

    conn.commit()
    cur.close()
    conn.close()


def create_schema():
    run_sql_file("schema.sql")       
    run_sql_file("procedures.sql")
    print("Schema and procedures created")


def get_group_id(cur, group_name):
    if not group_name:
        group_name = "Other"

    cur.execute(
        "INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
        (group_name,)
    )

    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    return cur.fetchone()[0]


def add_contact():
    username = input("Name: ").strip()
    email = input("Email: ").strip()
    birthday = input("Birthday YYYY-MM-DD or empty: ").strip()
    group_name = input("Group Family/Work/Friend/Other: ").strip()

    phone = input("Phone: ").strip()
    phone_type = input("Phone type home/work/mobile: ").strip()

    if birthday == "":
        birthday = None

    conn = get_connection()
    cur = conn.cursor()

    group_id = get_group_id(cur, group_name)

    cur.execute(
        """
        INSERT INTO contacts (username, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (username) DO UPDATE
        SET email = EXCLUDED.email,
            birthday = EXCLUDED.birthday,
            group_id = EXCLUDED.group_id
        RETURNING id
        """,
        (username, email, birthday, group_id)
    )

    contact_id = cur.fetchone()[0]

    if phone:
        cur.execute(
            "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
            (contact_id, phone, phone_type)
        )

    conn.commit()
    cur.close()
    conn.close()

    print("Contact saved")


def call_add_phone():
    name = input("Contact name: ").strip()
    phone = input("New phone: ").strip()
    phone_type = input("Phone type home/work/mobile: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()

    print("Phone added")


def call_move_to_group():
    name = input("Contact name: ").strip()
    group_name = input("New group: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL move_to_group(%s, %s)", (name, group_name))

    conn.commit()
    cur.close()
    conn.close()

    print("Contact moved")


def print_rows(rows):
    if not rows:
        print("No contacts found")
        return

    for row in rows:
        print("-" * 60)
        print(f"ID: {row[0]}")
        print(f"Name: {row[1]}")
        print(f"Email: {row[2]}")
        print(f"Birthday: {row[3]}")
        print(f"Group: {row[4]}")
        print(f"Phones: {row[5]}")


def search_contacts():
    query = input("Search name/email/phone: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s::text)", (query,)) 
    rows = cur.fetchall()

    print_rows(rows)

    cur.close()
    conn.close()


def filter_by_group():
    group_name = input("Group name: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            c.id,
            c.username,
            c.email,
            c.birthday,
            g.name,
            COALESCE(string_agg(p.phone || ' (' || p.type || ')', ', '), '')
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        LEFT JOIN phones p ON p.contact_id = c.id
        WHERE g.name ILIKE %s
        GROUP BY c.id, c.username, c.email, c.birthday, g.name
        ORDER BY c.username
        """,
        (group_name,)
    )

    rows = cur.fetchall()
    print_rows(rows)

    cur.close()
    conn.close()


def search_by_email():
    email = input("Email pattern: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            c.id,
            c.username,
            c.email,
            c.birthday,
            g.name,
            COALESCE(string_agg(p.phone || ' (' || p.type || ')', ', '), '')
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        LEFT JOIN phones p ON p.contact_id = c.id
        WHERE c.email ILIKE %s
        GROUP BY c.id, c.username, c.email, c.birthday, g.name
        ORDER BY c.username
        """,
        (f"%{email}%",)
    )

    rows = cur.fetchall()
    print_rows(rows)

    cur.close()
    conn.close()


def paginated_contacts():
    limit = 5
    offset = 0
    sort_by = input("Sort by name/birthday/date: ").strip()

    if sort_by not in ("name", "birthday", "date"):
        sort_by = "name"

    while True:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM get_contacts_page(%s, %s, %s)", (limit, offset, sort_by))
        rows = cur.fetchall()

        print(f"\nPage offset: {offset}")
        print_rows(rows)

        cur.close()
        conn.close()

        command = input("next / prev / quit: ").strip().lower()

        if command == "next":
            offset += limit

        elif command == "prev":
            offset = max(0, offset - limit)

        elif command == "quit":
            break


def delete_contact():
    name = input("Name to delete: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM contacts WHERE username = %s", (name,))

    conn.commit()
    cur.close()
    conn.close()

    print("Deleted if existed")


def export_json():
    filename = input("JSON filename to export, example contacts.json: ").strip()

    if not filename:
        filename = "contacts.json"

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            c.id,
            c.username,
            c.email,
            c.birthday,
            g.name
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        ORDER BY c.username
        """
    )

    contacts = []

    for contact_id, username, email, birthday, group_name in cur.fetchall():
        cur.execute(
            "SELECT phone, type FROM phones WHERE contact_id = %s ORDER BY id",
            (contact_id,)
        )

        phones = [{"phone": phone, "type": phone_type} for phone, phone_type in cur.fetchall()]

        contacts.append({
            "username": username,
            "email": email,
            "birthday": birthday.isoformat() if birthday else None,
            "group": group_name,
            "phones": phones
        })

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4)

    cur.close()
    conn.close()

    print(f"Exported to {filename}")


def import_json():
    filename = input("JSON filename to import: ").strip()

    if not Path(filename).exists():
        print("File not found")
        return

    with open(filename, "r", encoding="utf-8") as file:
        contacts = json.load(file)

    conn = get_connection()
    cur = conn.cursor()

    for item in contacts:
        username = item.get("username")
        email = item.get("email")
        birthday = item.get("birthday")
        group_name = item.get("group", "Other")
        phones = item.get("phones", [])

        cur.execute("SELECT id FROM contacts WHERE username = %s", (username,))
        existing = cur.fetchone()

        if existing:
            answer = input(f"{username} exists. skip or overwrite? ").strip().lower()

            if answer == "skip":
                continue

            cur.execute("DELETE FROM contacts WHERE username = %s", (username,))

        group_id = get_group_id(cur, group_name)

        cur.execute(
            """
            INSERT INTO contacts (username, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (username, email, birthday, group_id)
        )

        contact_id = cur.fetchone()[0]

        for phone_item in phones:
            cur.execute(
                "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                (contact_id, phone_item["phone"], phone_item["type"])
            )

    conn.commit()
    cur.close()
    conn.close()

    print("JSON import finished")


def import_csv():
    filename = input("CSV filename, example contacts.csv: ").strip()

    if not Path(filename).exists():
        print("File not found")
        return

    conn = get_connection()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            username = row["username"]
            email = row.get("email")
            birthday = row.get("birthday") or None
            group_name = row.get("group") or "Other"
            phone = row.get("phone")
            phone_type = row.get("type") or "mobile"

            group_id = get_group_id(cur, group_name)

            cur.execute(
                """
                INSERT INTO contacts (username, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (username) DO UPDATE
                SET email = EXCLUDED.email,
                    birthday = EXCLUDED.birthday,
                    group_id = EXCLUDED.group_id
                RETURNING id
                """,
                (username, email, birthday, group_id)
            )

            contact_id = cur.fetchone()[0]

            if phone:
                cur.execute(
                    "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                    (contact_id, phone, phone_type)
                )

    conn.commit()
    cur.close()
    conn.close()

    print("CSV import finished")


def menu():
    while True:
        print("\n--- PHONEBOOK TSIS1 ---")
        print("1. Create schema")
        print("2. Add contact")
        print("3. Add phone to contact")
        print("4. Move contact to group")
        print("5. Search contacts name/email/phone")
        print("6. Filter by group")
        print("7. Search by email")
        print("8. Paginated contacts")
        print("9. Delete contact")
        print("10. Export JSON")
        print("11. Import JSON")
        print("12. Import CSV")
        print("0. Exit")

        choice = input("Choose: ").strip()

        try:
            if choice == "1":
                create_schema()
            elif choice == "2":
                add_contact()
            elif choice == "3":
                call_add_phone()
            elif choice == "4":
                call_move_to_group()
            elif choice == "5":
                search_contacts()
            elif choice == "6":
                filter_by_group()
            elif choice == "7":
                search_by_email()
            elif choice == "8":
                paginated_contacts()
            elif choice == "9":
                delete_contact()
            elif choice == "10":
                export_json()
            elif choice == "11":
                import_json()
            elif choice == "12":
                import_csv()
            elif choice == "0":
                break
            else:
                print("Wrong option")

        except Exception as error:
            print("Error:")
            print(error)


if __name__ == "__main__":
    menu()