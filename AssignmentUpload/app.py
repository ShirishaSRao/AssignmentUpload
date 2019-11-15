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
app.config["MONGO_URI"]= "mongodb+srv://dbShirisha:myatlasdatabase@cluster0-pb58c.mongodb.net/test?retryWrites=true&w=majority"
mongo = pymongo.MongoClient('mongodb+srv://dbShirisha:myatlasdatabase@cluster0-pb58c.mongodb.net/test?retryWrites=true&w=majority')

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
db = pymongo.database.Database(mongo, 'user_credentials')
usercol = pymongo.collection.Collection(db, 'user_credentials')

@app.route('/api/v1/login',methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    print(type(username))
    for x in usercol.find({}):
        print(x)
    """print(username)
    print(password)
    
    print(x)
    if(not(x)):
        return "Username does not exists!",400
    if(x):
        if(x['password']==password):
            return "",201
        else:
            return "Password Incorrect!",400"""
    return jsonify({"name":"arya"}),200

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
