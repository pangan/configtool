from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
	#return "Hello, Flask!"
	pass_param= {'var1':'A'}
	return render_template('index.html',
							title='Home',
							param=pass_param)
