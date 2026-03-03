import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "super-secure-key"

app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            rollnumber TEXT,
            year TEXT,
            branch TEXT,
            photo TEXT
        )
    ''')
    
    conn.commit()
    conn.close()




def get_db():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

db = get_db()
students = db.execute("SELECT * FROM students").fetchall()
db.close()







@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        year = request.form['year']
        Rollnumber = request.form['Rollnumber']
        Branch = request.form['Branch']

        photo = request.files['photo']
        filename = secure_filename(photo.filename)
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(photo_path)

        conn = sqlite3.connect('students.db')
        c = conn.cursor()

        c.execute('''
            INSERT INTO students (name, rollnumber, year, branch, photo)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, Rollnumber, year, Branch, filename))

        conn.commit()
        conn.close()

        return render_template(
            'preview.html',
            name=name,
            year=year,
            Rollnumber=Rollnumber,
            Branch=Branch,
            photo=filename
        )

    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "admin123":
            session['admin'] = True
            return redirect(url_for('admin'))
        else:
            return "Invalid Credentials"

    return render_template('login.html')

@app.route('/delete/<int:id>')
def delete(id):
    db = get_db()
    db.execute("DELETE FROM students WHERE id=?", (id,))
    db.commit()
    db.close()
    return redirect(url_for('admin'))

@app.route('/admin')
def admin():
    if 'admin' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    students = c.fetchall()
    conn.close()

    return render_template('admin.html', students=students)


init_db()

conn = sqlite3.connect('students.db')
c = conn.cursor()

c.execute("SELECT * FROM students")
print(c.fetchall())

conn.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)