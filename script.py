from flask import Flask,render_template,request,session
import sqlite3
import os
import shutil
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename


app = Flask(__name__ ,template_folder='/FrontEnd/Html',static_folder='/FrontEnd')
app.secret_key = "y337kGcys"

@app.route('/')
def home():
	return render_template("ecell.html")
@app.route('/sponser')
def sponser():
	return render_template("sponser.html")

if __name__=="__main__":
	app.run(debug=True)