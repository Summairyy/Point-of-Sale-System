from tkinter import *
from tkinter import ttk
import sqlite3

root  = Tk()
root.title("Point of Sale")
root.geometry("1350x750+0+0")
root.configure(bg = "#d9d9d9")

in_carts = []
id_list = []
qty_list = []
list_total = []
incart_id = 0
payment_var = StringVar(value="Please input")
cusid_var = StringVar()
#==================Customers==================
def cus_search():
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute("SELECT * FROM customers WHERE customer_id like ?",(cusid_entry.get(),))
    theid = c.fetchall()
    for cusdata in theid:
        cusname_entry.insert(0,cusdata[2]+' '+cusdata[3])
        cusno_entry.insert(0,cusdata[4])
    conn.commit()
    conn.close()

def cus_edit():
    import database_customers

def cus_del():
    cusid_entry.delete(0,END)
    cusname_entry.delete(0,END)
    cusno_entry.delete(0,END)

#===================Product===================
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
##Open INVENTORY Window    
def inventory_open():
    import database_pos

def search_records():
    lookup_record = pd_entry.get()
    for record in tree_stock.get_children():
        tree_stock.delete(record)
    pd_entry.delete(0,END)
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

def sel_item():
    global list_total
    selected = tree_stock.focus()
    item_id = tree_stock.item(selected)['values'][0]
    item = list(tree_stock.item(selected)['values'][0:3])
    qty_stock = tree_stock.item(selected)['values'][3]
    if qty_stock == 0:
            pass
    elif item_id in id_list:
        qty = qty_list[in_carts.index(item)] + 1
        new_item = list(tree_stock.item(selected)['values'][0:3])+[qty]
        print(incart_id)
        tree_cart.item('I00'+str(in_carts.index(item)+1+incart_id), values=new_item)
        qty_list[in_carts.index(item)] = qty
        qty_stock = [qty_stock- 1]
        tree_stock.item(selected,values=item+qty_stock)
    else:
        qty_list.append(1)
        in_carts.append(item)
        id_list.append(in_carts[in_carts.index(item)][0])
        tree_cart.insert("",END,values=(item+[1]))
        qty_stock = [qty_stock - 1]
        tree_stock.item(selected,values=item+qty_stock)
    list_total = []
    total_entry.delete(0,END)
    subtt_entry.delete(0,END)
    tax_entry.delete(0,END)
    
    for price_pd in tree_cart.get_children():
        price = int(tree_cart.item(price_pd,'values')[2])
        qty_int = int(tree_cart.item(price_pd,'values')[3])
        cal_total = price * qty_int
        list_total.append(cal_total)
    list_total = sum(list_total)
    tax_cal = 0.07*list_total
    sub_total_cal = list_total - tax_cal

    total_entry.insert(0,list_total)
    tax_entry.insert(0,'%.2f'%tax_cal)
    subtt_entry.insert(0,'%.2f'%sub_total_cal)

def calculate():
    global list_total
    total_entry.delete(0,END)

    pay = payment_entry.get()
    change_cal = int(pay) - list_total

    total_entry.insert(0,list_total)
    change_entry.insert(0,'%.2f'%change_cal)
    #Update Database
    conn = sqlite3.connect('pos.db')
    c = conn.cursor()
    for i in range(len(id_list)):
        q = qty_list[i]
        id = id_list[i]
        c.execute('UPDATE stock SET quatity = quatity - ? WHERE oid = ?',(q,id))

    conn.commit()
    conn.close()


def clean_bill():
    global list_total, in_carts, id_list, qty_list,incart_id
    for record in tree_cart.get_children():
        tree_cart.delete(record)
    total_entry.delete(0,END)
    subtt_entry.delete(0,END)
    tax_entry.delete(0,END)
    change_entry.delete(0,END)
    payment_entry.delete(0,END)
    cusid_entry.delete(0,END)
    cusname_entry.delete(0,END)
    cusno_entry.delete(0,END)
    incart_id  = incart_id + len(in_carts)
    list_total = []
    in_carts = []
    id_list = []
    qty_list = []
    list_total = []

