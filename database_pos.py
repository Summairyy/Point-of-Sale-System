from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from tkinter import colorchooser

inventory = Tk()
inventory.title("Database POS")
inventory.geometry("750x570")

id = StringVar()
#Menu
my_menu = Menu(inventory)
inventory.config(menu=my_menu)

def view_database():
    for record in tree_stock.get_children():
        tree_stock.delete(record)

    conn = sqlite3.connect('pos.db')
    c = conn.cursor()
    c.execute("SELECT * FROM stock")
    records = c.fetchall()
    #Add data to the screen
    global count
    count = 0
    for record in records:
        print(record)

    for record in records:
        if count % 2 == 0:
            tree_stock.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3]),tags=('evenrow',))
        else:
            tree_stock.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3]),tags=('oddrow',))
        count += 1  
    
    conn.commit()
    conn.close()

def search_records():
    lookup_record = search_entry.get()
    for record in tree_stock.get_children():
        tree_stock.delete(record)
    search_entry.delete(0,END)
    conn = sqlite3.connect('pos.db')
    c = conn.cursor()
    c.execute("SELECT * FROM stock WHERE product_name like ?",(lookup_record,))
    records = c.fetchall()
    #Add data to the screen
    global count
    count = 0
    for record in records:
        print(record)

    for record in records:
        if count % 2 == 0:
            tree_stock.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3]),tags=('evenrow',))
        else:
            tree_stock.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3]),tags=('oddrow',))
        count += 1  
    
    conn.commit()
    conn.close()

def primary_color():
    primary_color = colorchooser.askcolor()[1]
    if primary_color:
        tree_stock.tag_configure('evenrow',background=primary_color)  

def secon_color():
    secon_color = colorchooser.askcolor()[1]
    if secon_color:
        tree_stock.tag_configure('oddrow',background=secon_color)

def hl_color():
    hl_color = colorchooser.askcolor()[1]
    if hl_color:
        style.map('Treeview',background=[('selected',hl_color)])

option_menu = Menu(my_menu,tearoff=0)
my_menu.add_cascade(label="Options",menu=option_menu)
option_menu.add_command(label="Primary Color",command=primary_color)
option_menu.add_command(label="Secondary Color",command=secon_color)
option_menu.add_command(label="Highlight Color",command=hl_color)
option_menu.add_separator()
option_menu.add_command(label="Exit",command=inventory.quit)

#====================database=========================
conn = sqlite3.connect('pos.db')
c = conn.cursor()
#Create tablea
c.execute("""CREATE TABLE IF NOT EXISTS stock (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name text,
                price int,
                quatity int)""")

conn.commit()
conn.close()

#============================================================================
style = ttk.Style()
style.theme_use('default')
style.configure("Treeview",bg="#D3D3D3",fg="black",rowheight=25,fieldbackground="#D3D3D3")

style.map('Treeview',background=[('selected',"#a38767")])
#===========Search============================
search_frame = LabelFrame(inventory,text="Search Records")
search_frame.pack(fill=X,expand="yes",padx=20)
saerch_lbl = Label(search_frame,text="Product Name :")
saerch_lbl.grid(row=0,column=0,padx=8,pady=8)
search_entry = Entry(search_frame,font=10,width=35)
search_entry.grid(row=0,column=1,padx=8,pady=8)
search_btn = Button(search_frame,text="Search",width=10,command=search_records)
search_btn.grid(row=0,column=2,padx=8,pady=8)
refresh_btn = Button(search_frame,text="Refresh table",width=10,command=view_database)
refresh_btn.grid(row=0,column=3,padx=8,pady=8)

# Create Treeview Frame & Scrollbar
tree_farme = Frame(inventory)
tree_farme.pack(pady=15)
tree_scroll = Scrollbar(tree_farme)
tree_scroll.pack(side=RIGHT,fill=Y)
# Create Treeview
tree_stock = ttk.Treeview(tree_farme,yscrollcommand=tree_scroll.set,selectmode="extended")
tree_stock.pack()
tree_scroll.config(command=tree_stock.yview)
#Format Column
tree_stock['columns'] = ("Product ID","Product Name","Price","Quatity")
tree_stock.column("#0",width=0,stretch=NO)
tree_stock.column("Product ID",anchor=CENTER,width=140)
tree_stock.column("Product Name",anchor=CENTER,width=250)
tree_stock.column("Price",anchor=CENTER,width=140)
tree_stock.column("Quatity",anchor=CENTER,width=140)
#Heading
tree_stock.heading("#0")
tree_stock.heading("Product ID",text="Product ID", anchor=CENTER)
tree_stock.heading("Product Name",text="Product Name", anchor=CENTER)
tree_stock.heading("Price",text="Price", anchor=CENTER)
tree_stock.heading("Quatity",text="Quatity", anchor=CENTER)

tree_stock.tag_configure('oddrow',background="white")
tree_stock.tag_configure('evenrow',background="#FAD5A5")  

########################Button Command##############################
#Move Up
def up():
    rows = tree_stock.selection()
    for row in rows:
        tree_stock.move(row,tree_stock.parent(row),tree_stock.index(row)-1)
#Move Down
def down():
    rows = tree_stock.selection()
    for row in reversed(rows):
        tree_stock.move(row,tree_stock.parent(row),tree_stock.index(row)+1)
