from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re

app = Flask(__name__)
app.secret_key = 'keepitsecretkeepitsafe'
mysql = MySQLConnector(app,'emails')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
    query = "SELECT * FROM emails"                           # define your query
    emails = mysql.query_db(query)                           # run query with query_db()
    print emails
    return render_template('index.html', all_emails=emails)

@app.route('/process', methods=['POST'])
def validate():
    emailID=request.form['email']
    if EMAIL_REGEX.match(request.form['email']):
        query = "SELECT email FROM emails"
        emails = mysql.query_db(query)
        if len(emails) == 0:
            query = "INSERT INTO emails (email, created_at, updated_at) VALUES (:email, NOW(), NOW())"
            data = {
                'email': request.form['email']
                }
            mysql.query_db(query, data)
            flash('The email address '+emailID +" has been successfully added!")
            return redirect('/success')
        if len(emails) != 0:
            for i in emails:
                print i['email']
                if i['email']==request.form['email']:
                    flash('Email address already exists. Please try again')
                    return redirect('/')
            else:
                query = "INSERT INTO emails (email, created_at, updated_at) VALUES (:email, NOW(), NOW())" 
                data = {
                    'email': request.form['email']
                    }
                mysql.query_db(query, data)
                flash('The email address '+emailID +" has been successfully added!")
                return redirect('/success')
    else:
        flash('Invalid Email!')
    return redirect('/')

@app.route('/success')
def success():
    query = "SELECT * FROM emails"
    emails = mysql.query_db(query)
    return render_template('success.html', emails=emails)

@app.route('/delete', methods=["POST"])
def delete():
    emailId=request.form['email']
    query = "DELETE FROM emails WHERE email = :email"
    data = {'email' : emailId}
    mysql.query_db(query, data)
    flash("The email address "+emailId +" has been successfully deleted!")
    return redirect('/success')

app.run(debug=True)