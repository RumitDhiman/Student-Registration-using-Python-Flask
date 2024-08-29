from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Default XAMPP MySQL user
            password='',  # Default XAMPP MySQL password
            database='student_registration'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO student (name, email, phone)
                VALUES (%s, %s, %s, %s)
            ''', (name, email, phone))
            connection.commit()
            return redirect(url_for('success'))
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()
    
    return 'Failed to register student.'

@app.route('/success')
def success():
    return 'Registration successful!'

if __name__ == '__main__':
    app.run(debug=True)
