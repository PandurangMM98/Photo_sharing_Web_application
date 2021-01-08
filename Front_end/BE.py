import os
from flask import Flask,flash,redirect,render_template,request,session,abort,jsonify,make_response
from werkzeug.exceptions import HTTPException, default_exceptions, abort, Aborter
from flask_sqlalchemy import SQLAlchemy
import hashlib
from base64 import b64encode
from datetime import datetime
import json
import requests
import ast
import re

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "reg.db"))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

class Reg(db.Model):
    username = db.Column(db.String(80), unique = True, nullable=False, primary_key=True)
    password = db.Column(db.String(40), nullable=False)
    	
class Category(db.Model):
	category = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
	count = db.Column(db.Integer)

class Images(db.Model):
	#num = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
	actId = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
	user = db.Column(db.String(80), nullable=False)
	timestamp = db.Column(db.String(100), nullable=False)
	caption = db.Column(db.String(10000))
	upvotes = db.Column(db.Integer)
	img64 = db.Column(db.String(300))
	category = db.Column(db.String(80))


@app.errorhandler(400)
def not_found(error):
	return make_response(jsonify({}), 400)

@app.errorhandler(405)
def not_found(error):
	return make_response(jsonify({}), 405)

@app.route("/")
def home():
	return "BACKEND"

#API 1
@app.route("/api/v1/users", methods=['POST', 'GET'])
def adduser():
	if request.method=='POST':
		#GET DATA IN JSON 
		data = request.get_json()
		#USERNAME
		us = data['username']
		temp = Reg.query.filter_by(username=us).first()
		if temp is not None:
			return make_response(jsonify({}), 400)
		#PASSWORD
		pa = data['password']
		if len(pa)!=40 and all(char in string.hexdigits for char in pa) and type(pa)!=str:
			return make_response(jsonify({}), 400)
		#DATABASE UPDATE
		temp = Reg(username=us, password=pa)
		db.session.add(temp)
		db.session.commit()
		return make_response(jsonify({}), 201)
	else:
		return make_response(jsonify({}), 405)

#API 2
@app.route("/api/v1/users/<username>", methods=['DELETE','GET'])
def removeuser(username):
	#GET DATA IN JSON
	data = request.get_json()
	if request.method=='DELETE':
		temp = Reg.query.filter_by(username = username).first()
		if temp is None:
			return make_response(jsonify({}),400)
		else:
			db.session.delete(temp)
			db.session.commit()
			return make_response(jsonify({}),200)
	else:
		return make_response(jsonify({}), 405)


#API 3 & 4
@app.route("/api/v1/categories", methods=['POST', 'GET'])
def category():
	if request.method=='GET':
		#GET DATA JSON
		data = request.get_json()
		#QUERYING
		all_cat = Category.query.all()
		if len(all_cat)==0:
			return make_response(jsonify({}), 204)
		#RESPONSE
		response = dict()
		for obj in all_cat:
			response[obj.category] = obj.count
		if bool(response) is False:
			return make_response(jsonify({}), 204)
		return make_response(jsonify(response), 200)

	elif request.method=='POST':
		#GET DATA JSON
		data = request.get_json()
		#ca = "".join(i.encode("UTF-8") for i in data)
		print(type(data), data)
		ca = "".join(i.encode("UTF-8") for i in data)
		print(type(ca), ca)
		#QUERY
		temp1 = Category.query.filter_by(category = ca).first()
		if temp1 is not None:
			return make_response(jsonify({}), 400)	
		#DATABASE UPDATE
		temp = Category(category = ca, count = 0)
		db.session.add(temp)
		db.session.commit()
		return make_response(jsonify({}), 201)
	
	else:
		return make_response(jsonify({}), 405)

#API 5
@app.route("/api/v1/categories/<categoryName>", methods = ['DELETE', 'GET'])
def removecat(categoryName):
	data = request.get_json()
	if request.method=='DELETE':
		temp = Category.query.filter_by(category = categoryName).first()
		if temp is None:
			return make_response(jsonify({}), 400)
		else:
			db.session.delete(temp)
			db.session.commit()
			return make_response(jsonify({}), 200)
	else:
		return make_response(jsonify({}), 405)

