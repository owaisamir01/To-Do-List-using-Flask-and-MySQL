from flask import Flask, render_template, request,redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'test_db'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST']) 
def index():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO test_record (title, description) VALUES (%s, %s)", (title, desc))
            mysql.connection.commit()  
            cur.close()
            return render_template('index.html')
        except Exception as e:
            return f"An error occurred: {str(e)}"
    else:
        return render_template('index.html')

@app.route('/showdata')
def showdata():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM TEST_RECORD")
        data = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        return render_template('table.html', tabledata=data)
       
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/delete/<int:id>')
def delete(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM TEST_RECORD WHERE ID = %s", (id,))
        mysql.connection.commit()
        cur.close()
        return redirect('/showdata')
    except Exception as e:
        return f"An error occurred: {str(e)}"


@app.route('/edit/<int:id>')
def edit(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM test_record WHERE id = %s", (id,))
        data = cur.fetchone()  # Assuming only one record will match the ID
        cur.close()

        return render_template('edit.html', data=data)
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/editdata/<int:id>', methods=['POST'])
def editdata(id):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        try:
            cur = mysql.connection.cursor()
            cur.execute('UPDATE TEST_RECORD SET TITLE=%s, DESCRIPTION=%s WHERE ID=%s', (title, desc, id))
            mysql.connection.commit()
            cur.close()
            return redirect('/showdata')
        except Exception as e:
            return f"An error occurred: {str(e)}"



if __name__ == '__main__':
    app.run(debug=True)
