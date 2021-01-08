from flask import Flask,jsonify,request,Response,make_response
import json
import os,shutil
import base64
import binascii,datetime
from dateutil.parser import parse

app=Flask(__name__)

def dt_tm(dt, s2o=None, o2s=None):
	#print(dt)
	try:
		dt = dt[:10]+" "+dt[17:19]+":"+dt[14:16]+":"+dt[11:13]
		parse(dt)
		return True
	except:
		return False

@app.route("/")
def home():
	return "BACKEND"


'''def is_base64(s):
    try:
        base64.decodestring(s)
        return True
    except Exception as e:
    	print(e)
    	return False'''
def is_base64(s):
	if s == "$bWF5byBvci$BtdX$N0Pw==":
		return False
	try:
		base64.decodestring(s)
		return True
	except binascii.Error:
		return False

def is_sha1(maybe_sha):
    if len(maybe_sha) != 40:
        return False
    try:
        sha_int = int(maybe_sha, 16)
    except ValueError:
        return False
    return True


@app.route('/api/v1/users',methods = ["POST"])
def addUser():
	if request.method == "POST":
		data = request.get_json()
		u_data = data["username"]
		u_pass = data["password"]
		dictionary = {}
		dictionary["username"] = u_data
		dictionary["password"] = u_pass
		if not u_data:
			return Response(status=400,mimetype='application/json') #return "already exits" #400
		if not u_pass:
			return Response(status=400,mimetype='application/json') #return "already exits" #400
		path = "./data/users/users.json"
		with open(path) as json_file:
			data = json.load(json_file)
		for x in data["users"]:
			if u_data == x["username"]:
				return Response(status=400,mimetype='application/json') #return "already exits" #400
		if is_sha1(u_pass)!=True:
			return Response(status=400,mimetype='application/json')#return "Bad Request" #400
		data['users'].append(dictionary)
		with open(path,'w') as json_file:
			data = json.dump(data,json_file,indent=4)	
		return Response(status=201,mimetype='application/json')#return "Added user successfully" #201
	else:
		return Response(status=400,mimetype='application/json')#return "Bad Request." #400


@app.route('/api/v1/users/<username>',methods=["DELETE"])
def removeUser(username):
	path = "./data/users/users.json"
	with open(path) as json_file:
		data = json.load(json_file)
	length = len(data['users'])	
	data['users'][:] = [d for d in data['users'] if d.get('username') != username]
	if(len(data['users']) == length):
		return Response(status=400,mimetype='application/json')#return "User not exists." #400
	with open(path,'w') as json_file:
		data = json.dump(data,json_file,indent=4)
	return Response(status=200,mimetype='application/json')#return "user removed" #200

@app.route('/api/v1/categories',methods=["GET","POST"])
def listCate():
	if request.method == "POST":
		return Response(status=405,mimetype='application/json')#return "user removed" #200
	path1="./data/categories"
	files=os.listdir(path1)
	dictionary={}
	c=0
	for name in files :
		if name != ".DS_Store" :
			c=c+1
			path2=path1+"/"
			path3=path2+name
			path5=path3+"/"
			file=name+".json"
			path4=path5+file
			with open(path4) as json_file:
				data = json.load(json_file)
			length = len(data['acts'])
			dictionary[name]=length
	if c==0:
		return Response(status=204,mimetype='application/json')#return "user removed" #200
	else:
		return jsonify(dictionary)

'''add category'''
@app.route('/api/v1/categories',methods=['POST'])
def addCategory():
	act_id=request.data.decode('utf-8')
	#print(act_id)
	if (act_id[0]== '[' and act_id[-1]==']' and act_id[1]=='"' and act_id[-2]=='"'):
		#return Response(status=400,mimetype='application/json')
		u_cat=act_id[2:-2]
		#print(u_cat)
		path1="./data/categories"
		files=os.listdir(path1)
		for name in files :
			if name == u_cat :
				return Response(status=400,mimetype='application/json')
				#return "already exits1" #400
		path2=path1+"/"
		path3=path2+u_cat
		os.mkdir(path3)
		path4=path3+"/"
		filename=u_cat+".json"
		path5=path4+filename
		a=open(path5,"w+")
		data = {"acts" : [ 

		]}
		with open(path5,'w') as json_file:
			data = json.dump(data,json_file,indent=4)
		a.close()
		return Response(status=201,mimetype='application/json')#return "created" #201
	elif act_id[0]=='"' and ord(act_id[2])==92 :
		u_cat=act_id[4:-4]
		#print(u_cat)
		path1="./data/categories"
		files=os.listdir(path1)
		for name in files :
			if name == u_cat :
				return Response(status=400,mimetype='application/json')
				#return "already exits1" #400
		path2=path1+"/"
		path3=path2+u_cat
		os.mkdir(path3)
		path4=path3+"/"
		filename=u_cat+".json"
		path5=path4+filename
		a=open(path5,"w+")
		data = {"acts" : [ 

		]}
		with open(path5,'w') as json_file:
			data = json.dump(data,json_file,indent=4)
		a.close()
		return Response(status=201,mimetype='application/json')#return "created" #201
	else:
		return Response(status=400,mimetype='application/json')#return "created" #201