#API 6 & 8
@app.route("/api/v1/categories/<categoryName>/acts", methods=['GET'])
def list_acts(categoryName):
	if request.method=='GET':
		data = request.get_json()
		temp = Images.query.filter_by(category=categoryName).all()
		if len(temp)==0:
			return make_response(json.dumps([]), 204)
		if len(temp)>100:
			return make_response(json.dumps([]), 413)
		response = [{"actId":obj.actId, "username":obj.user, "timestamp":obj.timestamp, \
					"caption":obj.caption, "upvotes":obj.upvotes, "imgB64":obj.img64} \
					for obj in temp] 
		response1 = sorted(response, key=lambda k:k['timestamp'], reverse=True)
		
		if request.args:
			start = int(request.args.get('start'))
			end = int(request.args.get("end"))
			if end-start+1 > 100:
				return make_response(json.dumps([]), 413)
			response2 = response1[start-1:end]
			return make_response(json.dumps(response2), 200)
		else:
			return make_response(json.dumps(response1), 200)
	else:
		return make_response(jsonify({}), 405)

#API 7
@app.route("/api/v1/categories/<categoryName>/acts/size",methods=['GET'])
def size(categoryName):
	if request.method=='GET':
		data = request.get_json()
		temp = Images.query.filter_by(category = categoryName).all()
		if len(temp)==0:
			return make_response(json.dumps([]), 204)
		length = len(temp)
		return make_response(json.dumps([length]), 200)
	else:
		return make_response(json.dumps([]), 405)


#API 9
@app.route("/api/v1/acts/upvote", methods=["GET", "POST"])
def upvote():
	if request.method == "POST":
		data = request.get_json()
		aid = data[0]
		temp = Images.query.filter_by(actId=aid).first()
		if temp is None:
			return make_response(json.dumps([]), 400)
		temp.upvotes = temp.upvotes + 1
		db.session.commit()
		temp = Images.query.filter_by(actId=aid).first()
		print(temp.actId, temp.upvotes)
		return make_response(json.dumps([]), 200)
	else:
		return make_response(json.dumps([]), 405)

#API 10
@app.route("/api/v1/acts/<actId>", methods=['DELETE', 'GET'])
def remove_act(actId):
	if request.method=='DELETE':
		data = request.get_json()
		temp = Images.query.filter_by(actId = actId).first()
		if temp is None:
			return make_response(jsonify({}), 400)
		else:
			temp1 = Category.query.filter_by(category=temp.category).first()
			temp1.count = temp1.count - 1
			db.session.commit()
			db.session.delete(temp)
			db.session.commit()
			return make_response(jsonify({}), 200)
	else:
		return make_response(jsonify({}), 405)

#API 11
@app.route("/api/v1/acts", methods=['POST', 'GET'])
def upload_act():
	if request.method == 'POST':
		data = request.get_json()

		aid = data['actId']
		temp = Images.query.filter_by(actId=aid).first()
		if temp is not None:
			return make_response(jsonify({}), 400)

		us = data['username']
		temp = Reg.query.filter_by(username=us).first()
		if temp is None:
			return make_response(jsonify({}), 400)

		cap = data['caption']
		cat = data['category']
		temp = Category.query.filter_by(category=cat).first()
		temp.count = temp.count+1
		db.session.commit()

		time = data['timestamp']
		try:
			datetime.strptime(time, '%d-%m-%Y:%S-%M-%H')
		except:
			return make_response(jsonify({}), 400)
		
		img64 = data['imgB64']

		temp = Images(actId=aid,user=us,category=cat,caption=cap,upvotes=0,timestamp=time,img64=img64)
		db.session.add(temp)
		db.session.commit()
		return make_response(jsonify({}), 201)
	else:
		return make_response(jsonify({}), 405)

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=80)
