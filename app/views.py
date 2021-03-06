import os
from flask import render_template, request , redirect, url_for
from app import app
from werkzeug import secure_filename

from lib import Common

import time
import json


from flask import Markup
from functools import wraps

UPLOAD_FOLDER = '/opt/configtool/uploads'
CONFIG_FOLDER = '/opt/configtool/config'
BUILDS_FOLDER = '/opt/configtool/app/static/builds'

ALLOWED_EXTENSIONS = set(['xml'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
lib = Common()

def check_auth(username, password):
	logins = dict()

	try:
		with open(CONFIG_FOLDER+'/logins.json') as json_logins:
			logins = json.load(json_logins)
			json_logins.close()
	except Exception, e:
		return False
	
	if username in logins:
		return logins[username] == password
	return False	
	

def authenticate():
	return ('Bad Login! you are not allowed to use this system!',
	 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if not auth or not check_auth(auth.username, auth.password):
			return authenticate()
		return f(*args, **kwargs)
	return decorated

@app.route('/')
@app.route('/index')
@requires_auth
def index():
	return render_template('upload.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
@requires_auth
def upload_file():
	
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'temp1.xml'))
			_conf_host = ""
			if "HTTP_X_CONF_HOST" in request.environ:
				_conf_host = request.environ["HTTP_X_CONF_HOST"]
			
			return redirect(_conf_host+url_for('editor',filename=filename))
			

	return render_template('upload.html')



@app.route('/editor')
@requires_auth
def editor():
	with open(CONFIG_FOLDER+'/config.json') as conf:
		json_conf = json.load(conf)
		xml_list = []	

		for item in json_conf:
			for xml_item in lib.find_xml_tag(json_conf[item]):
				xml_list.append(xml_item)

		xml_doc = {}
		xml_file = os.path.join(app.config['UPLOAD_FOLDER'],'temp1.xml')
		try:
			with open(xml_file) as f:
				for line in f:
					for xml_tag in xml_list:
						if "<"+xml_tag+">" in line:
							xml_doc[xml_tag] = lib.get_tag_value(line)
						elif "<config " in line:
							xml_doc['version'] = lib.get_tag_attr(line,'version')
		except Exception:
			pass
		
		new_version = xml_doc['version'][:-6]+time.strftime('%y%m%d')
		conf_tab2 = [xml_doc['version'],[]]
		json_conf_sorted = sorted(json_conf.items())
		
		for item in json_conf_sorted:
			tab_dic_title = {item[0]:[]}
			
			for tab_item in lib.find_tab_items(item[1], xml_doc):
				tab_dic_title[item[0]].append(tab_item)

			conf_tab2[1].append(tab_dic_title)

		return render_template('editor.html', new_version=new_version, conf_tab= conf_tab2)


@app.route('/savefile', methods=['GET', 'POST'])	
@requires_auth
def savefile():
	if request.method == 'POST':
		f = open(os.path.join(BUILDS_FOLDER,request.form['file_name']), 'w')
		with open(os.path.join(app.config['UPLOAD_FOLDER'],'temp1.xml')) as f_source:
			empty_tags = []
			line_number = 0

			for line in f_source:
				line_number +=1
				if "<config " in line:
					line = '<config version="%s">' %(request.form['new_version'])
				else:
					if lib.is_empty_tag(line):
						empty_tags.append('%s: %s'%(line_number,line))

				for xml_tag in request.form:
					if "<"+xml_tag+">" in line:
						line = lib.update_xml_value(line,request.form[xml_tag])
					
				f.write(line)
		f.close()
	return render_template('savefile.html',
		new_version = request.form['new_version'], file_name = request.form['file_name'], empty_tags=empty_tags)

@app.route('/builds')
@requires_auth
def builds():
	path = os.path.expanduser(BUILDS_FOLDER)
	return render_template('builds.html', tree=lib.make_tree(path))

@app.context_processor
def sub_options():
	
	def find_sub_options(items):	

		return Markup(lib.make_ret_html_for_editor(items))

	return dict(find_sub_options=find_sub_options)

@app.route('/ping')
def ping():
	ret = "pong..."
	return ret
	
@app.route('/logout')
def logout():
	return render_template('logout.html'), 401

'''
Shows this page if invalid address is entered!
'''
@app.errorhandler(404)
@requires_auth
def page_not_found(e):
	return render_template('upload.html'), 404