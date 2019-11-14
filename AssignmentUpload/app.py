from flask import Flask, render_template, Markup, request, redirect,jsonify,abort
import requests
import os
from werkzeug import secure_filename
from flask_cors import CORS
#from form import myForm
from flask_static_compress import FlaskStaticCompress
#from currenttime import yourtime, prettytime
import logging
from flask_pymongo import PyMongo
import pymongo
import json


app = Flask(__name__)
CORS(app)

app.config["UPLOAD_FOLDER"]="/Users/shirishasrao/Desktop/WT/database"

@app.route('/upload')
def upload_file_home():
   return render_template('drag.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method =='POST':
        f = request.files['file']
        if f:
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return 'file uploaded successfully'
        else:
        	return 'error while uploading. Please reupload'    

if __name__ == '__main__':
   app.run(debug = True)
