import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# Функция для создания таблицы
def init_db():
    conn = sqlite3.connect('business_orders.db') # Подключаемся к базе данных
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    order_details TEXT NOT NULL,
    status TEXT DEFAULT 'Новый')
    """)
    conn.commit()
    conn.close()


# Функция для добавления данных в таблицу
# Создаём функцию добавления заказа. Здесь же устанавливаем автоматическое назначение статуса ‘Новый’.
def add_order():
    conn = sqlite3.connect('business_orders.db') # Подключаемся к базе данных
    cur = conn.cursor() # Выполняем запрос
    cur.execute("INSERT INTO orders (customer_name, order_details, status) VALUES (?, ?, 'Новый')",
                (customer_name_entry.get(), order_details_entry.get()))
    conn.commit() # Сохраняем изменения
    conn.close() # Закрываем соединение
    customer_name_entry.delete(0, tk.END) # Очищаем поле ввода имени клиента
    order_details_entry.delete(0, tk.END) # Очищаем поле ввода деталей заказа
    view_orders()


# Функция для просмотра таблицы
# Создаём функцию для того, чтобы внесённые данные отображались в таблице в открытом окне:
def view_orders():
    for i in tree.get_children():
        tree.delete(i)  # Очищаем таблицу
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()  # Выполняем запрос
    cur.execute("SELECT * FROM orders") # Выбираем все данные
    rows = cur.fetchall() # Выводим данные
    for row in rows:
        tree.insert("", tk.END, values=row) # Заполняем таблицу
    conn.close()


def complete_order():
    selected_item = tree.selection()
    if selected_item:
        order_id = tree.item(selected_item[0], "values")[0]
        conn = sqlite3.connect('business_orders.db')
        cur = conn.cursor()
        cur.execute("UPDATE orders SET status = 'Завершен' WHERE id = ?", (order_id,))
        conn.commit()
        conn.close()
        view_orders()
    else:
        messagebox.showwarning("Предупреждение", "Выберите заказ для завершения")
        return


# Создаём окошко интерфейса
app = tk.Tk()
app.title("Система управления заказами")
# app.positionfromcenterx(app.winfo_screenwidth() / 2)
# Добавляем надписи, которые будут появляться в окошке.
# Используем функцию pack сразу, потому что надпись не нужно сохранять в переменную.
tk.Label(app, text="Имя клиента").pack()

# Создаём поле для ввода имени клиента:
customer_name_entry = tk.Entry(app)
customer_name_entry.pack()

# Создаём такие же поля для деталей заказа:
tk.Label(app, text="Детали заказа").pack()

# Создаём поле для ввода деталей заказа:
order_details_entry = tk.Entry(app)
order_details_entry.pack()

# Создаём кнопку, которая будет добавлять введённые данные в таблицу:
add_button = tk.Button(app, text="Добавить заказ", command=add_order)
add_button.pack()

# Запускаем функцию завершения заказа
complete_button = tk.Button(app, text="Завершить заказ", command=complete_order)
complete_button.pack()

# Используем новую функцию, чтобы создать таблицу из колонок, которые в ней размещены:
columns = ("id", "customer_name", "order_details", "status")
# Создаём таблицу
tree = ttk.Treeview(app, columns=columns, show="headings")
# Чтобы перебрать кортеж и поставить каждый его элемент в качестве кортежа, используем цикл

for column in columns: #
    tree.heading(column, text=column)
    tree.pack()

# Инициализируем базу данных
init_db()
# Создаём функцию для просмотра таблицы
view_orders()
# Чтобы посмотреть, как сейчас всё выглядит, вводим команду:
app.mainloop()