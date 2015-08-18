import os
from flask import render_template, request , redirect, url_for
from app import app
from werkzeug import secure_filename

UPLOAD_FOLDER = '/opt/configtool/uploads'
ALLOWED_EXTENSIONS = set(['xml'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
@app.route('/index')
def index():
	#return "Hello, Flask!"
	pass_param= {'var1':'A'}
	return render_template('index.html',
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
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('editor',filename=filename))

	return render_template('upload.html')


@app.route('/editor')
def editor():
	filedata = []
	with open(os.path.join(app.config['UPLOAD_FOLDER'],'config.xml')) as f:
		filedata = f.readlines()

	
	return render_template('editor.html', confile=filedata)