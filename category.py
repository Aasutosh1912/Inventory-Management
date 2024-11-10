
from tkinter import * 

from tkinter import ttk,messagebox
from employee import connect_database



def delete_category(treeview):
    index=treeview.selection()
    content=treeview.item(index)
    row=content['values']
    id=row[0]
    if not index:
        messagebox.showerror('Error','No row is selected')
        return
    cursor,connect=connect_database()
    if not cursor or not connect:
        return
    cursor.execute('use inventory_system')
    cursor.execute('DELETE FROM category_data WHERE id=%s',(id,))
    connect.commit()
    treeview_data(treeview)
    messagebox.showinfo("Info","Record is deleted")




def clear(id_entry,category_name_entry,description_text):
    id_entry.delete(0,END)
    category_name_entry.delete(0,END)
    description_text.delete(1.0,END)


def treeview_data(treeview):
    cursor,connect=connect_database()
    if not cursor or not connect:
        return
    try:
        cursor.execute('use inventory_system')
        cursor.execute('Select * from category_data')
        records=cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('',END,values=record)
    except Exception as e:
        messagebox.showerror('Error',f'Error due to {e}')

    finally:
        cursor.close()
        connect.close()



def add_category(id,name,description,treeview):
    if id=='' or name=='' or description=='':
        messagebox.showerror('Error','All fields are required')

    else:
        cursor,connect=connect_database()
        if not cursor or not connect:
            return
        cursor.execute("Use inventory_system")
        cursor.execute('CREATE TABLE IF NOT EXISTS category_data (id INT PRIMARY KEY, name VARCHAR(100),description TEXT)')
        cursor.execute('SELECT * from category_data WHERE id=%s',(id,))
            
        if cursor.fetchone():
            messagebox.showerror('ERROR','Id already exists')

        cursor.execute('INSERT INTO category_data VALUES(%s,%s,%s)',(id,name,description.strip()))
        connect.commit()
        messagebox.showinfo('Info','Data is inserted')
        treeview_data(treeview)


def category_form(root):
    global back_image,logo
    category_frame=Frame(root,width=1070,height=567,bg='white')
    category_frame.place(x=200,y=100)
    headingLabel=Label(category_frame,text= 'Manage Category Details', font=('times new roman',16,'bold'),bg='#0f4d7d',fg='white')  
    headingLabel.place(x=0,y=0,relwidth=1)

    back_image=PhotoImage(file='back.png')
    back_Button=Button(category_frame,image=back_image,bd=0,cursor='hand2',bg='white',command=lambda:category_frame.place_forget())
    back_Button.place(x=0,y=30)

    logo=PhotoImage(file='product_category.png')
    label=Label(category_frame,image=logo,bg='white')
    label.place(x=30,y=100)


    details_frame=Frame(category_frame,bg='white')
    details_frame.place(x=500,y=60)

    id_label=Label(details_frame,text='Id',font=('times new roman',14,'bold'),bg='white')
    id_label.grid(row=0,column=0,padx=20,sticky='w')
    id_entry=Entry(details_frame,font=('times new roman',14,'bold'),bg='Lightyellow')
    id_entry.grid(row=0,column=1)


    category_name_label=Label(details_frame,text='Category Name',font=('times new roman',14,'bold'),bg='white')
    category_name_label.grid(row=1,column=0,padx=20,sticky='w')
    category_name_entry=Entry(details_frame,font=('times new roman',14,'bold'),bg='Lightyellow')
    category_name_entry.grid(row=1,column=1,pady=20)


    description_label=Label(details_frame,text='Description',font=('times new roman',14,'bold'),bg='white')
    description_label.grid(row=2,column=0,padx=20,sticky='nw')
    description_text=Text(details_frame,width=25,height=6,bd=2,bg='Lightyellow')
    description_text.grid(row=2,column=1)


    button_frame=Frame(category_frame,bg='white')
    button_frame.place(x=580,y=280)

    add_button=Button(button_frame,text="Add",font=('times new roman',14),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda: add_category(id_entry.get(),category_name_entry.get(),description_text.get(1.0,END).strip(),treeview))
    add_button.grid(row=0,column=0,padx=20)


    delete_button=Button(button_frame,text="Delete",font=('times new roman',14),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda: delete_category(treeview))
    delete_button.grid(row=0,column=1,padx=20)

    clear_button=Button(button_frame,text="Clear",font=('times new roman',14),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda: clear(id_entry,category_name_entry,description_text))
    clear_button.grid(row=0,column=2,padx=20)

    treeview_frame=Frame(category_frame,bg='yellow')
    treeview_frame.place(x=530,y=340,height=200,width=500)

    scrolly=Scrollbar(treeview_frame,orient=VERTICAL)
    scrollx=Scrollbar(treeview_frame,orient=HORIZONTAL)

    treeview=ttk.Treeview(treeview_frame,columns=('Id','Name','Description'),show='headings',yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
    scrolly.pack(side=RIGHT,fill=Y)
    scrollx.pack(side=BOTTOM,fill=X)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)


    treeview.pack(fill=BOTH,expand=1)
    treeview.heading('Id',text='Id')
    treeview.heading('Name',text='Category Name')
    treeview.heading('Description',text='Description')
    
    treeview.column('Id',width=80)
    treeview.column('Name',width=140)
    
    treeview.column('Description',width=300)

    treeview_data(treeview)