from flask import Flask,render_template,request
import MySQLdb,csv
import tablib
import os



app = Flask(__name__)

ROOT = os.path.dirname(os.path.abspath(__file__))
dataset = tablib.Dataset()

mydb = MySQLdb.connect(host="localhost", user="", passwd="")

cursor_em = mydb.cursor()
DATABASE_NAME = "employeeattendance"
cursor_em.execute("SHOW DATABASES")

check = False
for x in cursor_em:
    print(x)
    if x == (DATABASE_NAME,):
        check = True
        mydb = MySQLdb.connect(host="localhost", user="", db=DATABASE_NAME)
        cursor=mydb.cursor()
        break
if not check:
    cursor_em.execute("CREATE DATABASE " + DATABASE_NAME)
    mydb = MySQLdb.connect(host="localhost", user="", db=DATABASE_NAME)
    cursor_em=mydb.cursor()
    cursor_em.execute("CREATE TABLE tbl_attendance (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), attendance VARCHAR(255))")



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
    if request.method == 'POST':
        target = os.path.join(ROOT, 'temp/')

        if not os.path.isdir(target):
            os.mkdir(target)
        file = request.files['file']
        filename = file.filename
        destination = target + 'temp.csv'
        file.save(destination)
        with open(destination, 'r') as f:
            dataset.csv = f.read()
            r = csv.DictReader(f)
            print(dataset.csv)
        for x in dataset:
            val = (x[1], x[2])
            sql = "INSERT INTO tbl_attendance(name,attendance) VALUES (%s, %s)"
            cursor.execute(sql, val)
            mydb.commit()
        return render_template('table.html', dataset=dataset)

if __name__ == '__main__':
    app.run(debug=True)
