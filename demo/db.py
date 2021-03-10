from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask("__name__")
	
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/.db'
db = SQLAlchemy(app)


class tbl_signup(db.Model):
username = db.Column(db.String(80), primary_key=True)
email_id = db.Column(db.String(120), unique=True, nullable=False)
dob = db.Column(db.String(50), unique=False, nullable=False)
password = db.Column(db.String(80), unique=False, nullable=False)
def __init__(self,username,email_id,dob,password):
	self.username=username
	self.email_id=email_id
	self.dob=dob
	self.password=password

@app route(/users)
def users():
	result=db.tbl_signup.query.all()
	bpdb.set_trace()
	return render_template('users.html',result)

@app.route('/shoes')
def shoes():
	return render_template('shoes.html')

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method =="POST":
		username=request.form["username"]
		password=request.form["password"]
		session["username"]=username
		session["password"]=password
		return redirect(url_for('shoes',username=username,password=password))
	
	else:
		return render_template("login.html")

@app.route('/signup',methods=['GET','POST'])
def signup():
	if request.method =="POST":
		
	
	else:
		return render_template("signup.html")

def __repr__(self):
return '<Name of user %r>' % self.name

class Login(db.Model):
login_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
username = db.Column(db.String(80),db.ForeignKey('username'), nullable=False)
password = db.Column(db.String(80), unique=False, nullable=False)

def __repr__(self):
return '<User %r>' % self.username

class Blog(db.Model):

blog_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
username = db.Column(db.String(80), db.ForeignKey('username'), nullable=False)
img = db.Column(db.String(100), unique=False, nullable=False)
des = db.Column(db.String(1000), unique=False, nullable=False)
date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

def __repr__(self):
return '<User %r>' % self.username
