from socketserver import BaseRequestHandler
from socketserver import TCPServer

import json
from svncount import counter

class MyHandler(BaseRequestHandler):
	def handle(self):
		indata=self.request.recv(1024*5)
		outdata=self.deal(indata)
		self.request.sendall(outdata)


	def deal(self,indata):
		instr=indata.decode()
		outstr='unknow command'

		try:
			cmd,arg=self.parseInput(instr)
		except Exception:
			print('error input: '+instr)
			raise
		if 'count'==cmd:
			outstr=self.cmd_count(arg)
		return outstr.encode()


	def parseInput(self,instr):
		tmp=instr.split(';;',1)
		cmd,argstr=tmp[0],tmp[1]

		arg=dict()
		for _pair in argstr.split(';'):
			tmp2=_pair.split(':',1)
			_key=tmp2[0]
			if len(tmp2)==1:
				_value=None
			else:
				_value=tmp2[1]
			arg[_key]=_value
		return cmd,arg


	def cmd_count(self,arg):
		url,start,end=arg.get('url'),arg.get('start'),arg.get('end')
		if (url is None) or (start is None) or (end is None):
			print('input error:')
			print('arg: '+arg)
			return 'nozuonodie'

		sc=counter(url,start,end)

		name,psd=arg.get('username'),arg.get('password')
		if (name is not None) and (psd is not None):
			sc.setauthority(name,psd)
		return json.dumps(sc.countNow())


def runserver(config=None):
	if config is None:
		config={'host':'','port':200}
	serv=TCPServer((config['host'],config['port']),MyHandler)
	print('listening port: '+str(config['port']))
	print('server name   : svncount')
	print('server type   : tcp')
	serv.serve_forever()


if __name__=='__main__':
	runserver()
	