from tkinter import * 

from tkinter import ttk,messagebox
from employee import connect_database


def sales_form(root):
    global back_image

    sales_frame=Frame(root,width=1070,height=567,bg='white')
    sales_frame.place(x=200,y=100)

    topFrame=Frame(sales_frame,bg="white",relief=RIDGE)
    topFrame.place(x=50,y=110)

    back_image=PhotoImage(file='back.png')
    back_button=Button(sales_frame,image=back_image,bd=0,cursor='hand2',bg='white',command=lambda: sales_frame.place_forget())
    back_button.place(x=0,y=50)

    headingLabel=Label(sales_frame,text= 'View Customer Bills', font=('times new roman',25,'bold'),bg='#0f4d7d',fg='white')  
    headingLabel.place(x=0,y=0,relwidth=1)
    

    

    num_label=Label(topFrame,text='Invoice No.',font=('times new roman',14,'bold'),bg='white')
    num_label.grid(row=0,column=0,padx=(0,15),sticky='w')
    search_entry=Entry(topFrame,font=('times new roman',14,'bold'),bg='Lightyellow',width=20)
    search_entry.grid(row=0,column=1)


    search_button=Button(topFrame,text="Search",font=('times new roman',14),width=8,cursor='hand2',fg='white',bg='#0f4d7d')
    search_button.grid(row=0,column=2,padx=15)


    show_button=Button(topFrame,text="Show All",font=('times new roman',14),width=8,cursor='hand2',fg='white',bg='#0f4d7d')
    show_button.grid(row=0,column=3)

    left_frame=Frame(sales_frame,bg='white',height=450,width=250)
    left_frame.place(x=50,y=180)

    scrolly=Scrollbar(left_frame,orient=VERTICAL)
    scrollx=Scrollbar(left_frame,orient=HORIZONTAL)

    treeview=ttk.Treeview(left_frame,yscrollcommand=scrolly.set,xscrollcommand=scrollx.set,height=15)
    scrolly.pack(side=RIGHT,fill=Y)
    scrollx.pack(side=BOTTOM,fill=X)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)

    treeview.pack(fill=BOTH,expand=1)
