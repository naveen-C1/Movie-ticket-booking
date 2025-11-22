import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector as a

# ---------------- DATABASE SETUP -----------------
passwd = input("Enter MySQL Password: ")
con = a.connect(host="localhost", user="root", passwd=passwd)
cur = con.cursor()

cur.execute("CREATE DATABASE IF NOT EXISTS shows")
cur.execute("USE shows")

cur.execute("""CREATE TABLE IF NOT EXISTS MyShow(
        moviename VARCHAR(30),
        charge INT,
        showtime VARCHAR(50),
        showdate VARCHAR(20))""")

cur.execute("""CREATE TABLE IF NOT EXISTS Snacks(
        name VARCHAR(30),
        cost INT)""")

cur.execute("""CREATE TABLE IF NOT EXISTS Viewers(
        name VARCHAR(30),
        ticket INT,
        payment INT,
        showdata VARCHAR(20),
        phone VARCHAR(20))""")

cur.execute("""CREATE TABLE IF NOT EXISTS Worker(
        name VARCHAR(30),
        work VARCHAR(20),
        salary VARCHAR(20))""")

con.commit()

# ----------------- APP WINDOW ---------------------
root = tk.Tk()
root.title("Majestic Movie System (MMS)")
root.geometry("1000x620")
root.configure(bg="#151515")

title_label = tk.Label(root, text="🎬 Majestic Movie System (MMS)", 
                       font=("Arial", 24, "bold"), fg="gold", bg="#151515")
title_label.pack(pady=20)

# ------------------- HELPERS ----------------------

def clear_frame():
    for widget in main_frame.winfo_children():
        widget.destroy()

# ---------- UNIVERSAL TABLE DISPLAY ----------
def display_table(query, columns, title):
    clear_frame()

    tk.Label(main_frame, text=title, font=("Arial", 20, "bold"), fg="white", bg="#151515").pack(pady=10)

    table = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)

    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=150)

    cur.execute(query)
    for row in cur.fetchall():
        table.insert("", tk.END, values=row)

    table.pack(pady=10)


# -------------------- ADD FORMS --------------------

def add_show():
    clear_frame()
    tk.Label(main_frame, text="Add Movie Show", font=("Arial", 20, "bold"), fg="white", bg="#151515").pack(pady=10)

    labels = ["Movie Name", "Charge", "Show Time", "Show Date"]
    entries = {}

    for l in labels:
        tk.Label(main_frame, text=l, fg="white", bg="#151515").pack()
        e = tk.Entry(main_frame, width=30)
        e.pack(pady=2)
        entries[l] = e

    def submit():
        data = (entries["Movie Name"].get(), entries["Charge"].get(),
                entries["Show Time"].get(), entries["Show Date"].get())
        cur.execute("INSERT INTO MyShow VALUES (%s,%s,%s,%s)", data)
        con.commit()
        messagebox.showinfo("Success", "Show Added Successfully!")

    tk.Button(main_frame, text="Submit", font=("Arial",14),
              bg="green", fg="white", command=submit).pack(pady=10)


def add_snack():
    clear_frame()

    tk.Label(main_frame, text="Add Snack", font=("Arial", 20, "bold"), fg="white", bg="#151515").pack(pady=10)

    tk.Label(main_frame, text="Snack Name", fg="white", bg="#151515").pack()
    name = tk.Entry(main_frame, width=30)
    name.pack()

    tk.Label(main_frame, text="Cost", fg="white", bg="#151515").pack()
    cost = tk.Entry(main_frame, width=30)
    cost.pack()

    def submit():
        cur.execute("INSERT INTO Snacks VALUES (%s,%s)", (name.get(), cost.get()))
        con.commit()
        messagebox.showinfo("Success", "Snack Added Successfully!")

    tk.Button(main_frame, text="Submit", bg="green", fg="white",
              font=("Arial",14), command=submit).pack(pady=10)


def book_ticket():
    clear_frame()
    tk.Label(main_frame, text="Book Ticket", font=("Arial", 20, "bold"), fg="white", bg="#151515").pack(pady=10)

    labels = ["Viewer Name", "Tickets", "Cost per Ticket", "Show Date & Time", "Phone"]
    entries = {}

    for l in labels:
        tk.Label(main_frame, text=l, fg="white", bg="#151515").pack()
        e = tk.Entry(main_frame, width=30)
        e.pack(pady=2)
        entries[l] = e

    def submit():
        t = int(entries["Tickets"].get())
        cost = int(entries["Cost per Ticket"].get())
        total = t * cost

        data = (entries["Viewer Name"].get(), t, total,
                entries["Show Date & Time"].get(), entries["Phone"].get())

        cur.execute("INSERT INTO Viewers VALUES (%s,%s,%s,%s,%s)", data)
        con.commit()
        messagebox.showinfo("Success", f"Booking Successful! Total Payment = ₹{total}")

    tk.Button(main_frame, text="Submit", bg="green", fg="white",
              font=("Arial",14), command=submit).pack(pady=10)


