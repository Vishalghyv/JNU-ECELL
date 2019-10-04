from flask import Flask,render_template,request,session
app = Flask(__name__ ,template_folder='../frontend/html',static_folder='../frontend')
