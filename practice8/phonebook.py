from connect import connect

def search(pattern):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_pattern(%s::text)", (pattern,))
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("Ничего не найдено.")
    conn.close()

def add_or_update(name, phone):
    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL upsert_contact(%s::varchar, %s::varchar)", (name, phone))
    conn.commit()
    print("Готово!")
    conn.close()

def add_many(contacts: list):
    names  = [c[0] for c in contacts]
    phones = [c[1] for c in contacts]
    conn = connect()
    cur  = conn.cursor()
    cur.execute("CALL insert_many_contacts(%s::varchar[], %s::varchar[])", (names, phones))
    conn.commit()
    print("Готово!")
    conn.close()

def delete_contact(value):
    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL delete_contact(%s::varchar)", (value,))
    conn.commit()
    print("Удалено!")
    conn.close()

def paginate(limit, offset):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_paginated(%s::int, %s::int)", (limit, offset))
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("Записей нет.")
    conn.close()


while True:
    print("\n1 - Поиск")
    print("2 - Добавить / обновить одного")
    print("3 - Удалить")
    print("4 - Пагинация")
    print("5 - Добавить много сразу")
    print("0 - Выход")

    choice = input("Выбери: ")

    if choice == "1":
        p = input("Паттерн: ")
        search(p)

    elif choice == "2":
        n = input("Имя: ")
        ph = input("Телефон: ")
        add_or_update(n, ph)

    elif choice == "3":
        v = input("Имя или телефон: ")
        delete_contact(v)

    elif choice == "4":
        l = int(input("Лимит: "))
        o = int(input("Оффсет: "))
        paginate(l, o)

    elif choice == "5":
        contacts = []
        count = int(input("Сколько контактов? "))
        for _ in range(count):
            n  = input("Имя: ")
            ph = input("Телефон: ")
            contacts.append((n, ph))
        add_many(contacts)

    elif choice == "0":
        break
