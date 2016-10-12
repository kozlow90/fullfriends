from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')


app = Flask(__name__)
app.secret_key = "ThisIsSecret!"
mysql = MySQLConnector('fullfriends')


@app.route('/')
def index():
	friends=mysql.fetch("SELECT * from friends")
	return render_template('index.html',friends=friends)


@app.route('/friends',methods=['POST'])
def create():
	if len(request.form['name'])<1:
		flash("name cannot be empty")
	else:
		query = "INSERT INTO friends (name) VALUES ('{}')".format(request.form['name'])
		mysql.run_mysql_query(query)
	return redirect('/')


@app.route('/friends/<id>/edit',methods=['GET'])
def edit(id):
	friend = mysql.fetch(("SELECT * from friends where id='{}'").format(id))
	print friend
	return render_template("update.html",friend = friend)


@app.route('/update/<id>',methods=['POST'])
def update(id):
	query = "UPDATE friends SET name = '{}' WHERE id = {}".format(request.form['name'],id)
	mysql.run_mysql_query(query)
	return redirect('/')

@app.route('/friends/<id>/delete',methods=['POST'])
def destroy(id):
	query = "DELETE from friends WHERE id = {}".format(id)
	mysql.run_mysql_query(query)
	return redirect('/')

	
app.run(debug=True)