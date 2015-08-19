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
