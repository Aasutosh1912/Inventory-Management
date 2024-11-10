from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from employee import connect_database

def show_all(search_combo,search_entry,treeview_a):
    treeview_data(treeview_a)
    search_entry.delete(0,END)
    search_combo.set('Search By')


def search_product(search_combo,search_entry,treeview_a):
    if search_entry.get()=="":
        messagebox.showerror("Error","Enter Value To Search")
    elif search_combo.get()=='Search By':
        messagebox.showerror("Error","Please Select an Option")
    else:
        cursor,connect=connect_database()
        if not cursor or not connect:
            return
        cursor.execute("Use inventory_system")
        cursor.execute(f"select * from product_data where {search_combo.get()}=%s",(search_entry.get(),))
        records=cursor.fetchall()
        if len(records)==0:
            messagebox.showerror("Error","No Records Found")
            return

        treeview_a.delete(*treeview_a.get_children())
        for record in records:
            treeview_a.insert('',END,values=record)

def clear_fields(category_combo,supply_combo,name_entry,price_entry,qty_entry,status_combo,treeview_a):
    treeview_a.selection_remove(treeview_a.selection())
    name_entry.delete(0,END)
    price_entry.delete(0,END)
    qty_entry.delete(0,END)
    category_combo.set("Select")
    supply_combo.set("Select")
    status_combo.set("Select Status")

def delete_product(treeview_a,category_combo,supply_combo,name_entry,price_entry,qty_entry,status_combo):
    index=treeview_a.selection()
    dict=treeview_a.item(index)
    content=dict['values']
    id=content[0]
    if not index:
        messagebox.showerror("Error","No row selected")
        return
    data=messagebox.askyesno("Confirm","Do you really want to delete?")
    if data:
        cursor,connect=connect_database()
        if not cursor or not connect:
            return
        try:
            cursor.execute("Use inventory_system")
            cursor.execute("Delete from product_data where id=%s",(id,))
            connect.commit()
            messagebox.showinfo("Success","Data Deleted")
            clear_fields(category_combo,supply_combo,name_entry,price_entry,qty_entry,status_combo,treeview_a)
        except Exception as e:
            messagebox.showerror("Error",f"Error Due to {e}")

        finally:
            cursor.close()
            connect.close()
        
    


def update_product(category,supplier,name,price,qty,status,treeview_a):
    index=treeview_a.selection()
    dict=treeview_a.item(index)
    content=dict['values']
    id=content[0]
    if not index:
        messagebox.showerror("Error","No row selected")
        return
    cursor,connect=connect_database()
    if not cursor or not connect:
        return
    cursor.execute("Use inventory_system")
    cursor.execute("select * from product_data where id=%s",(id,))
    current_data=cursor.fetchone()
    current_data=current_data[1:]
    current_data=list(current_data)
    current_data[3]=str(current_data[3])
    current_data=tuple(current_data)

    qty=int(qty)
    new_data=(category,supplier,name,price,qty,status)

    if current_data==new_data:
        messagebox.showinfo("Info",'No changes Detected')
        return
    
    cursor.execute("Update product_data set category=%s,supplier=%s,name=%s,price=%s,quantity=%s,status=%s where id=%s",(category,supplier,name,price,qty,status,id))
    connect.commit()
    messagebox.showinfo("Info","Data is updated")
    treeview_data(treeview_a)

def select_data(event,treeview_a,category_combo,supply_combo,name_entry,price_entry,qty_entry,status_combo):
    index=treeview_a.selection()
    dict=treeview_a.item(index)
    content=dict['values']
    name_entry.delete(0,END)
    price_entry.delete(0,END)
    qty_entry.delete(0,END)
    category_combo.set(content[1])
    supply_combo.set(content[2])
    name_entry.insert(0,content[3])
    price_entry.insert(0,content[4])
    qty_entry.insert(0,content[5])
    status_combo.set(content[6])




def treeview_data(treeview_a):
    cursor,connect=connect_database()
    if not cursor or not connect:
        return
    try:
        cursor.execute("Use inventory_system")
        cursor.execute("select * from product_data")
        records=cursor.fetchall()
        treeview_a.delete(*treeview_a.get_children())
        for record in records:
            treeview_a.insert('',END,values=record)
    except Exception as e:
        messagebox.showerror("Error",f"Error Due to {e}")

    finally:
        cursor.close()
        connect.close()


