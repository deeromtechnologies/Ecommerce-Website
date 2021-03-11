from flask import Flask,render_template,request,url_for,session,redirect
from flask_sqlalchemy import SQLAlchemy
import bpdb
from flask_mail import Mail
from flask_mail import Message
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms import Form, BooleanField, StringField, PasswordField,IntegerField,DateField,SubmitField, validators,ValidationError
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
db = SQLAlchemy(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'gopikasathish94@gmail.com'
app.config['MAIL_PASSWORD'] = 'Arjun_2407'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

"""@app.route('/')
def index():
	msg = Message("Hello",sender='gopikasathish94@gmail.com',recipients=['gopika@deerom.com'])
	msg.body="Thank you for registering with us"
	mail.send(msg)
	return "Sent"""

app.secret_key="saudiuagsduig"

@app.route('/shoes')
def shoes():
	return render_template('shoes.html')


class SignupForm(FlaskForm):
	uid=IntegerField('uid',validators=[DataRequired()])
	username = StringField('username',validators=[DataRequired()])
	email_id = StringField('email_id',validators=[DataRequired(),validators.Length(min=6, max=35)])
	#dob=DateField('dob',validators=[DataRequired()])
	password = PasswordField('password',validators=[DataRequired()])
	dob=StringField('dob',validators=[DataRequired()])

class tbl_signup(db.Model):


	uid = db.Column(db.String(120),primary_key=True)
	username = db.Column(db.String(80), unique=False,nullable=False)
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
	username= db.Column(db.String(120), primary_key=True)
	uid=db.Column(db.String(120), db.ForeignKey('tbl_signup'))
	title = db.Column(db.String(220), unique=False, nullable=False)
	content = db.Column(db.String(80), unique=False, nullable=False)
	image = db.Column(db.String(220), unique=False, nullable=False)
	date = db.Column(db.DateTime, nullable=False)
	def __init__(self,username,uid,title,content,image,date):
			self.username=username
			self.uid=uid
			self.title=title
			self.content=content
			self.image=image
			self.date=date	


@app.route('/views')
def views():
	result1=tbl_signup.query.all()
	#bpdb.set_trace()
	return render_template('view.html',result=result1 )


@app.route('/data/<uid>')
def data(uid):
	result1=tbl_signup.query.filter_by(uid=uid).first()
	return render_template('data.html',result=result1 )

@app.route('/blog_display')
def blog_display():
    result1=tbl_blog.query.all()
    #bpdb.set_trace()
    return render_template('blog_display.html',result=result1 ) 

 

@app.route('/login',methods=["GET","POST"])
def login():
	if request.method =="POST":
		username=request.form["username"]
		session["username"]=username
		password=request.form["password"]
		session["password"]=password
		return redirect(url_for("shoes"))
	else:
		return render_template('login.html')



@app.route('/signup', methods=["POST","GET"])
def signup():
	form = SignupForm(request.form)
	if request.method == 'POST' and form.validate_on_submit():
		signup = tbl_signup(uid=form.uid.data,username=form.username.data,email_id=form.email_id.data,dob=form.dob.data,password=form.password.data)
		db.session.add(signup)
		db.session.commit()
		msg = Message('Hello', sender = 'gopikasathish94@gmail.com',recipients = [form.email_id.data])
		msg.body = "Thanks for registering"
		mail.send(msg)
		return redirect(url_for('views'))
	else:
		return render_template('signup.html',form=form)

@app.route('/details/<username>')
def details(username):
	detail= tbl_signup.query.filter_by(username=username).first()
	return render_template('details.html',result=detail)



@app.route('/add_blog/<uid>',methods=["GET","POST"])
def add_blog(uid):
    #bpdb.set_trace()
    
    if request.method == 'POST':
        blog = tbl_blog(uid=request.form['uid'],date=request.form['date'],username=request.form['username'],title= request.form['title'],image=request.form['image'], content=request.form['content'])
        db.session.add(blog)
        db.session.commit()
        uid1=request.form['uid']
        return redirect(url_for('/blog_display',uid=uid1))
    result1=tbl_signup.query.filter_by(uid=uid).first()   
    return render_template('add_blog.html',result=result1) 


@app.route('/data/<int:uid>/update',methods = ['GET','POST'])
def update(uid):
	bpdb.set_trace()
	user=tbl_signup.query.filter_by(uid=uid).first()
	if request == "POST":
		if user:
			db.session.delete(user)
			db.session.commit()
			username=request.form['username']
			password=request.form['password']
			email_id=request.form['email_id']
			dob=request.form['dob']
			user=tbl_signup(username=username,password=password,email_id=email_id,dob=dob)
			db.session.add(user)
			db.session.commit()
			return redirect('views')
	return render_template('update.html', user = user)


@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('login'))


if __name__ == '__main__':
	db.create_all()
	app.run(debug = True)


