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
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'temp1.xml'))
			return redirect(url_for('editor',filename=filename))

	return render_template('upload.html')


@app.route('/editor')
def editor():
	filedata = {}
	jsondata = None



	try:
		with open(os.path.join(app.config['UPLOAD_FOLDER'],'temp1.xml')) as f:
			for line in f:
				if "<ems_url>" in line:
					filedata["ems_url"] = get_tag_value(line)
				elif "<counter_report_url>" in line:
					filedata["sup_url"] = get_tag_value(line)
				elif "<config " in line:
					filedata["conf_ver"] = get_tag_attr(line,'version')
	except Exception:
		filedata["ems_url"] = None
		filedata["sup_url"] = None
		filedata["conf_ver"] = None
				
		
		#iledata = f.readlines()


	
	return render_template('editor.html',
	 ems_url=filedata["ems_url"],
	  sup_url=filedata["sup_url"],
	  conf_ver=filedata["conf_ver"])

def get_tag_value(complete_tag):
	rec_val = complete_tag.strip()
	do_copy = True
	ret_val = ""
	for ch in rec_val:
		if ch == "<":
			do_copy = False
		elif ch == ">":
			do_copy = True
		elif do_copy:
			ret_val = ret_val + ch

	return ret_val

def get_tag_attr(complete_tag, attr):
	rec_val = complete_tag.strip()
	ret_val = rec_val[rec_val.find(attr):]
	ret_val = ret_val[ret_val.find('"')+1:]
	ret_val = ret_val[:ret_val.find('"')]

	return ret_val