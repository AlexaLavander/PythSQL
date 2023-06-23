import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS client(id SERIAL PRIMARY KEY, email VARCHAR UNIQUE, first_name VARCHAR NOT NULL, last_name VARCHAR NOT NULL, phones VARCHAR);")
        
    pass

def add_client(conn, first_name, last_name, email, phone = ""):
    with conn.cursor() as cur:
        cur.execute(""f"INSERT INTO client(email, first_name, last_name, phones) VALUES('{email}', '{first_name}', '{last_name}', '{phone}');""")
        
    pass

def add_phone(conn, client_id, new_phone):
    with conn.cursor() as cur:
        cur.execute(f"SELECT phones FROM client WHERE id = {client_id}")
        if(cur.fetchall() == [('',)]):
            cur.execute(""f"UPDATE client SET phones ='{new_phone}' WHERE id = {client_id};""")
            
        else:
            cur.execute(f"SELECT phones FROM client WHERE id = {client_id};")
            old_phones = cur.fetchall()[0][0]
            if(str(new_phone) in old_phones):
               pass
            else:
                cur.execute(f"UPDATE client SET phones = '' WHERE id = {client_id}")
                cur.execute(""f"UPDATE client SET phones ='{old_phones + str(f', ') + str(new_phone)}' WHERE id = {client_id};""")
    pass

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    with conn.cursor() as cur:
        if(first_name != None):
            cur.execute(f"UPDATE client SET first_name = '{first_name}' WHERE id = {client_id};")
        if(last_name != None):
            cur.execute(f"UPDATE client SET last_name = '{last_name}' WHERE id = {client_id};")
        if(email != None):
            cur.execute(f"UPDATE client SET email = '{email}' WHERE id = {client_id};")
        if(phones != None):
                cur.execute(f"UPDATE client SET phones = '{phones}' WHERE id = {client_id};")

    pass

def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute(f'SELECT phones FROM client WHERE id = {client_id}')
        all_phones = cur.fetchall()[0]
        for phones in all_phones:
            if str(phone) in str(phones):
                deleting_phone = str(phones).replace((", " + str(phone)), "")
                deleting_phone = deleting_phone.replace(str(phone), "")
                if str(deleting_phone) == "":
                    cur.execute(f"UPDATE client SET phones = '' WHERE id = {client_id}")

                else:
                    cur.execute(f"UPDATE client SET phones = '{deleting_phone}' WHERE id = {client_id}")
            else:
                print("Номер не найден")
                    
    pass

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute(f'DELETE FROM client WHERE id = {client_id}')
    pass

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        if(first_name != None):
            cur.execute(f"SELECT id FROM client WHERE first_name = '{first_name}'")
            ids = cur.fetchall()
            for id in ids:
                print('По имени клиента найдены id =', id[0])
            if ids == []:
                print("Клиент с таким именем не найден")
        if(last_name != None):
            cur.execute(f"SELECT id FROM client WHERE last_name = '{last_name}'")
            ids = cur.fetchall()
            for id in  ids:
                print('По фамилии клиента найдены id =', id[0])
            if ids == []:
                print("Клиент с такой фамилией не найден")
        
        if(email != None):
            cur.execute(f"SELECT id FROM client WHERE email = '{email}'")
            ids = cur.fetchall()
            for id in ids:
                print('По имени клиента найдены id =', id[0])
            if ids == []:
                print("Клиент с таким email не найден")
        if(phone != None):
            cur.execute(f"SELECT phones, id FROM client")
            phones_id = cur.fetchall()
            for ids_phones in phones_id:
                if str(phone) in ids_phones[0]:
                   print('По телефону клиента найдены id =', ids_phones[1])
                    
        
    pass



with psycopg2.connect(database=" ", user="postgres", password=" ") as conn:
    create_db(conn)
    
    add_client(conn, "Cameron", "Boys", "rip@gmail.com")
    add_client(conn, "Tasya", "Orlova", "tasyaLife@gmail.com")
    add_client(conn, "Cameron", "Girls", "girlStyle@gmail.com")

    add_phone(conn, 1, 1111)
    add_phone(conn, 1, 89746)
    add_phone(conn, 2, 1111)
    add_phone(conn, 3, 89746)
    add_phone(conn, 3, 9999)
    
    change_client(conn, 1, "Denis")
    change_client(conn, 2, last_name="Volkova")

    delete_phone(conn, 2, 1111)

    delete_client(conn, 2)

    find_client(conn, "Афина", phone = 89746)


   

    pass 
conn.close()