def fetch_supplier_category(category_combo,supply_combo):
    category_option=[]
    supply_option=[]
    cursor,connect=connect_database()
    if not cursor or not connect:
        return
    cursor.execute("Use inventory_system")
    cursor.execute("select name from category_data")
    names=cursor.fetchall()
    if len(names)>0:
        category_combo.set("Select")
        for name in names:
            category_option.append(name[0])
        category_combo.config(values=category_option)

    cursor.execute("select name from supplier_data")
    names=cursor.fetchall()
    if len(names)>0:
        supply_combo.set("Select")
        for name in names:
            supply_option.append(name[0])
        supply_combo.config(values=supply_option)

def add_product(category,supplier,name,price,qty,status,treeview_a):
    if category=='Empty':
        messagebox.showerror("Error","Please Add Category")
    elif supplier=="Empty":
        messagebox.showerror("Error","Please Add Supplier")
    elif category=='Select' or supplier=="Select" or name=="" or price=="" or qty=="" or status=="Select Status":
        messagebox.showerror("Error","All Fields Required")
    else:
        cursor,connect=connect_database()
        if not cursor or not connect:
            return
        cursor.execute("Use inventory_system")
        cursor.execute("create table if not exists product_data(id INT AUTO_INCREMENT PRIMARY KEY,category VARCHAR(100),supplier VARCHAR(100),name VARCHAR(100),price DECIMAL(10,2),quantity INT,status VARCHAR(50))")
        
        cursor.execute("select * from product_data where category=%s and supplier=%s and name=%s",(category,supplier,name))
        existing_product=cursor.fetchone()
        if existing_product:
            messagebox.showerror("Error",'Product alredy exist')
            return


        cursor.execute("Insert into product_data (category,supplier,name,price,quantity,status) values(%s,%s,%s,%s,%s,%s)",(category,supplier,name,price,qty,status))
        connect.commit()
        messagebox.showinfo("Success","Product Added")
        treeview_data(treeview_a)

