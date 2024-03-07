from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

customers = Tk()
customers.title("Database POS")
customers.geometry("750x570")

row_id = StringVar()
#====================database=========================
conn = sqlite3.connect('customers.db')
c = conn.cursor()
#Create tablea
c.execute("""CREATE TABLE IF NOT EXISTS customers (
                row_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id text,
                first_name text,
                last_name text,
                phone_num int)""")

conn.commit()
conn.close()
#-------------------------------------------------------
def view_cus_database():
    for record in tree_cus.get_children():
        tree_cus.delete(record)

    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute("SELECT * FROM customers")
    records = c.fetchall()
    #Add data to the screen
    global count
    count = 0
    for record in records:
        print(record)

    for record in records:
        if count % 2 == 0:
            tree_cus.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3],record[4]),tags=('evenrow',))
        else:
            tree_cus.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3],record[4]),tags=('oddrow',))
        count += 1  
    
    conn.commit()
    conn.close()

def search_records():
    lookup_record = search_entry.get()
    for record in tree_cus.get_children():
        tree_cus.delete(record)
    search_entry.delete(0,END)
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute("SELECT * FROM customers WHERE customer_id like ?",(lookup_record,))
    records = c.fetchall()
    #Add data to the screen
    global count
    count = 0
    for record in records:
        print(record)

    for record in records:
        if count % 2 == 0:
            tree_cus.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3],record[4]),tags=('evenrow',))
        else:
            tree_cus.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3],record[4]),tags=('oddrow',))
        count += 1  
    
    conn.commit()
    conn.close()
#Remove one data
def remove_one():
    x = tree_cus.selection()[0]
    tree_cus.delete(x)

    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute("DELETE from customers WHERE customer_id=" + cid_entry.get())
    conn.commit()
    conn.close()
    clean_entries()

#Clean entry box
def clean_entries():
    row_id.set("")
    cid_entry.delete(0,END)
    fname_entry.delete(0,END)
    lname_entry.delete(0,END)
    phone_entry.delete(0,END) 
#Select Record
def sel_record(e):
    cid_entry.delete(0,END)
    fname_entry.delete(0,END)
    lname_entry.delete(0,END)
    phone_entry.delete(0,END) 

    selected = tree_cus.focus()
    values = tree_cus.item(selected,'values')
    #output to entry boxs
    row = values[0]
    row_id.set(row)
    cid_entry.insert(0,values[1])
    fname_entry.insert(0,values[2])
    lname_entry.insert(0,values[3])
    phone_entry.insert(0,values[4])
#Update Data
def update_record():
    selected = tree_cus.focus()
    tree_cus.item(selected,text="",values=(row_entry.get(),cid_entry.get(),fname_entry.get(),lname_entry.get(),phone_entry.get(),))
    
    #Update Database
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute("""UPDATE customers SET
            customer_id =?,
            first_name = ?,
            last_name = ?,
            phone_num = ?

            WHERE oid = ?""",
            (
                cid_entry.get(),
                fname_entry.get(),
                lname_entry.get(),
                phone_entry.get(),
                row_entry.get()
            ))

    conn.commit()
    conn.close()
    clean_entries()
#Add data
def add_data():  
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute("INSERT INTO customers (customer_id,first_name,last_name,phone_num) VALUES ( :cus_id, :f_name,:l_name, :phone_num)",
              {
                'cus_id': cid_entry.get(),
                'f_name': fname_entry.get(),
                'l_name': lname_entry.get(),
                'phone_num': phone_entry.get()
              })

    conn.commit()
    conn.close()
    clean_entries()

    tree_cus.delete(*tree_cus.get_children())
    view_cus_database()
#==================================================================
style = ttk.Style()
style.theme_use('default')
style.configure("Treeview",bg="#D3D3D3",fg="black",rowheight=25,fieldbackground="#D3D3D3")