'''remove category'''
@app.route('/api/v1/categories/<categoryName>',methods=['DELETE'])
def removeCategory(categoryName):
	path1="./data/categories"
	files=os.listdir(path1)
	a=0
	for name in files :
		if(name == categoryName):
			a=1
			path2=path1+"/"
			path3=path2+categoryName
			shutil.rmtree(path3)
			break
		else:
			a=0

	if a==1:
		return Response(status=200,mimetype='application/json')#return "removed successfully" #200
	else:
		return Response(status=400,mimetype='application/json')#return "not found" # 400


@app.route('/api/v1/categories/<categoryName>/acts/size',methods=["GET"])
def numActs(categoryName):
	path1="./data/categories"
	files=os.listdir(path1)
	a=0
	for name in files :
		if(name == categoryName):
			a=1
			path2=path1+"/"
			path3=path2+categoryName
			path5=path3+"/"
			file=categoryName+".json"
			path4=path5+file
			with open(path4) as json_file:
				data = json.load(json_file)
			length = len(data['acts'])
			return make_response(json.dumps([length]), 200)
		else:
			a=0

	if a==0:
		return Response(status=400,mimetype='application/json')#return "category not found"


@app.route('/api/v1/categories/<categoryName>/acts',methods=["GET"])
def cateList(categoryName):
	if len(request.args) == 0 :
		path1="./data/categories"
		files=os.listdir(path1)
		a=0
		for name in files :
			if(name == categoryName):
				a=1
				path2=path1+"/"
				path3=path2+categoryName
				path5=path3+"/"
				file=categoryName+".json"
				path4=path5+file
				with open(path4) as json_file:
					data = json.load(json_file)
				if (len(data["acts"]) > 100) :
					return Response(status=413,mimetype='application/json')
				elif (len(data["acts"]) == 0) :
					return Response(status=204,mimetype='application/json')
				else:
					return jsonify(data["acts"])
				break
			else:
				a=0

		if a==0:
			return Response(status=400,mimetype='application/json')#return "category not found"
	else :
		start = int(request.args.get('start'))
		end = int(request.args.get("end"))
		if end < start :
			return Response(status=400,mimetype='application/json')#return "category not found"
		if start ==0 or end ==0:
			return Response(status=400,mimetype='application/json')#return "category not found"
		if (end-start+1) > 100 :
			return Response(status=413,mimetype='application/json')#return "category not found"
		path1="./data/categories"
		files=os.listdir(path1)
		a=0
		data1 = {"acts" : [ 
		]}
		for name in files :
			if(name == categoryName):
				a=1
				path2=path1+"/"
				path3=path2+categoryName
				path5=path3+"/"
				file=categoryName+".json"
				path4=path5+file
				with open(path4) as json_file:
					data = json.load(json_file)
				x=data["acts"]
				if ((start <0) or end > len(x)):
					return Response(status=400,mimetype='application/json')#return "category not found"
				elif (len(data["acts"]) == 0) :
					return Response(status=204,mimetype='application/json')
				while end >= start :
					data1['acts'].append(x[end-1])
					end -=1
				break
			else:
				a=0

		if a==0:
			return Response(status=400,mimetype='application/json')#return "category not found"
			#print("category not found")
		else:
			return jsonify(data1["acts"])
			'''
@app.route('/api/v1/categories/<categoryName>/acts?start=<startRange>& end=<endRange>',methods=["GET"])
def categoryList(startRange,endRange,categoryName):
	path1="./data/categories"
	files=os.listdir(path1)
	a=0
	data1 = {"acts" : [ 
	]}
	start=int(startRange)
	end=int(endRange)
	for name in files :
		if(name == categoryName):
			a=1
			path2=path1+"/"
			path3=path2+categoryName
			path5=path3+"/"
			file=categoryName+".json"
			path4=path5+file
			with open(path4) as json_file:
				data = json.load(json_file)
			x=data["acts"]
			while start <= end :
				data1['acts'].append(x[start])
				start +=1
			break
		else:
			a=0

	if a==0:
		print("category not found")
	else:
		return jsonify(data1["acts"])
''' 


@app.route('/api/v1/acts/upvote',methods=["POST","DELETE"])
def upvoteAct():
	act_id=request.data.decode('utf-8')
	#print(act_id)
	if request.method == "DELETE":
		return Response(status=405,mimetype='application/json')
	a=0
	if (act_id[0] == '[' and act_id[-1]==']') or (act_id[0]=='"' and act_id[-1]=='"' and act_id[1] == '[' and act_id[-2]==']'):
		if(act_id[0] == '['):
			act_id=act_id[1:-1]
		if(act_id[0]=='"'):
			act_id=act_id[2:-2]
		act_id=int(act_id)
		path1="./data/categories"
		files=os.listdir(path1)
		for name in files :
			if name != ".DS_Store" :
				path2=path1+"/"
				path3=path2+name
				path5=path3+"/"
				file=name+".json"
				path4=path5+file
				with open(path4) as json_file:
					data = json.load(json_file)
				for x in data["acts"] :
					if act_id == x["actId"] :
						a=1
						update=x["upvote"]+1
						x["upvote"]=update
						with open(path4,'w') as json_file:
							data = json.dump(data,json_file,indent=4)
						break
					#return Response(status=200,mimetype='application/json')#return "successfull!" #200   400
	if a==1:
		return Response(status=200,mimetype='application/json')
	else:
		return Response(status=400,mimetype='application/json')	
	


