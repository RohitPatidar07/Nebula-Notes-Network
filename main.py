#“Nebula Notes Network”    : Develop a Tkinter application for creating, organizing, and searching notes, with data saved in both local files and a MySQL database.
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import os
from datetime import datetime

# Database connection
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rohitdemo@123",
            database="tkinter"
        )
        return connection
    except mysql.connector.Error as err:
        messagebox.showerror("Database Connection Error", f"Error: {err}")
        return None
 
def save_note():
    title = title_entry.get()
    content = content_text.get("1.0", tk.END).strip()

    if not title or not content:
        messagebox.showerror("Error", "Title and content cannot be empty")
        return

    try: 

        conn = connect_to_database()
        if conn is None:
            return
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notes (title, content) VALUES (%s, %s)", (title, content))
        conn.commit()
        cursor.close()
        conn.close()
 
        filename = f"notes/{title}_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
        with open(filename, "w") as file:
            file.write(content)

        messagebox.showinfo("Success", "Note saved successfully")
        title_entry.delete(0, tk.END)
        content_text.delete("1.0", tk.END)
        load_notes()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save note: {str(e)}")
 
def load_notes():
    conn = connect_to_database()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, timestamp FROM notes")
        notes = cursor.fetchall()
        cursor.close()
        conn.close()

        for row in tree.get_children():
            tree.delete(row)

        for note in notes:
            tree.insert("", tk.END, values=note)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
 
def view_note():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a note to view")
        return

    note_id = tree.item(selected_item[0])["values"][0]
    conn = connect_to_database()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT title, content FROM notes WHERE id = %s", (note_id,))
        note = cursor.fetchone()
        cursor.close()
        conn.close()

        view_window = tk.Toplevel(root)
        view_window.title(note[0])
        view_content = tk.Text(view_window, wrap=tk.WORD)
        view_content.insert(tk.END, note[1])
        view_content.config(state=tk.DISABLED)
        view_content.pack(fill=tk.BOTH, expand=True)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
 
root = tk.Tk()
root.title("Nebula Notes Network")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(pady=20, fill=tk.BOTH, expand=True)

title_label = tk.Label(frame, text="Title:")
title_label.grid(row=0, column=0, sticky=tk.W)

title_entry = tk.Entry(frame, width=50)
title_entry.grid(row=0, column=1, sticky=tk.W)

content_label = tk.Label(frame, text="Content:")
content_label.grid(row=1, column=0, sticky=tk.W)

content_text = tk.Text(frame, height=10, width=50)
content_text.grid(row=1, column=1, sticky=tk.W)

save_button = tk.Button(frame, text="Save Note", command=save_note)
save_button.grid(row=2, column=1, sticky=tk.W, pady=10)

tree_frame = tk.Frame(root)
tree_frame.pack(fill=tk.BOTH, expand=True)

columns = ("ID", "Title", "Timestamp")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.pack(fill=tk.BOTH, expand=True)

view_button = tk.Button(root, text="View Note", command=view_note)
view_button.pack(pady=10)

if not os.path.exists("notes"):
    os.makedirs("notes")

load_notes()

root.mainloop()