def remove():
    x = tree_cart.selection()[0]
    tree_cart.delete(x)
    total_entry.delete(0,END)
    subtt_entry.delete(0,END)
    tax_entry.delete(0,END)
    
def click(event):
    payment_entry.configure(state=NORMAL)
    payment_entry.delete(0, END)
    payment_entry.unbind('<Button-1>', clicked)

def print_bill():
    bill =Tk()
    bill.title("Receipt Bill")
    bill.geometry("400x550")
    bill_frame = Frame(bill,background="white",bd=2,relief=GROOVE)
    bill_frame.place(x=10,y=10,width=380,height=500)
    bill_area = Text(bill_frame,font=('Cascadia Code',13),bg="white",fg="black")
    bill_area.pack(fill=BOTH,expand=1)
    bill_area.insert(END,f"\t    Mobile Shop")
    bill_area.insert(END,f"\n -----------------------------------")
    bill_area.insert(END,f"\n Customer ID: {cusid_entry.get()}")
    bill_area.insert(END,f"\n Cus Name: {cusname_entry.get()}")
    bill_area.insert(END,f"\n Phone No: {cusno_entry.get()}")
    bill_area.insert(END,f"\n -----------------------------------")
    bill_area.insert(END,f"\n Product\t\t\tPrice  Qty ")
    bill_area.insert(END,f"\n -----------------------------------")
    for pd in range(len(in_carts)):
        qua = qty_list[pd]
        prod = in_carts[pd]
        pdname = prod[1]
        pdqua = prod[2]
        bill_area.insert(END,f"\n {pdname}\t\t\t{pdqua}\t{qua}")
    bill_area.insert(END,f"\n ===================================")
    bill_area.insert(END,f"\n\t\t Sub Total  {subtt_entry.get()}")
    bill_area.insert(END,f"\n\t\t Tax(7%)    {tax_entry.get()}")
    bill_area.insert(END,f"\n\t\t Total      {total_entry.get()}")
    bill_area.insert(END,f"\n\t\t Cash       {payment_entry.get()}")
    bill_area.insert(END,f"\n\t\t Change     {change_entry.get()}")
    clean_bill()
    bill.mainloop()
    
#=================FRAME======================#
main_frame = Frame(root,bd=8,background="#d9d9d9")
main_frame.place(x=0,y=0,width=1350,height=750)
#----------------------------------------------#
#Top Frame
top_frame = Frame(root,background="black",bd=2,relief=RIDGE)
top_frame.place(x=8,y=8,width=1334,height=50)
top_lbl = Label(top_frame,text="Point of Sale : Mobile Shop",font=('Cascadia Code',17,'bold'),bg="black",fg="white")
top_lbl.place(x=4,y=5)
#Items list Frame
items_frame = Frame(root,background="white",bd=2,relief=RIDGE)
items_frame.place(x=8,y=62,width=920,height=570)

itm_list_f = Frame(items_frame,background="#FFB2A5",bd=2,relief=GROOVE)
itm_list_f.place(x=8,y=8,width=900,height=40)
itm_lbl = Label(itm_list_f,text="Items List",font=('Cascadia Code',17,'bold'),bg="#FFB2A5",fg="white")
itm_lbl.place(x=3,y=0)

