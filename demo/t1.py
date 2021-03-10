from flask import render_template,Flask,request,url_for,session,redirect

app=Flask("__name__")

app.secret_key="f3er7677r7q3r5"


@app.route('/shoes/')
def shoes():
	return render_template("shoes.html")

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method =="POST":

		username=request.form['username']
		password=request.form['password']
		session["username"]=username
		session["password"]=password
		return redirect(url_for('login',username=username,password=password))
	else:

		if "username" in session:
			return redirect(url_for('profile'))

		return render_template("login.html")

@app.route("/logout")
def logout():
	session.pop("username",None)
	return redirect(url_for("login"))