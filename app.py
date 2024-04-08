from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from sqlite3 import Error
import os

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


    @app.route('/appointments')

    def appointments():
        return render_template("index.html", 'index')

    @app.route('/addpatient', methods=("POST",))
    def add_new_patient():
        conn = None
        try:
           conn = sqlite3.connect("patient.db")
        except Error as e:
            return "Error connecting to the database"
    
        try:
            current = conn.cursor()
            query = "INSERT INTO patient (name, password) VALUES ( ?, ?, ?, ?)"
            values = (request.form['name'], request.form['password'])
            current.execute(query, values)
            conn.commit
            current.close()
        except Error as e:
            return "Error making the query"
        finally:
            conn.close

        return render_template("index.html", page_title="index")
    

    @app.route('/', methods=("GET",))
    def hello():
        return render_template("in.html", page_title="hello")
    return app

    




app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
