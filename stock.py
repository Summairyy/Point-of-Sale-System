import sqlite3
conn = sqlite3.connect('stock.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS stock (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name text,
                price int,
                quatity int)""")

def insert_stock(product_name, price, quatity):
    ID = None
    with conn:
        c.execute("""INSERT INTO stock VALUES (?,?,?,?)""",
                        (ID,product_name, price, quatity))
    conn.commit() 
    print("Data was inserted")

def view_stock():
    with conn:
        c.execute("SELECT * FROM stock")
        allstock = c.fetchall() 
        print(allstock)
        
    return allstock

#insert_stock("Iphone11",20000,2)
view_stock()