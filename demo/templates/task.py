from flask import Flask,render_template,request,url_for,session,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask("__name__")

app.secret_key="4322"

@app.route('/')

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
		

@app.route("/logout")
def logout():
	session.pop("username",None)
	return redirect(url_for("login"))


@app.route('/signup',methods=['GET','POST'])
def signup():
	if request.method =="POST":
		username=request.form["username"]
		email_id=request.form["email_id"]
		dob=request.form["dob"]
		password=request.form[""]
		
		session["birthday"]=birthday
		session["password"]=password
		session["fullname"]=fullname
		session["email_id"]=email_id
		return redirect(url_for('shoes',username=username,dob=dob,password=password,email_id=email_id))
	
	else:
		return render_template("signup.html")


@app.route("/signout")
def signout():
	session.pop("fullname",None)
	return redirect(url_for("shoes"))


@app.route('/blog')
def blog():
	return render_template('blog.html')

if __name__ == '__main__':
	app.run(debug=True)