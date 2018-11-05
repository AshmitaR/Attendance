from flask import Flask,render_template,request
import MySQLdb,csv


app = Flask(__name__)

conn= MySQLdb.connect(host="localhost", user="root", db="attendence_system")
cursor = conn.cursor()

@app.route('/',methods=["GET","POST"])
def index():
    if request.method=="POST":
        username = str(request.form['username'])
        password = str(request.form['password'])
        print(username, password)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO admin (username,password)VALUES(%s,%s)', (username, password))
        cursor.close()
        conn.commit()
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login_form.html")

@app.route('/register')
def register():
    return render_template("register_form.html")


@app.route('/employee',methods=["GET","POST"])
def enter_employee():
    if request.method=="POST":
        username = str(request.form['username'])
        password = str(request.form['password'])
        cursor = conn.cursor()
        cursor.execute('SELECT username, password FROM admin WHERE username=%s',username)
        user=cursor.fetchone()
        cursor.close()
        conn.commit()
        if user[1]==password:
            return render_template("enter_employee.html")
        else: return "failed"

@app.route('/employee/create', methods=["GET", "POST"])
def create():
    employee_name = str(request.args.get('employee_name', ""))
    cursor = conn.cursor()
    cursor.execute('INSERT INTO employee (employee_name)VALUES(%s)', (employee_name))
    conn.commit()
    cursor.close()
    return render_template("enter_employee.html")

@app.route('/employee/export', methods=["GET", "POST"])
def export():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employee')
    res = cursor.fetchall()
    print res
    with open('E:\output.csv', 'w') as fileout:
        writer = csv.writer(fileout)
        writer.writerows(res)
    conn.commit()
    cursor.close()
    return render_template("enter_employee.html")


@app.route('/employee/show_attendence', methods=["GET", "POST"])
def show_attendance():
    return render_template("csv_generator.html")

if __name__ == '__main__':
    app.run(debug=True)
