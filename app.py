from flask import Flask, request, jsonify, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Function to establish connection with MySQL database
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',
        database='airport'
    )
    return conn

# Route to render HTML form for adding airport and list of airports
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute('SELECT * FROM Airport')
        airports = cursor.fetchall()
    except mysql.connector.Error as e:
        airports = []
        print(f'Error fetching airports: {e}')
    finally:
        cursor.close()
        conn.close()

    return render_template('index.html', airports=airports)

# Route to handle form submission and add airport
@app.route('/add_airport', methods=['POST'])
def add_airport():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Retrieve form data
        airport_code = request.form.get('airport_code')
        airport_name = request.form.get('airport_name')
        city = request.form.get('city')
        country = request.form.get('country')
        timezone_offset = request.form.get('timezone_offset')
        latitude = float(request.form.get('latitude'))
        longitude = float(request.form.get('longitude'))

        # Insert data into Airport table
        insert_query = '''
            INSERT INTO Airport (airport_code, airport_name, city, country, timezone_offset, latitude, longitude)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(insert_query, (airport_code, airport_name, city, country, timezone_offset, latitude, longitude))
        conn.commit()

        message = f'Airport {airport_code} added successfully'
    except mysql.connector.Error as e:
        conn.rollback()  # Rollback the transaction in case of error
        message = f'Error adding airport: {e}'
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('index'))

# Route to update an existing airport
@app.route('/update_airport/<airport_code>', methods=['POST'])
def update_airport(airport_code):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Retrieve form data
        airport_name = request.form.get('airport_name')
        city = request.form.get('city')
        country = request.form.get('country')
        timezone_offset = request.form.get('timezone_offset')
        latitude = float(request.form.get('latitude'))
        longitude = float(request.form.get('longitude'))

        # Update data in Airport table
        update_query = '''
            UPDATE Airport
            SET airport_name=%s, city=%s, country=%s, timezone_offset=%s, latitude=%s, longitude=%s
            WHERE airport_code=%s
        '''
        cursor.execute(update_query, (airport_name, city, country, timezone_offset, latitude, longitude, airport_code))
        conn.commit()

        message = f'Airport {airport_code} updated successfully'
    except mysql.connector.Error as e:
        conn.rollback()  # Rollback the transaction in case of error
        message = f'Error updating airport: {e}'
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('index'))

# Route to delete an airport
@app.route('/delete_airport/<airport_code>', methods=['POST'])
def delete_airport(airport_code):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Delete data from Airport table
        delete_query = '''
            DELETE FROM Airport
            WHERE airport_code=%s
        '''
        cursor.execute(delete_query, (airport_code,))
        conn.commit()

        message = f'Airport {airport_code} deleted successfully'
    except mysql.connector.Error as e:
        conn.rollback()  # Rollback the transaction in case of error
        message = f'Error deleting airport: {e}'
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
