from common import Common
import time

class Editor():
	def __init__(self):
		pass

	def html(self, json_conf, xml_file):

		lib = Common()

		xml_list = []	
		for item in json_conf:
			for xml_item in json_conf[item]:
				xml_list.append(xml_item)

		xml_doc = {}

		try:
			with open(xml_file) as f:
				for line in f:
					for xml_tag in xml_list:

						if xml_tag in line:
							if lib.get_tag_value(line) != "":
								xml_doc[xml_tag] = lib.get_tag_value(line)
						elif "<config " in line:
							xml_doc['version'] = lib.get_tag_attr(line,'version')
		except Exception:
			pass

		new_version = xml_doc['version'][:-6]+time.strftime('%y%m%d')

		conf_tab = '''
		<hr>
		<b>Config File Version </b>: %s<br>
		<dl>
		''' %(xml_doc['version'])

		for item in json_conf:
			conf_tab = conf_tab + "<dt><b>"+item+"</b>"
			for tab_item in json_conf[item]:
				if tab_item in xml_doc:
					conf_tab = conf_tab + "<dd>%s : <input type=text value='%s' size=%s name='%s'>"%(
						json_conf[item][tab_item]['caption'],
						xml_doc[tab_item],
						json_conf[item][tab_item]['size'],
						tab_item)

		conf_tab = conf_tab + "</dl>"

		ret = '''
			<html>
				<head>
					<link rel="stylesheet" type="text/css" href="/static/style.css">	
				</head>
				<body>
					<a href="/upload">Upload a file</a><br>
					<form method=POST action="savefile">
					%s
					<input type=submit value="Save As ...""><input type=text value='config_%s.xml' name='file_name'>
					</form>
					
				</body>
			<html>
		''' %(conf_tab, new_version)

		return ret
		