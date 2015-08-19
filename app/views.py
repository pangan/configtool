import os
from flask import render_template, request , redirect, url_for
from app import app
from werkzeug import secure_filename

from dynamic import Editor

import json

UPLOAD_FOLDER = '/opt/configtool/uploads'
CONFIG_FOLDER = '/opt/configtool/app/static'
BUILDS_FOLDER = '/opt/configtool/app/static/builds'

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
		f = open(os.path.join(BUILDS_FOLDER,request.form['file_name']), 'w')
		with open(os.path.join(app.config['UPLOAD_FOLDER'],'temp1.xml')) as f_source:
			for line in f_source:
				f.write(line)
		f.close()
	

	path = os.path.expanduser(BUILDS_FOLDER)
	return render_template('listfiles.html', tree=make_tree(path))

def make_tree(path):
    tree = dict(name=os.path.basename(path), children=[])
    try: lst = os.listdir(path)
    except OSError:
        pass #ignore errors
    else:
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                tree['children'].append(dict(name=name))
    return tree