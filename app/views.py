import os
from flask import render_template, request , redirect, url_for
from app import app
from werkzeug import secure_filename

from lib import Common

import time
import json

UPLOAD_FOLDER = '/opt/configtool/uploads'
CONFIG_FOLDER = '/opt/configtool/app/static'
BUILDS_FOLDER = '/opt/configtool/app/static/builds'

ALLOWED_EXTENSIONS = set(['xml'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
lib = Common()

@app.route('/')
@app.route('/index')
def index():
	return render_template('upload.html')


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
		
	with open(CONFIG_FOLDER+'/config.json') as conf:
		
		
		json_conf = json.load(conf)
		xml_list = []	
		
		for item in json_conf:
			for xml_item in json_conf[item]:
				xml_list.append(xml_item)
				if 'sub_options' in json_conf[item][xml_item]:
					for sub_item in json_conf[item][xml_item]['sub_options']:
						xml_list.append(sub_item)
		
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
			for tab_item in item[1]:
				

				sub_item_list = []
				if "sub_options" in item[1][tab_item]:
					
					for sub_item in item[1][tab_item]['sub_options']:
						sub_item_values = dict(title=item[1][tab_item]['sub_options'][sub_item]['caption'],
								 value = xml_doc[sub_item],
								 size = item[1][tab_item]['sub_options'][sub_item]['size'] ,
								 name = sub_item,
								 type = item[1][tab_item]['sub_options'][sub_item]['type'])

						sub_item_list.append(sub_item_values)
					
					
				xml_tag_value = ""
				if tab_item in xml_doc:
					xml_tag_value = xml_doc[tab_item]

				item_values = dict(title=item[1][tab_item]['caption'],
								 value = xml_tag_value,
								 size = item[1][tab_item]['size'] ,
								 name = tab_item,
								 type = item[1][tab_item]['type'],
								 sub_item = sub_item_list)

				tab_dic_title[item[0]].append(item_values)
				


			conf_tab2[1].append(tab_dic_title)

		return render_template('editor.html', new_version=new_version, conf_tab= conf_tab2)


@app.route('/savefile', methods=['GET', 'POST'])	
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
def builds():
	path = os.path.expanduser(BUILDS_FOLDER)
	return render_template('builds.html', tree=lib.make_tree(path))



