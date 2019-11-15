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
#from sklearn.feature_extraction.text import TfidfVectorizer
import glob



app = Flask(__name__)
CORS(app)

#app.config["UPLOAD_FOLDER"]="/Users/shirishasrao/Desktop/AssignmentUpload/database"
app.config["MONGO_URI"]= "mongodb+srv://shivangijadon16:pikachu4321@cluster0-wu1c9.mongodb.net/test?retryWrites=true&w=majority"
mongo = pymongo.MongoClient("mongodb+srv://shivangijadon16:pikachu4321@cluster0-wu1c9.mongodb.net/test?retryWrites=true&w=majority")

"""def plagiarism_check():
	file_list=glob.glob("/Users/shirishasrao/Desktop/AssignmentUpload/database/*.txt")
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
"""
db = pymongo.database.Database(mongo, 'user_cred')
usercol = db["user_col"]

@app.route('/api/v1/login',methods=['POST'])
def login():
    username =  request.form['username']
    password = request.form['password']
    current_user=usercol.find_one({"username":username})
    print(current_user)
    """if(not(current_user)):
        return "username does not exist!",400
    
    if(current_user):
        if(current_user['password']==password):
            session['user_id']= str(current_user['_id'])
            session['username'] = current_user['username']
            print(str(session['user_id']))
            print("done")
            print(current_user["name"])
            return jsonify({"userData" : session['username'],"Name":current_user["name"]}),200
        else:
            return "password incorrect!",400"""
    return username,200
    
@app.route('/api/v1/get/assignment/completed/<username>',methods=["GET"])
def get_completed_assignment(username):
    current_user=usercol.find_one({"username":username})
    print(current_user["Completed"])
    return jsonify({"Completed":current_user["Completed"]})

@app.route('/api/v1/get/assignment/pending/<username>',methods=["GET"])
def get_pending_assignment(username):
    current_user=usercol.find_one({"username":username})
    print(current_user["Pending"])
    return jsonify({"Pending":current_user["Pending"]})

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

if __name__ == '__main__':
   app.run(debug = True)
