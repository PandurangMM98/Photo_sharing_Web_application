import os
from flask import Flask,flash,redirect,render_template,request,session,abort,jsonify,make_response
import hashlib
from base64 import b64encode
import datetime
import json
import ast
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key1'

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/cat1")
def cat1():
	return render_template("c1.html")

@app.route("/cat2")
def cat2():
	return render_template("c2.html")

@app.route("/cat3")
def cat3():
	return render_template("c3.html")

@app.route("/cat4")
def cat4():
	return render_template("c4.html")

@app.route("/signup")
def signup():
	return render_template("register.html")

@app.route("/deleteuser")
def delete_account():
	return render_template("deleteuser.html")

@app.route("/cat")
def cat():
	return render_template("category.html")

@app.route("/deletecat")
def deletecat():
	return render_template("deletecat.html")

@app.route("/querycat")
def querycat():
	return render_template("querycat.html")

@app.route("/queryrange")
def range():
	return render_template("range.html")

@app.route("/upload")
def upload():
	return render_template("upload.html")

@app.route("/deleteact")
def deleteact():
	return render_template("deleteact.html")

@app.route("/blog")
def blog():
	return render_template("blog.html")

#API 1
@app.route("/adduser", methods=['GET', 'POST'])
def validate_user():
	#print(here)
	user = request.form.get("username")
	pwd = request.form.get("password")
	sec_pwd = hashlib.sha1(pwd.encode())
	data = {"username": user, "password": sec_pwd.hexdigest()} 
	r = requests.post("http://0.0.0.0:5005/api/v1/users", json=data)
	if r.status_code==201:
		return render_template("/errors/201.html")
	elif r.status_code==400:
		return render_template("/errors/400.html")
	elif r.status_code==405:
		return render_template("/errors/405.html")

#API 2
@app.route("/removeuser", methods=['POST','DELETE','GET'])
def delete_user():
	user = request.form.get("username")
	data = list()
	r = requests.delete("http://0.0.0.0:5005/api/v1/users/"+user, json=data)
	if r.status_code==200:
		return render_template("/errors/200.html", temp={}, templist=[])
	elif r.status_code==400:
		return render_template("/errors/400.html")
	elif r.status_code==405:
		return render_template("/errors/405.html")

#API 3 & 4
@app.route("/listAdd", methods=['GET', 'POST'])
def list_add_categories():
	if request.method=='GET':
		data = {}
		r = requests.get("http://52.21.60.17:80/api/v1/categories", json=data)
		temp = r.text
		temp = ast.literal_eval(temp)
		if r.status_code==200:
			return render_template("/errors/200.html", temp=temp, templist=[])
		elif r.status_code==204:
			return render_template("/errors/204.html")
		elif r.status_code==405:
			return render_template("/errors/405.html")


	elif request.method=='POST':
		cat = request.form.get("category")
		data = list(cat)
		r = requests.post("http://52.202.223.101:80/api/v1/categories", json=data)
		if r.status_code==201:
			return redirect("/cat")
		elif r.status_code==400:
			return render_template("/errors/400.html")
		elif r.status_code==405:
			return render_template("/errors/405.html")
	else:
		abort(405)

#API 5
@app.route("/removecat", methods=['POST','DELETE','GET'])
def remove_category():
	categoryName = request.form.get("category")
	data = list()
	r = requests.delete("http://52.202.223.101:80/api/v1/categories/"+categoryName, json=data)
	if r.status_code==200:
		return redirect("/listAdd")
	elif r.status_code==400:
		return render_template("/errors/400.html")
	elif r.status_code==405:
		return render_template("/errors/405.html")	