def product_form(root):
    global back_image

    product_frame=Frame(root,width=1070,height=567,bg='white')
    product_frame.place(x=200,y=100)

    leftFrame=Frame(product_frame,bg="white",bd=2,relief=RIDGE)
    leftFrame.place(x=20,y=40)

    back_image=PhotoImage(file='back.png')
    back_button=Button(product_frame,image=back_image,bd=0,cursor='hand2',bg='white',command=lambda: product_frame.place_forget())
    back_button.place(x=10,y=10)

    heading_label=Label(leftFrame,text='Manage Product Details',font=('times new roman',16,'bold'),bg='#0f4d7d',fg='white')
    heading_label.grid(row=0,columnspan=2,sticky='we')

    categorylabel=Label(leftFrame,text="Category",font=('times new roman',14,'bold'),bg='white')
    categorylabel.grid(row=1,column=0,padx=20,sticky='w')
    category_combo=ttk.Combobox(leftFrame,font=('times new roman',14,'bold'),width=18,state='readonly')
    category_combo.grid(row=1,column=1,pady=40)
    category_combo.set('Empty')

    supplylabel=Label(leftFrame,text="Supplier",font=('times new roman',14,'bold'),bg='white')
    supplylabel.grid(row=2,column=0,padx=20,sticky='w')
    supply_combo=ttk.Combobox(leftFrame,font=('times new roman',14,'bold'),width=18,state='readonly')
    supply_combo.grid(row=2,column=1)
    supply_combo.set('Empty')

    namelabel=Label(leftFrame,text="Name",font=('times new roman',14,'bold'),bg='white')
    namelabel.grid(row=3,column=0,padx=20,sticky='w')
    name_entry=Entry(leftFrame,font=('times new roman',14,'bold'),bg='white')
    name_entry.grid(row=3,column=1,pady=40)

    pricelabel=Label(leftFrame,text="Price",font=('times new roman',14,'bold'),bg='white')
    pricelabel.grid(row=4,column=0,padx=20,sticky='w')
    price_entry=Entry(leftFrame,font=('times new roman',14,'bold'),bg='white')
    price_entry.grid(row=4,column=1)

    qtylabel=Label(leftFrame,text="Quantity",font=('times new roman',14,'bold'),bg='white')
    qtylabel.grid(row=5,column=0,padx=20,sticky='w')
    qty_entry=Entry(leftFrame,font=('times new roman',14,'bold'),bg='white')
    qty_entry.grid(row=5,column=1,pady=40)

    statuslabel=Label(leftFrame,text="Status",font=('times new roman',14,'bold'),bg='white')
    statuslabel.grid(row=6,column=0,padx=20,sticky='w')
    status_combo=ttk.Combobox(leftFrame,values=('Active','Inactive'),font=('times new roman',14,'bold'),width=18,state='readonly')
    status_combo.grid(row=6,column=1)
    status_combo.set('Select Status')

    button_frame=Frame(leftFrame,bg='white')
    button_frame.grid(row=7,columnspan=2,pady=(30,10))

    addbutton=Button(button_frame,text='Add',font=('times new roman',14,'bold'),width=8,cursor="hand2",fg='white',bg="#0f4d7d",command=lambda: add_product(category_combo.get(),supply_combo.get(),name_entry.get(),price_entry.get(),qty_entry.get(),status_combo.get(),treeview_a))
    addbutton.grid(row=0,column=0,padx=10)

    updatebutton=Button(button_frame,text='Update',font=('times new roman',14,'bold'),width=8,cursor="hand2",fg='white',bg="#0f4d7d",command=lambda: update_product(category_combo.get(),supply_combo.get(),name_entry.get(),price_entry.get(),qty_entry.get(),status_combo.get(),treeview_a))
    updatebutton.grid(row=0,column=1,padx=10)

    deletebutton=Button(button_frame,text='Delete',font=('times new roman',14,'bold'),width=8,cursor="hand2",fg='white',bg="#0f4d7d",command=lambda: delete_product(treeview_a,category_combo,supply_combo,name_entry,price_entry,qty_entry,status_combo))
    deletebutton.grid(row=0,column=2,padx=10)

    clearbutton=Button(button_frame,text='Clear',font=('times new roman',14,'bold'),width=8,cursor="hand2",fg='white',bg="#0f4d7d",command=lambda: clear_fields(category_combo,supply_combo,name_entry,price_entry,qty_entry,status_combo,treeview_a))
    clearbutton.grid(row=0,column=3,padx=10)

    search_frame=LabelFrame(product_frame,text="Search Product",font=('times new roman',14,"bold"),bg="white")
    search_frame.place(x=510,y=30)
    search_combo=ttk.Combobox(search_frame,values=("Category","Supplier","Name","Status"),font=('times new roman',14),state="readonly",width=14)
    search_combo.grid(row=0,column=0,padx=10)
    search_combo.set("Search By")

    search_entry=Entry(search_frame,font=('times new roman',14,'bold'),bg='white',width="16")
    search_entry.grid(row=0,column=1)

    searchbutton=Button(search_frame,text='Search',font=('times new roman',14,'bold'),width=8,cursor="hand2",fg='white',bg="#0f4d7d",command=lambda: search_product(search_combo,search_entry,treeview_a))
    searchbutton.grid(row=0,column=2,padx=(10,0))

    showbutton=Button(search_frame,text='Show All',font=('times new roman',14,'bold'),width=8,cursor="hand2",fg='white',bg="#0f4d7d",command=lambda: show_all(search_combo,search_entry,treeview_a))
    showbutton.grid(row=0,column=3,padx=5)

    treeview=Frame(product_frame)
    treeview.place(x=510,y=100,width=550,height=460)

    scrolly=Scrollbar(treeview,orient=VERTICAL)
    scrollx=Scrollbar(treeview,orient=HORIZONTAL)

    treeview_a=ttk.Treeview(treeview,column=("ID","Category","Supplier","Name","Price","Quantity","Status"),show="headings",yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
    
    scrolly.pack(side=RIGHT,fill=Y)
    scrollx.pack(side=BOTTOM,fill=X)
    scrollx.config(command=treeview_a.xview)
    scrolly.config(command=treeview_a.yview)
    treeview_a.pack(fill=BOTH,expand=1)

    treeview_a.heading('ID',text='ID')
    treeview_a.heading('Category',text='Category')
    treeview_a.heading('Supplier',text='Supplier')
    treeview_a.heading('Name',text='Product Name')
    treeview_a.heading('Price',text='Price')
    treeview_a.heading('Quantity',text='Quantity')
    treeview_a.heading('Status',text='Status')
    fetch_supplier_category(category_combo,supply_combo)
    treeview_data(treeview_a)
    treeview_a.bind("<ButtonRelease-1>",lambda event:select_data(event,treeview_a,category_combo,supply_combo,name_entry,price_entry,qty_entry,status_combo))