#Remove one data
def remove_one():
    x = tree_stock.selection()[0]
    tree_stock.delete(x)

    conn = sqlite3.connect('pos.db')
    c = conn.cursor()
    c.execute("DELETE from stock WHERE product_name=" + pname_entry.get())
    conn.commit()
    conn.close()
    clean_entries()

#Remove all data
def remove_all():
    ##Messagebox
    response = messagebox.askyesno("Deleted!","This will delete EVERYTHING from the table\nAre you sure?")
    if response == 1:
        for record in tree_stock.get_children():
            tree_stock.delete(record)
        conn = sqlite3.connect('pos.db')
        c = conn.cursor()
        c.execute("DROP TABLE stock")

        conn.commit()
        conn.close()
        clean_entries()
        create_table_again()
#Clean entry box
def clean_entries():
    id.set("")
    pid_entry.delete(0,END)
    pname_entry.delete(0,END)
    p_price_entry.delete(0,END)
    pqua_entry.delete(0,END) 
#Select Record
def sel_record(e):
    pid_entry.delete(0,END)
    pname_entry.delete(0,END)
    p_price_entry.delete(0,END)
    pqua_entry.delete(0,END)

    selected = tree_stock.focus()
    values = tree_stock.item(selected,'values')
    #output to entry boxs
    x = values[0]
    id.set(x)
    pid_entry.insert(0,values[0])
    pname_entry.insert(0,values[1])
    p_price_entry.insert(0,values[2])
    pqua_entry.insert(0,values[3])
#Update Data
def update_record():
    selected = tree_stock.focus()
    print(selected)
    tree_stock.item(selected,text="",values=(pid_entry.get(),pname_entry.get(),p_price_entry.get(),pqua_entry.get(),))
    
    #Update Database
    conn = sqlite3.connect('pos.db')
    c = conn.cursor()
    c.execute("""UPDATE stock SET
            product_name = ?,
            price = ?,
            quatity = ?

            WHERE oid = ?""",
            (
                pname_entry.get(),
                p_price_entry.get(),
                pqua_entry.get(),
                pid_entry.get()
            ))
    print()
    conn.commit()
    conn.close()
    clean_entries()
#Add data
def add_data():  
    conn = sqlite3.connect('pos.db')
    c = conn.cursor()
    c.execute("INSERT INTO stock (product_name,price,quatity) VALUES ( :name, :price, :quatity)",
              {
                'name': pname_entry.get(),
                'price': p_price_entry.get(),
                'quatity': pqua_entry.get()
              })

    conn.commit()
    conn.close()
    clean_entries()

    tree_stock.delete(*tree_stock.get_children())
    view_database()

def create_table_again():
    conn = sqlite3.connect('pos.db')
    c = conn.cursor()
    #Create table
    c.execute("""CREATE TABLE IF NOT EXISTS stock (
                    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_name text,
                    price int,
                    quatity int)""")

    conn.commit()
    conn.close()


#=========Add Record==========================
data_frame = LabelFrame(inventory,text="Record")
data_frame.pack(fill="x", expand="yes",padx=20)
##Product ID
pid_label = Label(data_frame,text="Product ID")
pid_label.grid(row=0,column=0,padx=10,pady=10)
pid_entry = Entry(data_frame,textvariable=id,state=DISABLED)
pid_entry.grid(row=0,column=1,padx=10,pady=10)
##Product Name
pname_label = Label(data_frame,text="Product Name")
pname_label.grid(row=0,column=2,padx=10,pady=10)
pname_entry = Entry(data_frame)
pname_entry.grid(row=0,column=3,padx=10,pady=10)
##Price
p_price_label = Label(data_frame,text="Price")
p_price_label.grid(row=1,column=0,padx=10,pady=10)
p_price_entry = Entry(data_frame)
p_price_entry.grid(row=1,column=1,padx=10,pady=10)
##Quatity
pqua_label = Label(data_frame,text="Quatity")
pqua_label.grid(row=1,column=2,padx=10,pady=10)
pqua_entry = Entry(data_frame)
pqua_entry.grid(row=1,column=3,padx=10,pady=10)

#============Add Button========================
button_frame = LabelFrame(inventory,text="Commands")
button_frame.pack(fill="x",expand="yes",padx=20)
##Update Data
upd_button = Button(button_frame,text="Update Data",command=update_record)
upd_button.grid(row=0,column=0,padx=10,pady=10)
##Add Data
add_button = Button(button_frame,text="Add Data",command=add_data)
add_button.grid(row=0,column=1,padx=10,pady=10)
##Remove all data
re_all_button = Button(button_frame,text="Remove all data",command=remove_all)
re_all_button.grid(row=0,column=2,padx=10,pady=10)
##Remove one data
re_one_button = Button(button_frame,text="Remove one data",command=remove_one)
re_one_button.grid(row=0,column=3,padx=10,pady=10)
##Move Up
move_up_button = Button(button_frame,text="Move Up",command=up)
move_up_button.grid(row=0,column=4,padx=10,pady=10)
##Move Down
move_down_button = Button(button_frame,text="Move Down",command=down)
move_down_button.grid(row=0,column=5,padx=10,pady=10)
##Clean Entry Box
cle_button = Button(button_frame,text="Clean Entry Box",command=clean_entries)
cle_button.grid(row=0,column=6,padx=10,pady=10)

#Bind treeview
tree_stock.bind("<ButtonRelease-1>", sel_record)

view_database()

inventory.mainloop()

