import tkinter as tk
from tkinter import ttk
import sqlite3


def create_table():
    """Create the orders table if it doesn't exist."""
    with sqlite3.connect('business_orders.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                customer_name TEXT NOT NULL,
                order_details TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)


def add_order(customer_name_entry, order_details_entry, tree):
    """Add a new order to the database and update the table."""
    with sqlite3.connect('business_orders.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders (customer_name, order_details, status) VALUES (?, ?, 'Новый')",
                       (customer_name_entry.get(), order_details_entry.get()))
        conn.commit()

    customer_name_entry.delete(0, tk.END)
    order_details_entry.delete(0, tk.END)
    view_orders(tree)


def view_orders(tree):
    """Display the orders in the table."""
    tree.delete(*tree.get_children())
    with sqlite3.connect('business_orders.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders")
        rows = cursor.fetchall()
        for row in rows:
            tree.insert("", tk.END, values=row)


def main():
    app = tk.Tk()
    app.title("Система управления заказами")

    tk.Label(app, text="Имя клиента").pack()
    customer_name_entry = tk.Entry(app)
    customer_name_entry.pack()

    tk.Label(app, text="Детали заказа").pack()
    order_details_entry = tk.Entry(app)
    order_details_entry.pack()

    add_button = tk.Button(app, text="Добавить заказ", command=lambda: add_order(customer_name_entry, order_details_entry, tree))
    add_button.pack()

    columns = ("id", "customer_name", "order_details", "status")
    tree = ttk.Treeview(app, columns=columns, show="headings")
    for column in columns:
        tree.heading(column, text=column)
    tree.pack()

    create_table()
    view_orders(tree)

    app.mainloop()


if __name__ == "__main__":
    main()