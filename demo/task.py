from flask import Flask,render_template,request,url_for,session,redirect
from flask_sqlalchemy import SQLAlchemy
import bpdb
app = Flask("__name__")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/shoes.db'
db = SQLAlchemy(app)

app.secret_key="4=saudiuagsduig"

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


@app.route('/views')
def views():
	result1=tbl_signup.query.all()
	return render_template('view.html',result=result1 )

@app.route('/data/<uid>')
def data(uid):
	result1=tbl_signup.query.filter_by(uid=uid).first()
	return render_template('data.html',result=result1 )


@app.route('/shoes')
def shoes():
	return render_template('shoes.html')


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


@app.route('/signup',methods=["POST","GET"])
def signup():
	if request.method =="POST":
		bpdb.set_trace()
		signup=tbl_signup(uid=request.form['uid'],username=request.form['username'],email_id=request.form['email_id'],dob=request.form['dob'],password=request.form['password'])
		db.session.add(signup)
		db.session.commit()
		return redirect(url_for('views'))
	else:
		return render_template('signup.html')

@app.route('/blogs')
def blogs():
	return render_template('/blog.html')

@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('login'))


if __name__ == '__main__':
	db.create_all()
	app.run(debug = True)