from flask import Flask,render_template,request,url_for,session,redirect
from flask_sqlalchemy import SQLAlchemy
import bpdb
#from flask_login import LoginManager
#from models import db
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_mail import Message
from datetime import datetime,date
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms import Form, BooleanField, StringField, PasswordField,IntegerField,DateField,SubmitField, validators,ValidationError
from wtforms.validators import InputRequired,Email,Length
from flask_mail import Mail, Message
from flask_login import LoginManager,UserMixin,login_required, current_user



app = Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
db = SQLAlchemy(app)
Bootstrap(app)
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login' 

@login_manager.user_loader
def load_user(username):
	return tbl_signup.query.filter_by(username=username).first()

mail= Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'abcd@gmail.com'
app.config['MAIL_PASSWORD'] = '********'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.secret_key="saudiuagsduig"


@app.route('/')
def shoes():
	return render_template('shoes.html')


class SignupForm(FlaskForm):
	uid=IntegerField('uid',validators=[DataRequired()])
	username = StringField('username',validators=[DataRequired()])
	email_id = StringField('email_id',validators=[DataRequired(),validators.Length(min=6, max=35)])
	password = PasswordField('password',validators=[DataRequired()])
	dob=StringField('dob',validators=[DataRequired()])
	image = StringField('image',validators=[DataRequired()])
	title= StringField('title', validators=[DataRequired()])
	content= StringField('content', validators=[DataRequired()])
	date = DateField('date', validators=[DataRequired()])

class BlogUpdate(FlaskForm):
	blog_id=StringField('blog_id', validators=[DataRequired()])
	username = StringField('username', [validators.Length(min=4, max=27)])
	image = StringField('image',validators=[DataRequired()])
	title= StringField('title', validators=[DataRequired()])
	content= StringField('content', validators=[DataRequired()])
	date = DateField('date', validators=[DataRequired()])

class LoginForm(FlaskForm):
	username = StringField('username', [validators.Length(min=4, max=27)])
	password = PasswordField('password',validators=[DataRequired()])
	

class tbl_signup(UserMixin,db.Model):
	username = db.Column(db.String(80),primary_key=True )
	uid = db.Column(db.String(120),unique=False,nullable=False)
	email_id = db.Column(db.String(120), unique=False, nullable=False)
	dob = db.Column(db.Integer, unique=False, nullable=False)
	password = db.Column(db.String(80), unique=False, nullable=False)
	def __init__(self,uid,username,email_id,dob,password):
		self.uid=uid
		self.username=username
		self.email_id=email_id
		self.dob=dob
		self.password=password


class tbl_blog(db.Model):
	blog_id= db.Column(db.String(120), primary_key=True)
	username=db.Column(db.String(120), db.ForeignKey('tbl_signup'))
	title = db.Column(db.String(220), unique=False, nullable=False)
	content = db.Column(db.String(80), unique=False, nullable=False)
	image = db.Column(db.String(220), unique=False, nullable=False)
	date = db.Column(db.DateTime, nullable=False)
	def __init__(self,blog_id,username,title,content,image,date):
			self.blog_id=blog_id
			self.username=username
			self.title=title
			self.content=content
			self.image=image
			self.date=date	


@app.route('/view')
def view():
	result1=tbl_signup.query.all()
	#bpdb.set_trace()
	return render_template('view.html',result=result1 )


@app.route('/data/<username>')
def data(username):
	result1=tbl_signup.query.filter_by(username=username).first()
	return render_template('data.html',result=result1 )

@app.route('/blog_display/<username>')
def blog_display(username):
	result1=tbl_blog.query.filter_by(username=username).first()
	bpdb.set_trace()
	return render_template('blog_display.html',user=result1 ) 


 

@app.route('/login',methods=["GET","POST"])
def login():
	bpdb.set_trace()
	form=SignupForm()
	if request.method =='POST' and form.validate_on_submit():
		bpdb.set_trace()
		username=form.username.data
		password=form.password.data
		session["username"]=username
		user=tbl_signup.query.filter_by(username=username).first()
		if not user or not(user.password==password):
			return "check login credentials"
			return redirect(url_for('profile'),username=username)
	return render_template('login.html',form=form)

@app.route('/profile')
@login_required
def profile():
	return render_template('profile.html', name=current_user.name, mail=current_user.email)


@app.route('/signup', methods=["POST","GET"])
def signup():
	form = SignupForm(request.form)
	if request.method == 'POST' and form.validate_on_submit():
		signup = tbl_signup(uid=form.uid.data,username=form.username.data,email_id=form.email_id.data,dob=form.dob.data,password=form.password.data)
		db.session.add(signup)
		db.session.commit()
		msg = Message('Hello', sender = 'abc94@gmail.com',recipients = [form.email_id.data])
		msg.body = "Thanks for registering"
		mail.send(msg)
		return redirect(url_for('view'))
	else:
		return render_template('signup.html',form=form)



@app.route('/add_blog/<username>',methods=["GET","POST"])
def add_blog(username):
	form = SignupForm(request.form)
	if request.method == 'POST':
		bpdb.set_trace()
		blog = tbl_blog(date=form.date.data,username=form.username.data,title=form.title.data,image=form.image.data, content=form.content.data)
		db.session.add(blog)
		db.session.commit()
		username1=request.form['username']
		return redirect(url_for('blog_display',username=username1))
	result1=tbl_signup.query.filter_by(username=username).first()
	return render_template('add_blog.html',result=result1,form=form) 



@app.route('/update/<username>',methods = ["GET","POST"])
def update(username):
	form=BlogUpdate(request.form)
	blogup=tbl_blog.query.filter_by(username=username).first()
	if request.method == "POST":
		bpdb.set_trace()
		if blogup:
			db.session.delete(blogup)
			db.session.commit()
			blogup = tbl_blog(blog_id=form.blog_id.data,username=form.username.data,title= form.title.data,image=form.image.data, content=form.content.data,date=form.date.data)
			db.session.add(blogup)
			db.session.commit()
			username=form.username.data
			return "You have successfully updated the blog"
		return f"blog with username = {username} does not exist"
	result1=tbl_blog.query.filter_by(username=username).first()
	return render_template('update.html',result=result1,form=form)

@app.route('/delete/<uid>', methods=['GET','POST'])
def delete(uid):
	delperson= tbl_signup.query.filter_by(uid=uid).first()
	if request.method == 'POST':
		if delperson:
			db.session.delete(delperson)
			db.session.commit()
			return render_template("view.html")
		return render_template("404.html")

	return render_template('delete.html')


@app.route('/blog',methods=["POST","GET"])
def blog():
    form = BlogUpdate(request.form)
    if request.method =="POST":
        obj= tbl_blog(username=form.username.data,date=form.date.data,title=form.title.data,content=form.content.data,image=form.image.data)
        db.session.add(obj)
        db.session.commit()
        #result=blog.query.all()
        return redirect(url_for('blog_display'))
    else:
        return render_template('/blog1.html',form=form) 

@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('login'))


if __name__ == '__main__':
	db.create_all()
	app.run(debug = True)