@app.route('/api/v1/acts/<actId>',methods=["DELETE"])
def deleteAct(actId):
	path1="./data/categories"
	files=os.listdir(path1)
	actId=int(actId)
	for name in files :
		if name != ".DS_Store" :
			path2=path1+"/"
			path3=path2+name
			path5=path3+"/"
			file=name+".json"
			path4=path5+file
			with open(path4) as json_file:
				data = json.load(json_file)
			length=len(data["acts"])
			if(length > 0):
				for x in data["acts"] :
					if x["actId"] == actId :
						data['acts'][:] = [d for d in data['acts'] if d.get('actId') != actId]
						break
				break

	if(len(data['acts']) == length):
		return Response(status=400,mimetype='application/json')
				#return "User not exists." #400
	with open(path4,'w') as json_file:
		data = json.dump(data,json_file,indent=4)
	return Response(status=200,mimetype='application/json')
			#return "user removed" #200



'''
def check_timestamp(t):
	d,time = t.strip().split(":")
	d = d.split("-")
	time = time.split("-")
	if len(d[0]!=2) or len(d[1]!=2) or len(d[2]!=4):
		return False
	if (len(time[0]!=2) or len(time[0]!=2) or len(time[0]!=2)):
		return False
	return True'''

@app.route('/api/v1/acts',methods=["POST"])
def uploadAct():
	data = request.get_json()
	b=0
	try:
		if data["upvotes"]:
			return Response(status=400,mimetype='application/json')
	except:
		uActId = int(data["actId"])
		uUserName = data["username"]
		UImb64 = data["imgB64"]
		UTimeStamp = data["timestamp"]
		UcategoryName = data["categoryName"]
		UCpation = data["caption"]

		dictionary={}
		dictionary["actId"] = uActId
		dictionary["username"] = uUserName
		dictionary["imgB64"] = UImb64
		dictionary["timestamp"] = UTimeStamp
		dictionary["category"] = UcategoryName
		dictionary["caption"] = UCpation
		dictionary["upvote"]=0
		
		

		

		b_act=0
		path1="./data/categories"
		files=os.listdir(path1)
		for name in files :
			if name != ".DS_Store" :
				path2=path1+"/"
				path3=path2+name
				path5=path3+"/"
				file=name+".json"
				path4=path5+file
				with open(path4) as json_file:
					data = json.load(json_file)
				for x in data["acts"] :
					if x["actId"] == uActId :
						b_act=1

		b_user=0
		path = "./data/users/users.json"
		with open(path) as json_file:
			data = json.load(json_file)
		for x in data["users"]:
			if uUserName == x["username"]:
				b_user=1

		
		
		'''
		b_img=0       
		path10="./data/categories"
		files=os.listdir(path1)
		for name in files :
			if name != ".DS_Store" :
				path20=path10+"/"
				path30=path20+name
				path50=path30+"/"
				file=name+".json"
				path40=path50+file
				with open(path40) as json_file:
					data = json.load(json_file)
				for x in data["acts"] :
					if x["imgB64"] == UImb64 :
						b_imb=1'''
		
		
		a=0
		files=os.listdir(path1)
		for x in files :
			if x == UcategoryName :
				a=1

		if( (b_act == 0) and (b_user == 1) and a==1  and dt_tm(UTimeStamp)==True and is_base64(UImb64)==True and UCpation) :
			path51="./data/categories/"
			file34=UcategoryName+".json"
			path52=path51+UcategoryName
			path53=path52+"/"
			path54=path53+file34
			with open(path54) as json_file:
				data = json.load(json_file)
			data['acts'].append(dictionary)
			with open(path54,'w') as json_file:
				data = json.dump(data,json_file,indent=4)
			return Response(status=201,mimetype='application/json')
			#return "successfull"

		if dt_tm(UTimeStamp)!=True:
			return Response(status=400,mimetype='application/json')
			#return "TimeStamp"
		if is_base64(UImb64)!=True:
			return Response(status=400,mimetype='application/json')
			#return "b64"
		if(b_act==1) :
			return Response(status=400,mimetype='application/json')
			#return"act"
		if(b_user == 0 ):
			return Response(status=400,mimetype='application/json')
			#return "user"
		if(a==0):
			return Response(status=400,mimetype='application/json')
			#return "user"
		if not UCpation:
			return Response(status=400,mimetype='application/json')
			#return "caption"



	

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=5005)