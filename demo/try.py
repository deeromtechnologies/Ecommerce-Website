from flask import Flask,render_template,url_for,redirect

app = Flask(__name__)


@app.route('/')

@app.route('/shoes.html')
def shoes():
	return render_template('shoes.html')

@app.route('/profile.html')
def home():
	return render_template('profile.html')

@app.route('/signup.html')
def signup():
	return render_template('signup.html')

@app.route('/login.html')
def login():
	return render_template('login.html')

@app.route('/contact.html')
def contact():
	return render_template('contact.html')

@app.route('/about.html')
def about():
	return render_template('about.html')