pd_frame = Frame(items_frame,background="#F9F6E5",bd=2,relief=GROOVE)
pd_frame.place(x=8,y=54,width=900,height=504)
#----------------tree view--------------------------------------------
# Create Treeview Frame & Scrollbar
tree_farme = Frame(pd_frame)
tree_farme.place(x=40,y=50,height=430)
tree_scroll = Scrollbar(tree_farme)
tree_scroll.pack(side=RIGHT,fill=Y)
# Create Treeview
tree_stock = ttk.Treeview(tree_farme,yscrollcommand=tree_scroll.set,selectmode="extended",height=430)
tree_stock.pack()
tree_scroll.config(command=tree_stock.yview)
#Format Column
tree_stock['columns'] = ("Product ID","Product Name","Price","Quatity")
tree_stock.column("#0",width=0,stretch=NO)
tree_stock.column("Product ID",anchor=CENTER,width=150)
tree_stock.column("Product Name",anchor=CENTER,width=320)
tree_stock.column("Price",anchor=CENTER,width=150)
tree_stock.column("Quatity",anchor=CENTER,width=150)
#Heading
tree_stock.heading("#0")
tree_stock.heading("Product ID",text="Product ID", anchor=CENTER)
tree_stock.heading("Product Name",text="Product Name", anchor=CENTER)
tree_stock.heading("Price",text="Price", anchor=CENTER)
tree_stock.heading("Quatity",text="Quatity", anchor=CENTER)

tree_stock.tag_configure('oddrow',background="white")
tree_stock.tag_configure('evenrow',background="#FAD5A5")  
#-----------------------------------------------------------------------
pd_lbl = Label(pd_frame,text="Product Name :",background="#F9F6E5",font=('Cascadia Code',14))
pd_lbl.place(x=8,y=2)
pd_entry = Entry(pd_frame,textvariable="",font=14)
pd_entry.place(x=180,y=8,width=480)
search_btn = Button(pd_frame,text="Search",font=('Cascadia Code',12),command=search_records)
search_btn.place(x=670,y=8,width=100,height=28)
refresh_btn = Button(pd_frame,text="Refresh",font=('Cascadia Code',12),command=view_database)
refresh_btn.place(x=780,y=8,width=100,height=28)
#-----------------------------------------------------------------------
#Invoice Frame
invoice_frame = Frame(root,background="white",bd=2,relief=RIDGE)
invoice_frame.place(x=933,y=62,width=408,height=678)
    ##CUSTOMERS FRAME
cus_invoice_frame = Frame(invoice_frame,background="white",bd=2,relief=GROOVE)
cus_invoice_frame.place(x=8,y=8,width=390,height=150)
mobile_shop = Label(cus_invoice_frame,text="Mobile Shop",font=('Cascadia Code',13),bg="white",fg="#A07462")
mobile_shop.place(x=135,y=1)

cus_id = Label(cus_invoice_frame,text="Customer ID:",font=('Cascadia Code',13),bg="white")
cus_id.place(x=3,y=30)
cusid_entry = Entry(cus_invoice_frame,textvariable=cusid_var,font=14,bg="#FBFBFB")
cusid_entry.place(x=150,y=30,width=170)

cus_name = Label(cus_invoice_frame,text="Customer Name:",font=('Cascadia Code',13),bg="white")
cus_name.place(x=3,y=65)
cusname_entry = Entry(cus_invoice_frame,textvariable="",font=14,bg="#FBFBFB")
cusname_entry.place(x=150,y=70,width=170)

cus_no = Label(cus_invoice_frame,text="Phone Number:",font=('Cascadia Code',13),bg="white")
cus_no.place(x=3,y=105)
cusno_entry = Entry(cus_invoice_frame,textvariable="",font=14,bg="#FBFBFB")
cusno_entry.place(x=150,y=110,width=170)

serach_cusid = Button(cus_invoice_frame,text="Search",command=cus_search)
serach_cusid.place(x=330,y=30)
edit_cus = Button(cus_invoice_frame,text="Edit",command=cus_edit)
edit_cus.place(x=330,y=70,width=45)
del_entry = Button(cus_invoice_frame,text="Clear",command=cus_del)
del_entry.place(x=330,y=110,width=45)
    ##CART FRAME
cart_frame = Frame(invoice_frame,background="white",bd=2,relief=GROOVE)
cart_frame.place(x=8,y=163,width=390,height=290)

