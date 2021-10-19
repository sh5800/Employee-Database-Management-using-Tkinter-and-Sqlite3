import sqlite3
from tkinter import *
from tkinter import messagebox


class DB:
    def __init__(self):
        self.conn = sqlite3.connect("office.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS office (idn INTEGER PRIMARY KEY, name TEXT, doj TEXT, salary INTEGER)")
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def books(self):
        self.cursor.execute("SELECT * FROM office")
        rows = self.cursor.fetchall()
        return rows

    def insert(self, name, doj, salary):
        self.cursor.execute(
            "INSERT INTO office VALUES(NULL,?,?,?)", (name, doj, salary))
        self.conn.commit()

    def search(self, name="", doj="", salary=""):
        self.cursor.execute(
            "SELECT * FROM office WHERE name=? OR doj=? OR salary=?", (name, doj, salary))
        found_rows = self.cursor.fetchall()
        return found_rows

    def update(self, idn, name, doj, salary):
        self.cursor.execute(
            "UPDATE office SET name=?, doj=?, salary=?, idn=?", (name, doj, salary, idn))

    def delete(self, idn):
        self.cursor.execute("DELETE from office WHERE idn=?", (idn))
        self.conn.commit()


db = DB()


def get_selected_row(event):
    global selected_tuple
    index = list1.curselection()[0]
    selected_tuple = list1.get(index)
    e1.delete(0, END)
    e1.insert(END, selected_tuple[1])
    e2.delete(0, END)
    e2.insert(END, selected_tuple[2])
    e3.delete(0, END)
    e3.insert(END, selected_tuple[3])


def view_command():
    list1.delete(0, END)
    for row in db.view():
        list1.insert(END, row)


def search_command():
    list1.delete(0, END)
    for row in db.search(ID_text.get(), Name_text.get(), Salary_text.get()):
        list1.insert(END, row)


def add_command():
    db.insert(title_text.get(), Name_text.get(), Salary_text.get())
    list1.delete(0, END)
    list1.insert(END, (ID_text.get(), Name_text.get(), Salary_text.get()))


def delete_command():
    db.delete(selected_tuple[0])


def update_command():
    db.update(selected_tuple[0], ID_text.get(),
              Name_text.get(), Salary_text.get())


window = Tk()

window.title("My office")


def on_closing():
    dd = db
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()
        del dd


window.protocol("WM_DELETE_WINDOW", on_closing)

l1 = Label(window, text="ID")
l1.grid(row=0, column=0)

l2 = Label(window, text="Name")
l2.grid(row=0, column=2)

l3 = Label(window, text="Salary")
l3.grid(row=1, column=0)

ID_text = StringVar()
e1 = Entry(window, textvariable=ID_text)
e1.grid(row=0, column=1)

Name_text = StringVar()
e2 = Entry(window, textvariable=Name_text)
e2.grid(row=0, column=3)

Salary_text = StringVar()
e3 = Entry(window, textvariable=Salary_text)
e3.grid(row=1, column=1)

list1 = Listbox(window, height=6, width=35)
list1.grid(row=2, column=0, rowspan=6, columnspan=2)

sb1 = Scrollbar(window)
sb1.grid(row=2, column=2, rowspan=6)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

list1.bind('<<ListboxSelect>>', get_selected_row)

b1 = Button(window, text="View all Employees", width=14, command=view_command)
b1.grid(row=2, column=3)

b2 = Button(window, text="Search Employee", width=14, command=search_command)
b2.grid(row=3, column=3)

b3 = Button(window, text="Add Employee", width=14, command=add_command)
b3.grid(row=4, column=3)

b4 = Button(window, text="Update details", width=14, command=update_command)
b4.grid(row=5, column=3)

b5 = Button(window, text="Remove Employee", width=14, command=delete_command)
b5.grid(row=6, column=3)

b6 = Button(window, text="Close", width=14, command=window.destroy)
b6.grid(row=7, column=3)

window.mainloop()
