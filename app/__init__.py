from PIL import Image
from flask import Flask,render_template,request,session
from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, url_for, flash, redirect, request, Blueprint
# User Based Imports
from flask_login import current_user
from datetime import datetime
from flask_login import UserMixin
from wtforms import StringField, SubmitField, TextAreaField,BooleanField




app = Flask(__name__ ,template_folder='../frontend/html',static_folder='../frontend')
app.config['SECRET_KEY'] = 'mysecret'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app,db)


login_manager = LoginManager()

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "admin"
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    # This connects BlogPosts to a User Author.

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register!')

    def validate_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def validate_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')

class BlogPostForm(FlaskForm):
    # no empty titles or text possible
    # we'll grab the date automatically from the Model later
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    event = BooleanField('Event')
    submit = SubmitField('BlogPost')
def add_profile_pic(pic_upload,postname):

    filename = pic_upload.filename
    # Grab extension type .jpg or .png
    ext_type = filename.split('.')[-1]
    storage_filename = str(postname) + '.' +ext_type
    
    filepath = os.path.abspath(os.path.join(app._static_folder, 'resources/', storage_filename))

    # Play Around with this size.
    output_size = (1000, 1000)

    # Open the picture and save it
    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename

import json

#########################
#	Reading from json	#
#########################
with open('../articles/articles.json') as f:
	data = json.load(f)
posts=data["posts"]
headings=data["headings"]
@app.route('/')
def home():
	return render_template("ecell.html")
@app.route('/sponser')
def sponser():
	return render_template("sponser.html")
@app.route('/article/<num>')
def article(num):
	if num.isnumeric():
		if(int(num)<=3):
			articles=posts["post"+num]
			return render_template("article.html",articles=articles,headings=headings,num=num)
	return render_template("ecell.html")
@app.route('/registerEvent/<num>')
def event(num):
	if num.isnumeric():
		if(int(num)<=3):
			articles=posts["post"+num]
			if(articles["register"]):
					return render_template("event.html",articles=articles,num=num)
	return render_template("ecell.html")
@app.route('/listingArticle')
def listingArticle():
	return render_template("listing.html",posts=posts,variable=1)
@app.route('/listingEvent')
def listingEvent():
	return render_template("listing.html",posts=posts,variable=0)
@app.route('/admin')
def admin():
	return render_template("admin.html")
@app.route('/adminLogin', methods=['GET', 'POST'])
def adminLogin():
	form = LoginForm()
	if form.validate_on_submit():
	    # Grab the user from our User Models table
	    user = User.query.filter_by(email=form.email.data).first()

	    # Check that the user was supplied and the password is right
	    # The verify_password method comes from the User object
	    # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

	    if user.check_password(form.password.data) and user is not None:
	        #Log in the user

	        login_user(user)

	        # If a user was trying to visit a page that requires a login
	        # flask saves that URL as 'next'.
	        next = request.args.get('next')

	        # So let's now check if that next exists, otherwise we'll go to
	        # the welcome page.
	        if next == None or not next[0]=='/':
	            next = url_for('adminPosts')
	        return redirect(next)
	return render_template('login.html', form=form)
@app.route('/adminPosts')
@login_required
def adminPosts():
    with open('../articles/articles.json') as f:
        data = json.load(f)
    posts=data["posts"]
    headings=data["headings"]
    return render_template('adminPosts.html',posts=posts)

@app.route('/adminRegister', methods=['GET', 'POST'])
def adminRegister():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('adminLogin'))
    return render_template('register.html', form=form)

@app.route("/adminLogout")
@login_required
def adminLogout():
    logout_user()
    return redirect(url_for('admin'))
@app.route("/adminEdit/<num>/<name>")
@login_required
def adminEdit(num,name):
	post=posts[name]
	return render_template("articleEdit.html",post=post,name=name)
@app.route("/adminUpdate/<name>", methods=['GET', 'POST'])
@login_required
def adminUpdate(name):
    blog_post = posts[name]
    if blog_post["user_name"] != current_user.username:
        abort(403)

    form = BlogPostForm()
    if form.validate_on_submit():
        if form.picture.data:
            pic = add_profile_pic(form.picture.data,name)
            posts["post"+str(len(posts)-1)]["img"]="resources/"+pic
        posts[name]["heading"] = form.title.data
        posts[name]["article"]= form.text.data
        if(form.event.data ==True):
            posts[name]["register"]= 1
        else:
            posts[name]["register"]= 0
        if form.picture.data:
            pic = add_profile_pic(form.picture.data,"post"+str(len(posts)))
            posts["post"+str(len(posts))]["img"]="resources/"+pic
        with open('../articles/articles.json', 'w') as f:
            json.dump(data, f)
        return redirect(url_for('adminPosts'))
    elif request.method == 'GET':
        form.title.data = posts[name]["heading"]
        form.text.data = posts[name]["article"]
        form.event.data = posts[name]["register"]
    return render_template('create_post.html', title='Update Article',
                           form=form)
@app.route('/adminCreate',methods=['GET','POST'])
@login_required
def adminCreate():
    form = BlogPostForm()
    if form.validate_on_submit():
        posts["post"+str(len(posts)+1)]={}
        posts["post"+str(len(posts))]["heading"]=form.title.data
        posts["post"+str(len(posts))]["num"]=len(posts)
        headings["heading"+str(len(headings)+1)]=form.title.data
        posts["post"+str(len(posts))]["article"]=form.text.data
        posts["post"+str(len(posts))]["user_name"]=current_user.username
        if(form.event.data ==True):
            posts["post"+str(len(posts))]["register"]= 1
        else:
            posts["post"+str(len(posts))]["register"]= 0
        if form.picture.data:
            pic = add_profile_pic(form.picture.data,"post"+str(len(posts)))
            posts["post"+str(len(posts))]["img"]="resources/"+pic
        with open('../articles/articles.json', 'w') as f:
            json.dump(data, f)
        return redirect(url_for('adminPosts'))
    return render_template('create_post.html',form=form)
@app.route("/adminDelete/<name>", methods=['POST'])
@login_required
def adminDelete(name):
    blog_post = posts[name]
    if blog_post["user_name"] != current_user.username:
        abort(403)
    del posts[name]
    with open('../articles/articles.json', 'w') as f:
            json.dump(data, f)
    return redirect(url_for('adminPosts'))
@app.route('/<path:path>')
def catch_all(path):
    return render_template("ecell.html")
if __name__ == "__main__":
	app.run(debug=True)