from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'python-contactdb'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts")
    data = cur.fetchall()
    return render_template('index.html', contacts = data)

@app.route('/add_contacto', methods=['POST'])
def addContac():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contacts (name, phone, email) VALUES (%s,%s,%s)", (name, phone, email))
        mysql.connection.commit()
        flash('Contact Added successfully')
        return redirect(url_for('home'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def deleteContac(id):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM contacts WHERE id = {0}".format(id))
        mysql.connection.commit()
        flash('Contact deleted successfully')
        return redirect(url_for('home'))

@app.route('/edit/<string:id>', methods = ['POST','GET'])
def editContac(id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM contacts WHERE id = {0}".format(id))
        data = cur.fetchall()
        return render_template('edit.html', contact = data[0])
        
@app.route('/update/<string:id>',  methods = ['POST'])
def updateContacr(id):
        if request.method == 'POST':
                name = request.form['name']
                phone = request.form['phone']
                email = request.form['email']
                cur = mysql.connection.cursor()
                cur.execute("UPDATE contacts SET name = %s, email = %s, phone = %s WHERE id = %s", (name, email, phone, id))
                mysql.connection.commit()
                flash('Contact updated successfully')
                return redirect(url_for('home'))

if (__name__ == '__main__'):
    app.run(port = 3000, debug = True)
