from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from sqlite3 import Error
import os
import cv2
from keras.models import load_model




def create_app(test_config=None):


    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


            
    
    
    
    
    @app.route('/', methods=("GET",))
    def inp():
        return render_template('welcome_2.html')
    
    @app.route('/workerlogin', methods=("GET",))
    def appointments():
        return render_template("healthWorkerlogin_2.html")
    @app.route('/clinicianlogin', methods=("GET", ))
    def clinician():
       return render_template('clinicianlogin.html')
    @app.route('/clinicianlogin/work', methods=("POST" ,))
    def clinian_on_work():
       username = request.form['Username']
       password = request.form['Password']
       conn = sqlite3.connect('clinician.db')
       c = conn.cursor()
       c.execute('SELECT * FROM loginclinician WHERE username=? AND password=?', (username, password))
       user = c.fetchone()
       c.close()

       if user:
          return render_template('clinicianhomepage.html')
       else:
          return "unsuccessful login kindly input correct username and password"
       
       


    @app.route('/workerlogin/do')
    def back():
        return render_template('healthworker.html')
    
    @app.route('/workerlogin/do', methods=("POST",))
    def next():
        

        username = request.form['Username']
        password = request.form['Password']
        conn = sqlite3.connect('worker.db')
        c = conn.cursor()
        c.execute('SELECT * FROM worker WHERE username=? AND password=?', (username, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            return render_template('healthworker.html')
        else:
            return "unsuccessful login kindly input correct username and password"    
    
    
    @app.route('/patientlogin', methods=("GET",))
    def loginPatient():
        return render_template('patientlogin_3.html')
    
    
    def save_uploaded_file(file):
       filename = file.filename
       file_path = os.path.join('workerlogin/do/info/pred/records/', filename)
       file.save(file_path)
       return file_path
    
    
        
    @app.route('/patientlogin/logged' , methods=("GET",))
    def logged():
        if request.method == "GET":
           
           return render_template('patient.html')
    
    @app.route('/patientlogin/logged', methods=('POST','GET'))
    def logpatient():
        if request.method == 'POST':
            username = request.form['Username']
            password = request.form['Password']
            conn = sqlite3.connect('patient.db')
            c = conn.cursor()
            c.execute('SELECT * FROM patient WHERE username=? AND password=?', (username, password))
            user = c.fetchone()
            conn.close()
        
            if user:
             return render_template('patient.html')
            else:
             return "unsuccessful login kindly input correct username and password"
        if request.method == 'GET':
            username = request.form['Username']
            password = request.form['Password']
            conn = sqlite3.connect('patient.db')
            c = conn.cursor()
            c.execute('SELECT * FROM patient WHERE username=? AND password=?', (username, password))
            user = c.fetchone()
            conn.close()
        
            if user:
             return render_template('patient.html')
            else:
             return "unsuccessful login kindly input correct username and password"
            
    
    @app.route('/workerlogin/do/info/pred/records', methods=("GET", "POST"))
    def upload_and_display_records():
       
       if request.method == "POST":
           
          #if 'file' not in request.files:
            
            #return 'No file part'
        
          file = request.files['file']
          file_path = save_uploaded_file(file)
          if file.filename == '':
           return 'No selected file'
    
          
 

          return render_template('result.html', file_path=file_path) 
       if request.method == "GET":
          
          
          #if 'file' not in request.files:
            #return 'No file part'
        
          file = request.files['file']
          if file.filename == '':
            return 'No selected file'
    
          file_path = save_uploaded_file(file)
 

          return render_template('result.html', file_path=file_path)
          
       

    
    
        
    appointments={}

    @app.route('/patientlogin/logged/book', methods=("GET","POST"))
    def book():
       global selected_day, selected_time
       if request.method == "POST":
        selected_day = request.form['selected_day']
        selected_time = request.form['selected_time']
        appointments['selected_day'] = selected_day
        appointments['selected_time'] = selected_time
        return redirect(url_for('logged'))
       return render_template('bookappointment.html')
    
    @app.route('/patientlogin/logged/view', methods=('GET','POST'))
    def view():
       global selected_day, selected_time
       selected_day = appointments.get('selected_day')
       selected_time = appointments.get('selected_time')
       return render_template('viewappointment.html', selected_day=selected_day, selected_time=selected_time)

           
    
    @app.route('/patientlogin/logged/eyecare', methods=("GET",))
    def eyecare():
        return render_template('Eyecaretip.html')
    
    @app.route('/patientlogin/logged/contact', methods=("GET",))
    def contact():
        return render_template('contact.html')

    

    @app.route('/workerlogin/do/info', methods=("GET",))
    def disp():
        return render_template('new_patient.html')

    @app.route('/workerlogin/do/info/pred', methods=("POST",))
    def add_new_patient():
            

    

            try:
               

               conn = sqlite3.connect("patientform.db")
               current = conn.cursor()
               query = 'INSERT INTO patientform (fullName, phoneNumber, address, age, gender, diabetesType, weight, height, fever, bloodPressure, sugarLevel, appointmentDate, appointmentTime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
               values = (request.form['fullName'], request.form['phone-number'], request.form['address'], request.form['age'], request.form['gender'], request.form['diabetes'], request.form['weight'], request.form['height'], request.form['fever'], request.form['bloodPressure'], request.form['sugarLevel'], request.form['appointmentDate'], request.form['appointmentTime'])
               current.execute(query, values)
               conn.commit()
               current.close()
               conn.close()
               return render_template('Prediction.html')
            except Error as e:
               return str(e)
        
    
        


    
    @app.route('/workerlogin/do/patientrecords', methods=("GET","POST"))
    def gettingrecord():
    
     if request.method == "POST":
        search_query = request.form.get('searchInput', '').lower()
        conn = sqlite3.connect('patientform.db')
        c = conn.cursor()
        c.execute("SELECT * FROM patientform WHERE fullName LIKE ?", ('%' + search_query + '%',))
        patients = c.fetchall()
        conn.close()
        return render_template('patient_records.html', patients=patients)
     else:
        return render_template('patient_records.html', patients=None)  # Render the page without patient data
        
    
    @app.route('/workerlogin/do/manage')
    def manage():
       conn = sqlite3.connect('patientform.db')  # Replace 'your_database.db' with your actual SQLite database file path
       cursor = conn.cursor()
       cursor.execute("SELECT fullName, appointmentTime, appointmentDate FROM patientform")
       appointments = cursor.fetchall()
       conn.close()
       return render_template('appointmentmanagementcopy.html', appointments=appointments)
       
       



    @app.route('/workerlogin/do/newworker', methods=("GET",))
    def newworker():
        return render_template('register_healthworker.html')
    

    @app.route('/workerlogin/do/newworker', methods=("POST", "GET"))
    def addworker():
        
        if request.method == "POST": 
          conn = sqlite3.connect("WorkerInfo.db")
          current = conn.cursor()
          query = 'INSERT INTO HealthWorkers (name, email, password, phone, address, occupation, dob, age, gender) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
          values = (request.form['name'], request.form['email'], request.form['password'], request.form['phone'], request.form['address'], request.form['occupation'], request.form['dob'], request.form['age'], request.form['gender'])          
          current.execute(query, values)
          conn.commit()
          current.close()
          conn.close()
          return render_template('/workerlogin/do')
        
        if request.method == "GET": 
          conn = sqlite3.connect("WorkerInfo.db")
          current = conn.cursor()
          query = 'INSERT INTO HealthWorkers (name, email, password, phone, address, occupation, dob, age, gender) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
          values = (request.form['name'], request.form['email'], request.form['password'], request.form['phone'], request.form['address'], request.form['occupation'], request.form['dob'], request.form['age'], request.form['gender'])           
          current.execute(query, values)
          conn.commit()
          current.close()
          conn.close()
          return render_template('/workerlogin/do')
        
    @app.route('/clinicianlogin/cliniciansignup', methods=("GET" ,))
    def signUpclcn():
       return render_template('cliniciansignup.html')
    
    @app.route('/clinicianlogin/cliniciansignup', methods=("POST" ,))
    def signupclcn():
       if request.method == "POST":
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            if password == confirm_password:
               
               conn = sqlite3.connect("clinician.db")
               current = conn.cursor()
               query = 'INSERT INTO loginclinician (username, password) VALUES (?, ?)'
               values = (request.form['name'], request.form['password'])
               current.execute(query, values)
               conn.commit()
               current.close()
               conn.close()
               con = sqlite3.connect("clcnsignup.db")
               cur = con.cursor()
               Query = 'INSERT INTO clcnSignUp (name, email, phone, hospital, id_number, password) VALUES (?, ?, ?, ?, ?, ?)'
               vals = (request.form['name'], request.form['email'] ,request.form['phone'], request.form['hospital'], request.form['id_number'], request.form['password'] )           
               cur.execute(Query, vals)
               con.commit()
               cur.close()
               con.close()
               return redirect('/clinicianlogin')
            else:
             return "Please try again the confirm password does not match with the password"
       
       
        
        
    @app.route('/patientlogin/patientsignup', methods=("GET",))
    def patient_sign_up():
       return render_template('patientnewsignup.html')
    
    @app.route('/patientlogin/patientsignup', methods=("POST",))
    def signup():
       if request.method == "POST":
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            if password == confirm_password:
               
               conn = sqlite3.connect("patient.db")
               current = conn.cursor()
               query = 'INSERT INTO patient (username, password) VALUES (?, ?)'
               values = (request.form['username'], request.form['password'])
               current.execute(query, values)
               conn.commit()
               current.close()
               conn.close()
               con = sqlite3.connect("patientsignup.db")
               cur = con.cursor()
               Query = 'INSERT INTO PatientSignUp (full_name, username, email, password) VALUES (?, ?, ?, ?)'
               vals = (request.form['full_name'], request.form['username'], request.form['email'] ,request.form['password'])           
               cur.execute(Query, vals)
               con.commit()
               cur.close()
               con.close()
               return redirect('/patientlogin')
            else:
             return "Please try again the confirm password does not match with the password"
       
    @app.route('/workerlogin/workerssignup', methods=("POST", ))
    def Signup():
       
       if request.method == "POST": 
          password = request.form['password']
          confirm_password = request.form['confirm_password']
          if password == confirm_password:
             con = sqlite3.connect("worker.db")
             curr = con.cursor()
             Query = 'INSERT INTO worker (username, password) VALUES (?, ?)'
             vals = (request.form['username'], request.form['password'])
             curr.execute(Query, vals)
             con.commit()
             curr.close()
             conn = sqlite3.connect("WorkerInfo.db")
             current = conn.cursor()
             query = 'INSERT INTO HealthWorker (full_name, username, email, password, occupation, phone_number, address, dob, gender) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
             values = (request.form['full_name'], request.form['username'], request.form['email'] ,request.form['password'], request.form['occupation'], request.form['phone_number'], request.form['address'], request.form['dob'], request.form['gender'])           
             current.execute(query, values)
             conn.commit()
             current.close()
             conn.close()
             return redirect('/workerlogin')
          else:
             return "Please try again the confirm password does not match with the password"
    @app.route('/workerlogin/workerssignup', methods=("GET",))
    def worker_sign_up():
       return render_template('signupashealthworkernew.html')
       
          
       
    
       


    @app.route('/patientlog', methods=("GET",))
    def patient():
        selected_day = request.form['selected_day']
        selected_time = request.form['selected_time']
        return render_template("res.html", day=selected_day, time=selected_time)



    

        
    
    


    return app

    




app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
