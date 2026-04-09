from connect import connect

def search(pattern):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_pattern(%s)", (pattern,))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    conn.close()

def add_or_update(name, phone):
    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()
    conn.close()

def delete_contact(value):
    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL delete_contact(%s)", (value,))
    conn.commit()
    conn.close()

def paginate(limit, offset):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    conn.close()


while True:
    print("\n1 - Search")
    print("2 - Add or Update")
    print("3 - Delete")
    print("4 - Pagination")
    print("0 - Exit")

    choice = input("Choose: ")

    if choice == "1":
        p = input("Enter pattern: ")
        search(p)

    elif choice == "2":
        n = input("Name: ")
        ph = input("Phone: ")
        add_or_update(n, ph)

    elif choice == "3":
        v = input("Enter name or phone: ")
        delete_contact(v)

    elif choice == "4":
        l = int(input("Limit: "))
        o = int(input("Offset: "))
        paginate(l, o)

    elif choice == "0":
        break