style.map('Treeview',background=[('selected',"#a38767")])
#===========Search============================
search_frame = LabelFrame(customers,text="Search Records")
search_frame.pack(fill=X,expand="yes",padx=20)
saerch_lbl = Label(search_frame,text="Customer ID :")
saerch_lbl.grid(row=0,column=0,padx=8,pady=8)
search_entry = Entry(search_frame,font=10,width=35)
search_entry.grid(row=0,column=1,padx=8,pady=8)
search_btn = Button(search_frame,text="Search",width=10,command=search_records)
search_btn.grid(row=0,column=2,padx=8,pady=8)
refresh_btn = Button(search_frame,text="Refresh table",width=10,command=view_cus_database)
refresh_btn.grid(row=0,column=3,padx=8,pady=8)
# Create Treeview Frame & Scrollbar
tree_farme = Frame(customers)
tree_farme.pack(pady=10)
tree_scroll = Scrollbar(tree_farme)
tree_scroll.pack(side=RIGHT,fill=Y)
# Create Treeview
tree_cus = ttk.Treeview(tree_farme,yscrollcommand=tree_scroll.set,selectmode="extended")
tree_cus.pack()
tree_scroll.config(command=tree_cus.yview)
#Format Column
tree_cus['columns'] = ("Row ID","Customer ID","First Name","Last Name","Phone Number")
tree_cus.column("#0",width=0,stretch=NO)
tree_cus.column("Row ID",anchor=CENTER,width=100)
tree_cus.column("Customer ID",anchor=CENTER,width=100)
tree_cus.column("First Name",anchor=CENTER,width=180)
tree_cus.column("Last Name",anchor=CENTER,width=180)
tree_cus.column("Phone Number",anchor=CENTER,width=130)
#Heading
tree_cus.heading("#0")
tree_cus.heading("Row ID",text="Row ID", anchor=CENTER)
tree_cus.heading("Customer ID",text="Customer ID", anchor=CENTER)
tree_cus.heading("First Name",text="First Name", anchor=CENTER)
tree_cus.heading("Last Name",text="Last Name", anchor=CENTER)
tree_cus.heading("Phone Number",text="Phone Number", anchor=CENTER)

tree_cus.tag_configure('oddrow',background="white")
tree_cus.tag_configure('evenrow',background="#FAD5A5")  


#=========Add Record==========================
data_frame = LabelFrame(customers,text="Record")
data_frame.pack(fill="x", expand="yes",padx=20)
##Customer ID
cid_label = Label(data_frame,text="Customer ID")
cid_label.grid(row=0,column=0,padx=10,pady=10)
cid_entry = Entry(data_frame)
cid_entry.grid(row=0,column=1,padx=10,pady=10)
##First Name
fname_label = Label(data_frame,text="First Name")
fname_label.grid(row=1,column=0,padx=10,pady=10)
fname_entry = Entry(data_frame)
fname_entry.grid(row=1,column=1,padx=10,pady=10)
##Last Name
lname_label = Label(data_frame,text="Last Name")
lname_label.grid(row=1,column=2,padx=10,pady=10)
lname_entry = Entry(data_frame)
lname_entry.grid(row=1,column=3,padx=10,pady=10)
##Phone No.
phone_label = Label(data_frame,text="Phone No.")
phone_label.grid(row=0,column=2,padx=10,pady=10)
phone_entry = Entry(data_frame)
phone_entry.grid(row=0,column=3,padx=10,pady=10)
##Roe ID
row_label = Label(data_frame,text="Row ID")
row_label.grid(row=1,column=4,padx=10,pady=10)
row_entry = Entry(data_frame,textvariable=row_id,state=DISABLED)
row_entry.grid(row=1,column=5,padx=10,pady=10)

#============Add Button========================
button_frame = LabelFrame(customers,text="Commands")
button_frame.pack(fill="x",expand="yes",padx=20)
##Update Data
upd_button = Button(button_frame,text="Update Data",command=update_record)
upd_button.grid(row=0,column=0,padx=10,pady=10)
##Add Data
add_button = Button(button_frame,text="Add Data",command=add_data)
add_button.grid(row=0,column=1,padx=10,pady=10)
##Remove one data
re_one_button = Button(button_frame,text="Remove one data",command=remove_one)
re_one_button.grid(row=0,column=2,padx=10,pady=10)
##Clean Entry Box
cle_button = Button(button_frame,text="Clean Entry Box",command=clean_entries)
cle_button.grid(row=0,column=3,padx=10,pady=10)

tree_cus.bind("<ButtonRelease-1>", sel_record)
view_cus_database()
customers.mainloop()