
from flask import Flask, request, redirect, url_for, render_template, session
import mysql.connector

app = Flask(__name__)

try:
    conn = mysql.connector.connect(
        host='localhost',
        user="root",
        password='Reddy@656',
        database='students_db'
    )
    cursor = conn.cursor(dictionary=True)

except mysql.connector.Error as e:
    print('Error connecting to MySQL database:', e)


@app.route('/')
@app.route('/Dashboard')
def Dashboard():
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Student_Information')
    data = cursor.fetchall()
    print("Data in Dashboard:",data)
    return render_template('Dashboard.html', data=data)


@app.route("/Add_students", methods=['GET', 'POST'])
def add_student():
    msg = ''
    if request.method == 'POST':
        student_name = request.form['student_name']
        phone_number = request.form['Phone_number']
        email = request.form['Email']
        cursor.execute("INSERT INTO Student_Information (student_name, Phone_number, Email) "
                       "VALUES ( %s, %s, %s)", ( student_name, phone_number, email))
        conn.commit()
        msg = 'Student added successfully'
        
        # return render_template('add_students.html', msg=msg)
        return redirect(url_for('Dashboard'))
    return render_template('add_students.html')

# @app.route("/search")
# def search():
#     cursor=conn.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM Student_Information where student_name  ")

@app.route("/search", methods=["GET"])
def search():
    # Get the value from the input field (passed via URL)
    student_name = request.args.get("student_name")
    
    if student_name:
        # Fetch data from the database using the provided student name
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM Student_Information WHERE student_name LIKE %s"
        cursor.execute(query, ('%' + student_name + '%',))  # Use parameterized query to prevent SQL injection
        result = cursor.fetchall()  # Fetch all matching records
        
        # Return the results, e.g., render a template with the data
        return render_template("search.html", results=result,student_name=student_name)
    
    return render_template("search.html", message="Enter a student name to search.")

# view code 
@app.route('/view_student/<Student_ID>', methods=['GET','POST'])
def view_student(Student_ID):
    print("student_id :",Student_ID)
    cursor=conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Student_information WHERE Student_ID = %s', (Student_ID,))
    value=cursor.fetchone()
    print("VVVVVVV: ",value)
    return render_template('view.html',value=value)



#delete code

# @app.route('/delete_student/<Student_ID>',methods=['POST'])

# def delete_student(Student_ID):
#     print(f'studene_id________{Student_ID}')
#     cursor=conn.cursor()
#     cursor.execute('SELECT * FROM Student_information WHERE Student_ID = %s', (Student_ID,))
#     conn.commit()
#     return redirect('Dashborad.html')


@app.route('/delete_student/<int:Student_ID>', methods=['POST'])
def delete_student(Student_ID):
    print(f'Student_ID to delete: {Student_ID}')
    
    cursor = conn.cursor()

    try:
        # Execute DELETE query to remove the student record from the database
        cursor.execute('DELETE FROM Student_information WHERE Student_ID = %s', (Student_ID,))
        
        # Commit the transaction to save changes
        conn.commit()
        
        # Check if the student was actually deleted (rows affected)
        if cursor.rowcount > 0:
            print(f"Student with ID {Student_ID} deleted.")
        else:
            print(f"No student found with ID {Student_ID}.")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()  # Rollback in case of error
    
    finally:
        # Close the cursor after operation
        cursor.close()

    # Redirect to the dashboard page (make sure you have a route for 'dashboard')
    return redirect(url_for('Dashboard'))  # Change 'dashboard' to the actual route name of your dashboard

  # Replace with actual dashboard rendering logic
  

# @app.route('/update_stu/<int:Student_ID>', methods=['POST'])
# def update(Student_ID):
#     cursor=conn.cursor(dictionary=True)
#     cursor.execute('SELECT * FROM Student_information WHERE Student_ID=%s',(Student_ID,))
#     value=cursor.fetchone()
#     return render_template('add_students',data=value)

@app.route('/update_stu/<int:Student_ID>', methods=['POST', 'GET'])
def update(Student_ID):
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Student_information WHERE Student_ID=%s', (Student_ID,))
    value = cursor.fetchone()
    return render_template('add_students', data=value)


@app.route('/update_students/', methods=['GET','POST'])
def update_stu():
    print('studentid--------------------------')
    if request.method=='POST':
        Student_ID=request.form['Student_ID']
        Student_Name=request.form['Student_name']
        Phone_Number=request.form['Phone_Number']
        Email=request.form['Email']
        cursor.execute('UPDATE  Student_information set Student_Name=%s,Phone_Number=%s,Email=%s Where Student_ID=%s',(Student_ID,Student_Name,Phone_Number,Email))
        conn.commit()
        return redirect(url_for('Dashboard'))  
    elif request.method =='get':
        return render_template('Add_students')





if __name__ == '__main__':
    app.run(debug=True)
