from flask import Flask,render_template,request,url_for,session,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask("__name__")
	
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/shoes.db'
db = SQLAlchemy(app)


class tbl_signup(db.Model):
	

@app.route('/db')
def db():
	result=db.tbl_signup.query.all()
	bpdb.set_trace()
	return render_template('db.html',result)

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
		bpdb.set_trace()
		signup=tbl_signup(username=request.form['username'],email_id=request.form['email_id'],dob=request.form['dob'],password=request.form['password'])
		db.session.add(signup)
		db.session.commit()
		return redirect(url_for('db.html'))

	else:
		return render_template("login.html")

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
