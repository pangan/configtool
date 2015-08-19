import os
from flask import render_template, request , redirect, url_for
from app import app
from werkzeug import secure_filename

from dynamic import Editor

import json

UPLOAD_FOLDER = '/opt/configtool/uploads'
CONFIG_FOLDER = '/opt/configtool/app/static'
BUILDS_FOLDER = '/opt/configtool/app/builds'
ALLOWED_EXTENSIONS = set(['xml'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
@app.route('/index')
def index():
	#return "Hello, Flask!"
	pass_param= {'var1':'A'}
	return render_template('upload.html',
							title='Home',
							param=pass_param)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'temp1.xml'))
			return redirect(url_for('editor',filename=filename))

	return render_template('upload.html')


@app.route('/editor')
def editor():
	filedata = {}
	ret_html = Editor()
	jsondata = ""
	with open(CONFIG_FOLDER+'/config.json') as conf:
		conf_js = json.load(conf)
		
		return ret_html.html(conf_js, os.path.join(app.config['UPLOAD_FOLDER'],'temp1.xml'))


@app.route('/savefile', methods=['GET', 'POST'])	
def savefile():

	if request.method == 'POST':
		return render_template('listfiles.html')
		return request.form['file_name']
	else:
		return "nothing!"