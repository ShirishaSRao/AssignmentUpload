from flask import Flask, render_template, Markup, request, redirect,jsonify,abort
import requests
import os
#from werkzeug import secure_filename
from flask_cors import CORS
from flask_static_compress import FlaskStaticCompress
import logging
from flask_pymongo import PyMongo
import pymongo
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import glob

UPLOAD_FOLDER = 'database'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
count=0

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

#app.config["UPLOAD_FOLDER"]="/Users/shirishasrao/Desktop/AssignmentUpload/database"
#app.config["MONGO_URI"]= "mongodb+srv://shivangijadon16:pikachu4321@cluster0-wu1c9.mongodb.net/test?retryWrites=true&w=majority"
#mongo = pymongo.MongoClient("mongodb+srv://shivangijadon16:pikachu4321@cluster0-wu1c9.mongodb.net/test?retryWrites=true&w=majority")

def plagiarism_check():
	file_list=glob.glob("database/*.txt")
	corpus=[]
	for file_path in file_list:
		with open(file_path) as f_input:
			corpus.append(f_input.read())
	tfidf = TfidfVectorizer().fit_transform(corpus)
	pairwise_similarity = tfidf * tfidf.T
	a= pairwise_similarity.toarray()   
	print(a)
	n=len(corpus)
	for i in range(n-1):
		if(a[n-1][i]>0.75):
			return a[n-1][i]
	return 0		

#db = pymongo.database.Database(mongo, 'user_cred')
#usercol = db["user_col"]


@app.route('/',methods=["GET"])
def check():
    filename="database/usercol.json"
    with open(filename,'r') as f:
        data=json.load(f)
        print(data)
        print(data["users"])
    return "",200

@app.route('/api/v1/login',methods=['POST'])
def login():
    username =  request.form['username']
    password = request.form['password']
    filename="database/usercol.json"
    with open(filename,'r') as f:
        data=json.load(f)
        for i in data["users"]:
            if(i["username"]==username):
                if(i["password"]==password):
                    return jsonify({"username":username,"name":i["name"],"type":i["type"]}),200
                else:
                    return "Password Incorrect!",400
    return "Account does not exists!",400


@app.route('/api/v1/get/assignment/completed/<username>',methods=["GET"])
def get_completed_assignment(username):
    filename="database/usercol.json"
    with open(filename,'r') as f:
        data=json.load(f)
        for i in data["users"]:
            if(i["username"]==username):
                return jsonify({"Completed":i["Completed"]}),200

@app.route('/api/v1/get/assignment/pending/<username>',methods=["GET"])
def get_pending_assignment(username):
    filename="database/usercol.json"
    with open(filename,'r') as f:
        data=json.load(f)
        for i in data["users"]:
            if(i["username"]==username):
                return jsonify({"Pending":i["Pending"]}),200
    

@app.route('/api/v1/create/assignment',methods=["POST"])
def create_assignment():
    name=request.form["name"]
    filename="database/usercol.json"
    data={}
    with open(filename,'r') as f:
        data=json.load(f)
        print(type(data))
        for i in data["users"]:
            if(i["type"]=="student"):
                temp=i["Pending"]
                temp.append(name)
    print(data)
    with open(filename,"w") as f:
        json.dump(data,f)
    return "",200

@app.route('/api/v1/upload/<assignment_name>',methods=["POST"])
def upload(assignment_name):
    file=request.files['chooseFile']
    print(file.filename)
    filename=file.filename.split('.')[0]+file.filename.split('.')[-1]
    try:
        os.mkdir("database/"+assignment_name)
    except:
        pass
    file.save("database"+'/'+assignment_name+'/'+filename) 
    if(plagiarism_check()):
        return "Did not Pass Plagiarism check,PLease Reupload",400
    #print 'GET=',file.filename
    #print 'UPLOAD=',filename,'#'*50
    return jsonify({"path":"gg"}),200

@app.route('/api/v1/change_assignment/<username>',methods=["POST"])
def change(username):
    print(request)
    assignment=request.form['assignment_name']
    filename="database/usercol.json"
    data={}
    print(assignment)
    with open(filename,'r') as f:
        data=json.load(f)
        for i in data["users"]:
            if(i["name"]==username):
                temp=i["Pending"]
                temp.remove(assignment)
                print(temp)
                i["Pending"]=temp
                temp1=i["Completed"]
                temp1.append(assignment)
                print(temp1)
                i["Completed"]=temp1
    print(data)
    with open(filename,"w") as f:
        json.dump(data,f)
    return jsonify({}),200
"""
@app.route('/upload')
def upload_file_home():
   return render_template('test.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method =='POST':
        f = request.files['file']
        if f:
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            t=plagiarism_check()
            if(t==0):
              return 'File uploaded successfully'
            else:
              path=os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
              os.remove(path)
              return 'Plagiarism detected. Please re-upload.'
        else:
        	return 'error while uploading. Please re-upload'  


"""


if __name__ == '__main__':
   app.run(debug = True)
