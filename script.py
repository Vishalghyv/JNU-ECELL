from flask import Flask,render_template,request,session
from flask import Flask, request, redirect, url_for


app = Flask(__name__ ,template_folder='./frontend/html',static_folder='./frontend')
app.secret_key = "y337kGcys"

@app.route('/')
def home():
	print("Hello")
	return render_template("ecell.html")
@app.route('/sponser')
def sponser():
	return render_template("sponser.html")

if __name__=="__main__":
	app.run()