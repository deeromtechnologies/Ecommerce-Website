from flask import Flask,redirect,url_for,render_template
app = Flask(__name__)

@app.route('/')
def home():
	return "<h1>Hello World<h1>"

@app.route('/<name>')
def user(name):
	return f"<h1>Hello {name}!!<h1>"

@app.route('/admin')
def admin():
	return redirect(url_for("user", name="Admin!"))

@app.route('/index')
def index():
	return render_template('index.html')

if __name__ == '__main__':
	render.run()