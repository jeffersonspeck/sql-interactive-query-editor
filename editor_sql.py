import os
import psycopg2  # type: ignore
from dotenv import load_dotenv  # type: ignore
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import tkinter.font as tkFont

load_dotenv()

db_config = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

def execute_query(cursor, query):
    cursor.execute(query)
    if cursor.description:
        records = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]
        return headers, records
    else:
        return [], []

class SQLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SQL Executor")

        self.input_area = tk.Text(root, height=8, width=100)
        self.input_area.pack(padx=10, pady=10)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)

        self.execute_button = tk.Button(button_frame, text="Execute SQL", command=self.run_query)
        self.execute_button.pack(side=tk.LEFT, padx=5)

        self.load_file_button = tk.Button(button_frame, text="Load SQL File", command=self.load_sql_file)
        self.load_file_button.pack(side=tk.LEFT, padx=5)

        self.copy_button = tk.Button(button_frame, text="Copy Selected Row", command=self.copy_selection)
        self.copy_button.pack(side=tk.LEFT, padx=5)

        result_frame = tk.Frame(root)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(result_frame)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_y = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        scrollbar_x = ttk.Scrollbar(root, orient=tk.HORIZONTAL, command=self.tree.xview)
        scrollbar_x.pack(fill=tk.X)

        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    def set_processing_state(self, processing=True):
        state = tk.DISABLED if processing else tk.NORMAL
        self.execute_button.config(state=state)
        self.load_file_button.config(state=state)
        self.copy_button.config(state=state)
        self.input_area.config(state=state)

        if processing:
            self.root.config(cursor="watch")
            self.root.update()
            self.processing_label = tk.Label(self.root, text="Processing, please wait...")
            self.processing_label.pack(pady=5)
        else:
            self.root.config(cursor="")
            self.processing_label.destroy()

    def run_query(self):
        query = self.input_area.get("1.0", tk.END).strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter an SQL query or load a file.")
            return
        self.set_processing_state(True)
        self.root.after(100, lambda: self.execute_and_show(query))

    def load_sql_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("SQL Files", "*.sql"), ("All Files", "*.*")])
        if filepath:
            with open(filepath, 'r', encoding='utf-8') as file:
                sql_content = file.read()
            self.set_processing_state(True)
            self.root.after(100, lambda: self.execute_and_show(sql_content))

    def copy_selection(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No row selected to copy.")
            return
        
        row_values = self.tree.item(selected_item)["values"]
        row_text = '\t'.join(str(value) for value in row_values)
        
        self.root.clipboard_clear()
        self.root.clipboard_append(row_text)
        messagebox.showinfo("Copied", "Row data copied to clipboard.")

    def execute_and_show(self, query):
        try:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()
            headers, records = execute_query(cursor, query)
            cursor.close()
            conn.commit()
            conn.close()

            for item in self.tree.get_children():
                self.tree.delete(item)

            self.tree["columns"] = headers
            self.tree["show"] = "headings"

            for header in headers:
                self.tree.heading(header, text=header)
                self.tree.column(header, width=tk.font.Font().measure(header.title()))

            for row in records:
                self.tree.insert("", tk.END, values=row)

            for col in headers:
                max_width = max(
                    [tk.font.Font().measure(str(row[headers.index(col)])) for row in records] +
                    [tk.font.Font().measure(col)]
                )
                self.tree.column(col, width=max_width + 20)

        except Exception as e:
            messagebox.showerror("Error", f"Error executing query:\n{e}")
        finally:
            self.set_processing_state(False)            

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("800x600")
    app = SQLApp(root)
    root.mainloop()