# def view_tree_cart():
# Create Treeview
tree_cart = ttk.Treeview(cart_frame,yscrollcommand=tree_scroll.set,selectmode="extended",height=430)
tree_cart.pack()
tree_scroll.config(command=tree_cart.yview)
#Format Column
tree_cart['columns'] = ("Product ID","Product Name","Price","Quatity")
tree_cart.column("#0",width=0,stretch=NO)
tree_cart.column("Product ID",anchor=CENTER,width=80)
tree_cart.column("Product Name",anchor=CENTER,width=140)
tree_cart.column("Price",anchor=CENTER,width=80)
tree_cart.column("Quatity",anchor=CENTER,width=80)
#Heading
tree_cart.heading("#0")
tree_cart.heading("Product ID",text="Product ID", anchor=CENTER)
tree_cart.heading("Product Name",text="Product Name", anchor=CENTER)
tree_cart.heading("Price",text="Price", anchor=CENTER)
tree_cart.heading("Quatity",text="Quatity", anchor=CENTER)

tree_cart.tag_configure('oddrow',background="white")
tree_cart.tag_configure('evenrow',background="white")  
    ##TOTAL FRAME
total_frame = Frame(invoice_frame,background="white",bd=2,relief=GROOVE)
total_frame.place(x=8,y=458,width=390,height=160)

sub_total = Label(total_frame,text="Sub Total",font=('Cascadia Code',13),bg="white")
sub_total.place(x=3,y=1)
subtt_entry = Entry(total_frame,textvariable="",font=14,bg="white",justify = "right")
subtt_entry.place(x=210,y=3,width=170)

tax = Label(total_frame,text="Tax (7%)",font=('Cascadia Code',13),bg="white")
tax.place(x=3,y=30)
tax_entry = Entry(total_frame,textvariable="",font=14,bg="white",justify = "right")
tax_entry.place(x=210,y=34,width=170)

total = Label(total_frame,text="Total",font=('Cascadia Code',13),bg="white")
total.place(x=3,y=60)
total_entry = Entry(total_frame,textvariable="",font=14,bg="white",justify = "right")
total_entry.place(x=210,y=65,width=170)

payment = Label(total_frame,text="Payment",font=('Cascadia Code',13),bg="white")
payment.place(x=3,y=90)
payment_entry = Entry(total_frame,textvariable=payment_var,font=14,bg="white",justify = "right")
payment_entry.place(x=210,y=95,width=170)

change = Label(total_frame,text="Change",font=('Cascadia Code',13),bg="white")
change.place(x=3,y=120)
change_entry = Entry(total_frame,textvariable="",font=14,bg="white",justify = "right")
change_entry.place(x=210,y=125,width=170)

    ##PAY NOW BUTTON
pay_btn = Button(invoice_frame,text="PAY NOW",font=('Cascadia Code',16),bg="#C20114",fg="white",command=calculate)
pay_btn.place(x=8,y=625,width=390,height=40)
#Button Frame
btn_frame = Frame(root,background="white",bd=2,relief=RIDGE)
btn_frame.place(x=8,y=635,width=920,height=105)

inv_btn = Button(btn_frame,text="INVENTORY",font=('Cascadia Code',18),bg="#83D6E7",command=inventory_open)
inv_btn.place(x=20,y=14,width=350,height=70)

add_btn = Button(btn_frame,text="Add to Cart",font=('Cascadia Code',16),bg="#FFB2A5",command=sel_item)
add_btn.place(x=380,y=14,width=150,height=70)

clean_btn = Button(btn_frame,text="CLEAN",font=('Cascadia Code',16),bg="#FFB2A5",command=clean_bill)
clean_btn.place(x=540,y=14,width=100,height=70)

remove_btn = Button(btn_frame,text="Remove One",font=('Cascadia Code',16),bg="#FFB2A5",command=remove)
remove_btn.place(x=650,y=14,width=150,height=70)

print_btn = Button(btn_frame,text="PRINT",font=('Cascadia Code',16),bg="#FFB2A5",command=print_bill)
print_btn.place(x=810,y=14,width=100,height=70)

tree_stock.bind("<ButtonRelease-1>",sel_item)
clicked = payment_entry.bind('<Button-1>', click)
view_database()

root.mainloop()

