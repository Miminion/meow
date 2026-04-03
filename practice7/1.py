from connect import connect
import csv

def insert_contact(name, phone):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()
    cur.close()
    conn.close()

def show_contacts():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()
    
    for row in rows:
        print(row)
    
    cur.close()
    conn.close()

def update_contact(name, new_phone):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "UPDATE phonebook SET phone = %s WHERE first_name = %s",
        (new_phone, name)
    )
    conn.commit()
    cur.close()
    conn.close()

def delete_contact(name):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM phonebook WHERE first_name = %s",
        (name,)
    )
    conn.commit()
    cur.close()
    conn.close()

def insert_from_csv():
    conn = connect()
    cur = conn.cursor()
    
    with open("contacts.csv", 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
                (row[0], row[1])
            )
    
    conn.commit()
    cur.close()
    conn.close()

while True:
    print("\n1 - Add contact")
    print("2 - Show contacts")
    print("3 - Update contact")
    print("4 - Delete contact")
    print("5 - Import from CSV")
    print("0 - Exit")
    
    choice = input("Choose: ")
    
    if choice == "1":
        name = input("Name: ")
        phone = input("Phone: ")
        insert_contact(name, phone)
        
    elif choice == "2":
        show_contacts()
        
    elif choice == "3":
        name = input("Name: ")
        phone = input("New phone: ")
        update_contact(name, phone)
        
    elif choice == "4":
        name = input("Name: ")
        delete_contact(name)
        
    elif choice == "5":
        insert_from_csv()
        
    elif choice == "0":
        break