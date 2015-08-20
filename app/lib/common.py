import os
class Common():
	def __init__(self):
		pass

	def get_tag_value(self, complete_tag):
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

	def get_tag_attr(self, complete_tag, attr):
		rec_val = complete_tag.strip()
		ret_val = rec_val[rec_val.find(attr):]
		ret_val = ret_val[ret_val.find('"')+1:]
		ret_val = ret_val[:ret_val.find('"')]

		return ret_val

	def make_tree(self, path):
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