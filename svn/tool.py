
class linecount():
	def __init__(self,binstr):
		self.charset_list=['utf-8','shift-jis','MS932','ascii']
		self.content=self.decodestr(binstr)


	def decodestr(self,binstr):
		for charset in self.charset_list:
			result=self._decodestr(binstr,charset)
			if result is not None:
				return result
		return None


	def _decodestr(self,binstr,charset):
		try:
			return binstr.decode(charset)
		except UnicodeDecodeError:
			return None


	def count(self):
		if not self.content:
			msg='file can not decode by:'+','.join(self.charset_list)
			raise Exception(msg)
		return self.content.count('\n')+1



class diffcount():
	def __init__(self,diff_text):
		self.text=diff_text


	def count(self):
		addNum,delNum=0,0
		modified_list=self.text.split('\n')
		for modified_text in modified_list:
			if modified_text.startswith('+\t'):
				addNum+=1
			elif modified_text.startswith('-\t'):
				delNum+=1
		return addNum,delNum