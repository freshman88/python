import os
import pysvn
from tool import linecount,diffcount

class counter():
	"""
	hello~
	can't help now :(

	but you can read code,it's easy :)

	require: pysvn
	"""
	def __init__(self,url,revision_start_num,revision_end_num,
		tmp_path='c://tmp/svncount'):

		self.client=pysvn.Client()

		if not url.endswith('/'):
			url+='/'
		self.url=url

		self.revision_start=self._getRevision(revision_start_num)
		self.revision_end=self._getRevision(revision_end_num)

		self.tmp_path=tmp_path
		if not os.path.exists(tmp_path):
			os.makedirs(tmp_path)

		self.allow_file_type=['.html','.xhtml','.jsp','.php','.asp','.css'
		,'.js','.java','.py','.c','.h','.cpp','.txt','.csv','.xml','.json']
		self.ignore_file_name=[]
		self.ignore_file_path=[]


	def _getRevision(self,number):
		return pysvn.Revision(pysvn.opt_revision_kind.number,number)


	def findRevisions(self):
		log_mess=self.client.log(self.url,
			revision_start=self.revision_start,
			revision_end=self.revision_end)

		prev_revision=self.revision_start
		#log_mess is sorted by revision asc
		for mess in log_mess:
			revision=mess.get('revision')
			if prev_revision.number != revision.number:
				#(prev_revision,revision,author)
				revision_step=(prev_revision,revision,mess.get('author'))
				yield revision_step
			prev_revision=revision


	def findFiles(self,revision_step):
		summs=self.client.diff_summarize(self.url,
			revision1=revision_step[0],revision2=revision_step[1])
		
		for summ in summs:
			#(kind,path) eg:('added','/WebContent/a2l/js/a2l.js')
			info=(str(summ.get('summarize_kind')),summ.get('path'))
			if self.filter_file(info):
				yield info


	def filter_file(self,info):
		fullpath=self._fullpath()
		filename=os.path.basename(info[1])
		suffix=os.path.splitext(filename)[1]
		return self._ignore_file_path_filter(fullpath)\
		   and self._ignore_file_name_filter(filename)\
		   and self._allow_file_type_filter(suffix)


	def _allow_file_type_filter(self,suffix):
		return suffix in self.allow_file_type


	def _ignore_file_name_filter(self,filename):
		return filename not in self.ignore_file_name


	def _ignore_file_path_filter(self,fullpath):
		return fullpath not in self.ignore_file_path


	def _fullpath(self,info=None,rel_path=None):
		if info is not None:
			return self.url+info[1]
		elif rel_path is not None:
			if rel_path.startswith('/'):
				rel_path=rel_path[1:]
			return self.url+rel_path
		else:
			return self.url


	def countLine(self,info,revision_step):
		addNum,delNum,msg=0,0,None
		try:
			#kind:added, delete, modified
			kind=info[0]
			fullpath=self._fullpath(info)
			if 'added'==kind:
				binstr=self.client.cat(fullpath,revision_step[1])
				addNum=linecount(binstr).count()
			elif 'delete'==kind:
				binstr=self.client.cat(fullpath,revision_step[0])
				delNum=linecount(binstr).count()
			else:
				diff_text=self.client.diff(self.tmp_path,fullpath,
					revision1=revision_step[0],revision2=revision_step[1])
				addNum,delNum=diffcount(diff_text).count()
		except Exception as e:
			addNum,delNum,msg=0,0,str(e)
		return addNum,delNum,msg


	def _format_data(self):
		i=0
		while i < len(self.ignore_file_path):
			ignore_path=self.ignore_file_path[i]
			if not ignore_path.startswith('svn://'):
				self.ignore_file_path[i]=self._fullpath(rel_path=ignore_path)
			i+=1


	def countNow(self):
		self._format_data()

		result_list=list()
		for revsion_step in self.findRevisions():
			changed_list=list()
			for info in self.findFiles(revsion_step):
				changed=dict()
				changed['path']=self._fullpath(info)
				changed['addNum'],changed['delNum'],changed['msg']=\
						self.countLine(info,revsion_step)
				changed_list.append(changed)
			result=dict()
			result['start']  =revsion_step[0].number
			result['end']    =revsion_step[1].number
			result['author'] =revsion_step[2]
			result['changed']=changed_list
			result_list.append(result)
		return result_list


	def setauthority(self,name,psd):
		def login_method(realm,username,may_save):
			return True,name,psd,False

		self.client.callback_get_login =login_method


if __name__=='__main__':
	url=""
	revision_start_num=84634
	revision_end_num=86096
	sc=counter(url,revision_start_num,revision_end_num)
	rs=sc.countNow()
	# print(rs)
	import json
	print(json.dumps(rs))