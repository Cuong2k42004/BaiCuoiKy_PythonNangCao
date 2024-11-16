from flask import Flask, render_template, request, redirect, flash
import psycopg2
from psycopg2 import sql

app = Flask(__name__)
app.secret_key = "secret_key"  # Để sử dụng flash thông báo

# Kết nối cơ sở dữ liệu
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname='qlsv',
            user='postgres',
            password='123456',
            host='localhost',
            port='5432'
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

# Trang chủ - hiển thị danh sách sinh viên
@app.route("/")
def index():
    conn = get_db_connection()
    if not conn:
        flash("Cannot connect to the database", "danger")
        return render_template("index.html", students=[], error=True)

    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM students")
        students = cur.fetchall()
        cur.close()
        conn.close()
        return render_template("index.html", students=students)
    except Exception as e:
        flash(f"Error loading data: {e}", "danger")
        return render_template("index.html", students=[], error=True)

# Thêm sinh viên
@app.route("/add", methods=["POST"])
def add_student():
    fullname = request.form.get("fullname")
    departmentid = request.form.get("departmentid")

    if not fullname or not departmentid:
        flash("All fields are required", "danger")
        return redirect("/")

    conn = get_db_connection()
    if not conn:
        flash("Cannot connect to the database", "danger")
        return redirect("/")

    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO students (fullname, departmentid) VALUES (%s, %s)", (fullname, departmentid))
        conn.commit()
        cur.close()
        conn.close()
        flash("Student added successfully", "success")
    except Exception as e:
        flash(f"Error adding student: {e}", "danger")
    return redirect("/")

# Xóa sinh viên
@app.route("/delete/<int:studentid>")
def delete_student(studentid):
    conn = get_db_connection()
    if not conn:
        flash("Cannot connect to the database", "danger")
        return redirect("/")

    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM students WHERE studentid = %s", (studentid,))
        conn.commit()
        cur.close()
        conn.close()
        flash("Student deleted successfully", "success")
    except Exception as e:
        flash(f"Error deleting student: {e}", "danger")
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
