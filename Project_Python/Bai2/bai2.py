import tkinter as tk
from tkinter import messagebox
import psycopg2
from psycopg2 import sql
from PIL import Image, ImageTk
import sys  # Để thoát chương trình


class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database App")
        self.root.geometry("600x700")  # Điều chỉnh kích thước cửa sổ hợp lý hơn

        # Tạo background với hình ảnh
        try:
            self.bg_image = Image.open("CKTG2023.jpg")  # Đường dẫn tới hình ảnh
            self.bg_image = self.bg_image.resize((600, 700))  # Điều chỉnh kích thước hình ảnh
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)

            self.canvas = tk.Canvas(root, width=600, height=700)
            self.canvas.pack(fill="both", expand=True)

            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        except Exception as e:
            self.root.configure(bg='#f0f0f0')

        # Tạo frame chính để chứa các widget
        self.main_frame = tk.Frame(self.canvas, bg='white', bd=2, relief='groove')
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Database connection fields
        self.db_name = tk.StringVar(value='qlsv')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='123456')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.table_name = tk.StringVar(value='students')

        # Kiểm tra đăng nhập SQL trước khi hiện giao diện chính
        self.ask_login()

    def ask_login(self):
        # Tạo cửa sổ xác nhận
        result = messagebox.askyesno("SQL Login", "Bạn có muốn đăng nhập vào SQL không?")
        if not result:
            self.root.destroy()  # Thoát chương trình nếu chọn "Không"
            sys.exit()
        else:
            self.create_widgets()  # Hiển thị giao diện chính nếu chọn "Có"

    def create_widgets(self):
        # Title Label
        title_label = tk.Label(self.main_frame, text="Database Login", bg='white', fg='#333333', font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Connection section with grid layout
        labels = ["DB Name:", "User:", "Password:", "Host:", "Port:"]
        variables = [self.db_name, self.user, self.password, self.host, self.port]

        for i, (label, var) in enumerate(zip(labels, variables)):
            tk.Label(self.main_frame, text=label, bg='white', fg='#333333', font=('Arial', 9)).grid(row=i+1, column=0, padx=5, pady=5, sticky='e')
            entry = tk.Entry(self.main_frame, textvariable=var, font=('Arial', 9), width=30)
            entry.grid(row=i+1, column=1, padx=5, pady=5, sticky='w')
            if label == "Password:":
                entry.config(show="*")

        # Connect Button
        connect_button = tk.Button(self.main_frame, text="Connect", command=self.connect_db, bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'), width=20)
        connect_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Query operations (Ho Ten, Ma Nganh)
        self.student_name = tk.StringVar()
        self.department_id = tk.StringVar()

        tk.Label(self.main_frame, text="Ho Ten:", bg='white', fg='#333333', font=('Arial', 9)).grid(row=7, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(self.main_frame, textvariable=self.student_name, font=('Arial', 9), width=30).grid(row=7, column=1, padx=5, pady=5, sticky='w')

        tk.Label(self.main_frame, text="Ma Nganh:", bg='white', fg='#333333', font=('Arial', 9)).grid(row=8, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(self.main_frame, textvariable=self.department_id, font=('Arial', 9), width=30).grid(row=8, column=1, padx=5, pady=5, sticky='w')

        # Insert and Delete Buttons
        button_frame = tk.Frame(self.main_frame, bg='white')
        button_frame.grid(row=9, column=0, columnspan=2, pady=10)

        insert_button = tk.Button(button_frame, text="Insert Data", command=self.insert_data, bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'), width=12)
        insert_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(button_frame, text="Delete Data", command=self.delete_data, bg='#f44336', fg='white', font=('Arial', 10, 'bold'), width=12)
        delete_button.pack(side=tk.LEFT, padx=5)

        # Load Data Button
        load_button = tk.Button(self.main_frame, text="Load Data", command=self.load_data, bg='#2196F3', fg='white', font=('Arial', 10, 'bold'), width=20)
        load_button.grid(row=10, column=0, columnspan=2, pady=10)

        # Data display with scrollbar
        display_frame = tk.Frame(self.main_frame, bg='white')
        display_frame.grid(row=11, column=0, columnspan=2, pady=5, padx=5)

        scrollbar = tk.Scrollbar(display_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.data_display = tk.Text(display_frame, height=15, width=50, font=('Courier', 9), yscrollcommand=scrollbar.set, bg='#f8f9fa')
        self.data_display.pack(pady=5, fill="both", expand=True)
        scrollbar.config(command=self.data_display.yview)

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name.get(),
                user=self.user.get(),
                password=self.password.get(),
                host=self.host.get(),
                port=self.port.get()
            )
            self.cur = self.conn.cursor()
            messagebox.showinfo("Success", "Connected to the database successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error connecting to the database: {e}")

    def load_data(self):
        try:
            self.cur.execute("SELECT * FROM students")
            rows = self.cur.fetchall()
            self.data_display.delete(1.0, tk.END)
            self.data_display.insert(tk.END, f"{'ID':<10}{'Ho Ten':<20}{'Ma Nganh':<10}\n")
            self.data_display.insert(tk.END, "-"*40 + "\n")
            for row in rows:
                self.data_display.insert(tk.END, f"{row[0]:<10}{row[1]:<20}{row[2]:<10}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {e}")

    def insert_data(self):
        if not self.student_name.get() or not self.department_id.get():
            messagebox.showerror("Error", "All fields are required!")
            return
        try:
            query = "INSERT INTO students (fullname, departmentid) VALUES (%s, %s)"
            data = (self.student_name.get(), self.department_id.get())
            self.cur.execute(query, data)
            self.conn.commit()
            messagebox.showinfo("Success", "Data inserted successfully!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Error inserting data: {e}")

    def delete_data(self):
        if not self.student_name.get():
            messagebox.showerror("Error", "Student name is required to delete!")
            return
        try:
            query = "DELETE FROM students WHERE fullname = %s"
            data = (self.student_name.get(),)
            self.cur.execute(query, data)
            self.conn.commit()
            messagebox.showinfo("Success", "Data deleted successfully!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting data: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