#API 6
@app.route("/querycategory", methods = ['POST','GET'])
def list_acts():
	categoryName = request.form.get("category")
	data = {}
	r = requests.get("http://52.202.223.101:80/api/v1/categories/"+categoryName+"/acts", data=data)
	if r.status_code==200:
		temp1 = r.text
		temp1 = ast.literal_eval(temp1)
		return render_template("/errors/200.html", temp={}, templist = temp1)
	elif r.status_code==204:
		return render_template("/errors/204.html")
	elif r.status_code==405:
		return render_template("/errors/405.html")
	elif r.status_code==413:
		return render_template("/errors/413.html")	

#API 7
@app.route("/sizecategory", methods = ['POST','GET'])
def listsize():
	categoryName = request.form.get("category")
	data = {}
	r = requests.get("http://52.202.223.101:80/api/v1/categories/"+categoryName+"/acts/size", data=data)
	#print(r.status_code)
	temp1 = r.text
	if len(temp1) > 0:
		temp1 = ast.literal_eval(temp1)
	#print(temp1)
	if r.status_code==200:
		return render_template("/errors/200.html", temp={}, templist = temp1)
	elif r.status_code==204:
		return render_template("/errors/204.html")
	elif r.status_code==405:
		return render_template("/errors/405.html")


#API 8
@app.route("/rangequery", methods=['GET'])
def rangeacts():
	if request.method=="GET":
		cat = request.args.get("cat_name")
		start = request.args.get("start")
		end = request.args.get("end")
		data = {}
		r = requests.get("http://52.202.223.101:80/api/v1/categories/"+cat+"/acts?start="+start+"&end="+end, json=data)
		#print(r.status_code)
		if r.status_code==200:
			temp1 = r.text
			if len(temp1) > 0:
				temp1 = ast.literal_eval(temp1)
			return render_template("/errors/200.html", temp={}, templist = temp1)
		elif r.status_code==204:
			return render_template("/errors/204.html")
		elif r.status_code==405:
			return render_template("/errors/405.html")
		elif r.status_code==413:
			return render_template("/errors/413.html")
	else:
		abort(405)

#API 9
@app.route("/upvote", methods=['POST', "GET"])
def upvote():
	if request.method == "POST":
		aid = request.form.get("actid")
		data = [aid]
		r = requests.post("http://52.202.223.101:80/api/v1/acts/upvote", json=data)
		temp = r.text
		if r.status_code==200:
			return render_template("/errors/200.html", temp={}, templist=[])
		elif r.status_code==400:
			return render_template("/errors/400.html")
		elif r.status_code==405:
			return render_template("/errors/405.html")
	else:
		abort(405)

#API 10
@app.route("/actdelete", methods=['POST','DELETE','GET'])
def removeact():
	aid = request.form.get("actid")
	data = list()
	r = requests.delete("http://52.202.223.101:80/api/v1/acts/"+aid, json=data)
	if r.status_code==200:
		return render_template("/errors/200.html", temp={}, templist=[])
	elif r.status_code==400:
		return render_template("/errors/400.html")
	elif r.status_code==405:
		return render_template("/errors/405.html")

#API 11
@app.route("/upload_act", methods = ['GET', 'POST'])
def upload_act():
	actid = request.form.get('actid')
	username = request.form.get('username')
	category = request.form.get('category')
	caption = request.form.get("caption")
	#timestamp = str(datetime.now())
	s = str(datetime.datetime.now())
	d = datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S.%f')
	timestamp =  datetime.datetime.strftime(d, '%d-%m-%Y:%S-%M-%H')
	img = request.files['inputFile']
	img64 = b64encode(img.read())
	
	data = {"actId":actid, "username":username, "category":category, "timestamp":timestamp,"caption":caption,"imgB64": img64}

	r = requests.post("http://52.202.223.101:80/api/v1/acts", json=data)
	if r.status_code==201:
		return redirect("/upload")
	elif r.status_code==400:
		return render_template("/errors/400.html")
	elif r.status_code==405:
		return render_template("/errors/405.html")	


if __name__ == '__main__':
	app.run(host="0.0.0.0" , debug=True, port=5000)
	