def add_worker():
    clear_frame()
    tk.Label(main_frame, text="Add Worker", font=("Arial", 20, "bold"), fg="white", bg="#151515").pack(pady=10)

    labels = ["Worker Name", "Work Type", "Salary"]
    entries = {}

    for l in labels:
        tk.Label(main_frame, text=l, fg="white", bg="#151515").pack()
        e = tk.Entry(main_frame, width=30)
        e.pack(pady=2)
        entries[l] = e

    def submit():
        cur.execute("INSERT INTO Worker VALUES (%s,%s,%s)",
                    (entries["Worker Name"].get(), entries["Work Type"].get(), entries["Salary"].get()))
        con.commit()
        messagebox.showinfo("Success", "Worker Added Successfully")

    tk.Button(main_frame, text="Submit", bg="green", fg="white",
              font=("Arial",14), command=submit).pack(pady=10)


# -------------------- DELETE OPTIONS --------------------

def delete_show():
    clear_frame()
    tk.Label(main_frame, text="Delete Movie Show", font=("Arial", 20, "bold"),
             fg="white", bg="#151515").pack(pady=10)

    cur.execute("SELECT moviename FROM MyShow")
    shows = [i[0] for i in cur.fetchall()]

    if not shows:
        tk.Label(main_frame, text="No Shows Available", fg="red", bg="#151515").pack()
        return

    tk.Label(main_frame, text="Select Show to Delete", fg="white", bg="#151515").pack()
    cb = ttk.Combobox(main_frame, values=shows, width=30)
    cb.pack(pady=5)

    def delete():
        show = cb.get()
        cur.execute("DELETE FROM MyShow WHERE moviename=%s", (show,))
        con.commit()
        messagebox.showinfo("Deleted", f"Show '{show}' deleted successfully!")
        delete_show()

    tk.Button(main_frame, text="Delete", bg="red", fg="white",
              font=("Arial",14), command=delete).pack(pady=10)


def delete_booking():
    clear_frame()
    tk.Label(main_frame, text="Delete Ticket Booking", font=("Arial", 20, "bold"),
             fg="white", bg="#151515").pack(pady=10)

    cur.execute("SELECT name FROM Viewers")
    names = [i[0] for i in cur.fetchall()]

    if not names:
        tk.Label(main_frame, text="No Bookings Available", fg="red", bg="#151515").pack()
        return

    tk.Label(main_frame, text="Select Booking to Delete", fg="white", bg="#151515").pack()
    cb = ttk.Combobox(main_frame, values=names, width=30)
    cb.pack(pady=5)

    def delete():
        name = cb.get()
        cur.execute("DELETE FROM Viewers WHERE name=%s", (name,))
        con.commit()
        messagebox.showinfo("Deleted", f"Booking for '{name}' deleted successfully!")
        delete_booking()

    tk.Button(main_frame, text="Delete", bg="red", fg="white",
              font=("Arial",14), command=delete).pack(pady=10)


# -------------------- DISPLAY SCREENS --------------------

def display_shows():
    display_table("SELECT * FROM MyShow",
                  ["Movie", "Charge", "Time", "Date"],
                  "Available Shows")

def display_bookings():
    display_table("SELECT * FROM Viewers",
                  ["Name", "Tickets", "Payment", "Show", "Phone"],
                  "Ticket Bookings")

def display_workers():
    display_table("SELECT * FROM Worker",
                  ["Name", "Work", "Salary"],
                  "Workers List")


# ---------------- MENU BUTTONS ---------------------

button_frame = tk.Frame(root, bg="#151515")
button_frame.pack(side="left", fill="y", padx=10)

btn_style = {"font": ("Arial", 14), "bg": "#333", "fg": "white", "width": 20, "pady": 5}

tk.Button(button_frame, text="Add Show", command=add_show, **btn_style).pack(pady=5)
tk.Button(button_frame, text="Add Snack", command=add_snack, **btn_style).pack(pady=5)
tk.Button(button_frame, text="Book Ticket", command=book_ticket, **btn_style).pack(pady=5)
tk.Button(button_frame, text="Add Worker", command=add_worker, **btn_style).pack(pady=5)

tk.Button(button_frame, text="Display Shows", command=display_shows, **btn_style).pack(pady=5)
tk.Button(button_frame, text="Display Bookings", command=display_bookings, **btn_style).pack(pady=5)
tk.Button(button_frame, text="Display Workers", command=display_workers, **btn_style).pack(pady=5)

# 🔥 NEW DELETE BUTTONS BELOW:
tk.Button(button_frame, text="Delete Show", command=delete_show, bg="#660000", fg="white",
          font=("Arial",14), width=20, pady=5).pack(pady=5)

tk.Button(button_frame, text="Delete Booking", command=delete_booking, bg="#660000", fg="white",
          font=("Arial",14), width=20, pady=5).pack(pady=5)


main_frame = tk.Frame(root, bg="#151515")
main_frame.pack(side="right", expand=True, fill="both")

root.mainloop()
