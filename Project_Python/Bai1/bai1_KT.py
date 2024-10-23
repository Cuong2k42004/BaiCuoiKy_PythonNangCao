import tkinter as tk
from tkinter import ttk, messagebox

# Danh sách để lưu trữ kết quả
history = []

# Hàm xử lý tính toán dựa trên phép tính đã chọn
def calculate(operator):
    try:
        x = float(entry_x.get())  # Lấy giá trị từ ô nhập x
        y = float(entry_y.get())  # Lấy giá trị từ ô nhập y

        if operator == '+':
            result = x + y
        elif operator == '-':
            result = x - y
        elif operator == '*':
            result = x * y
        elif operator == '/':
            if y != 0:
                result = x / y
            else:
                messagebox.showerror("Lỗi", "Không thể chia cho 0")
                return
        
        result = round(result, 2)  # Làm tròn kết quả với 2 chữ số thập phân
        result_label.config(text=f"Kết quả: {result}")
        
        # Lưu kết quả vào danh sách history và cập nhật tab 2
        history.append(f"{x} {operator} {y} = {result}")
        update_history()

    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ vào x và y.")

# Hàm cập nhật lịch sử tính toán trong tab 2
def update_history():
    for widget in tab2.winfo_children():
        widget.destroy()  # Xóa các widget cũ để làm mới danh sách
    tk.Label(tab2, text="Lịch sử tính toán:", font=('Arial', 14)).pack(pady=10)
    for record in history:
        tk.Label(tab2, text=record, font=('Arial', 12)).pack()

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Tính Toán Casio")
root.geometry("400x400")  # Điều chỉnh kích thước cửa sổ

# Tạo các tab
tab_control = ttk.Notebook(root)

# Tab 1: Giải toán
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Máy tính')

# Tab 2: Lịch sử tính toán
tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text='Lịch sử')

# Đặt các tab vào cửa sổ
tab_control.pack(expand=1, fill="both")

# Ô nhập cho x và y với kích thước lớn hơn
tk.Label(tab1, text="Nhập x:", font=('Arial', 14)).grid(row=0, column=0, padx=10, pady=10)
entry_x = tk.Entry(tab1, width=15, borderwidth=5, font=('Arial', 14))
entry_x.grid(row=0, column=1)

tk.Label(tab1, text="Nhập y:", font=('Arial', 14)).grid(row=1, column=0, padx=10, pady=10)
entry_y = tk.Entry(tab1, width=15, borderwidth=5, font=('Arial', 14))
entry_y.grid(row=1, column=1)

# Khung hiển thị kết quả với kích thước lớn hơn
result_label = tk.Label(tab1, text="Kết quả: ", font=('Arial', 16))
result_label.grid(row=2, column=0, columnspan=2, pady=20)

# Tạo các nút cho phép tính, với kích thước nút lớn hơn
operators = ['+', '-', '*', '/']
for i, operator in enumerate(operators):
    button = tk.Button(tab1, text=operator, padx=30, pady=20, font=('Arial', 14), command=lambda op=operator: calculate(op))
    button.grid(row=3 + i // 2, column=i % 2, padx=20, pady=10)

# Tab 2: Lịch sử tính toán sẽ được cập nhật sau khi có kết quả
tk.Label(tab2, text="Lịch sử tính toán:", font=('Arial', 14)).pack(pady=10)

# Chạy vòng lặp chính
root.mainloop()
