import tkinter as tk
from tkinter import ttk
import sqlite3


# Создаём окошко интерфейса
app = tk.Tk()
app.title("Система управления заказами")
# Добавляем надписи, которые будут появляться в окошке. Используем функцию pack сразу, потому что надпись не нужно сохранять в переменную.
tk.Label(app, text="Имя клиента").pack()
# Создаём поле для ввода имени клиента:
customer_name_entry = tk.Entry(app)
customer_name_entry.pack()
# Создаём такие же поля для деталей заказа:
tk.Label(app, text="Детали заказа").pack()
order_details_entry = tk.Entry(app)
order_details_entry.pack()
# Создаём кнопку, которая будет добавлять введённые данные в таблицу:
add_button = tk.Button(app, text="Добавить заказ", command=add_order)
add_button.pack()
# Используем новую функцию, чтобы создать таблицу из колонок, которые в ней размещены:
columns = ("id", "customer_name", "order_details", "status")
tree = ttk.Treeview(app, columns=columns, show="headings")
# Чтобы перебрать кортеж и поставить каждый его элемент в качестве кортежа, используем цикл
for column in columns:
 tree.heading(column, text=column)
 tree.pack()
# Чтобы посмотреть, как сейчас всё выглядит, вводим команду:
app.mainloop()


# Create the database if it doesn't exis
# Создает базу данных SQLite, если она не существует
def create_database():
    # Создает соединение с базой данных SQLite и таблицу, если она не существуе
    # создает таблицу, если она не существует
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# Add an order to the database
def add_order(name, quantity, price):
    # Сохраняет заказ в базе данных
    # Параметры: name (строка), quantity (целое число), price (вещественное число)
    # Возвращает: None

    # Подключается к базе данных SQLite
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO orders (name, quantity, price) VALUES (?, ?, ?)
    ''', (name, quantity, price))
    conn.commit()
    conn.close()


# Returns: список кортежей с информацией о заказах
def get_orders():
    # Возвращает список кортежей с информацией о заказах
    conn = sqlite3.connect('orders.db')
    # Подключается к базе данных SQLite
    cursor = conn.cursor()
    # Выполняет запрос к базе данных SQLite
    cursor.execute('SELECT * FROM orders')
    # Возвращает список кортежей с информацией о заказах
    orders = cursor.fetchall()
    conn.close()
    return orders


# Deletes an order from the database.
def delete_order(order_id):
    # Удаляет заказ из базы данных.
    # Parameters: order_id (целое число)
    # Returns: None
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM orders WHERE id = ?', (order_id,))
    conn.commit()
    conn.close()


# Updates an order in the database.
def update_order(order_id, name, quantity, price):
    # Обновляет заказ в базе данных.
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE orders SET name = ?, quantity = ?, price = ?
        WHERE id = ?
    ''', (name, quantity, price, order_id))
    conn.commit()
    conn.close()


def complete_order(order_id): # Функция для завершения заказа
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()
    cur.execute("UPDATE orders SET status = 'Выполнен' WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()
    view_orders()


# Main program
def main():
    # Creates the GUI and sets up event handlers.
    # Создает графический интерфейс и настраивает обработчики событий.
    create_database()
    root = tk.Tk()
    root.title('Order System')

    # Create the main frame
    # Создает главный фрейм
    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Create the order entry frame
    # Создает фрейм для ввода заказа
    order_entry_frame = ttk.Frame(main_frame)
    order_entry_frame.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))

