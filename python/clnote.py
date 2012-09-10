import os
import sys
import json
import ConfigParser
import urllib,urllib2

class CLNote:

	ENDC = '\033[0m'

	@classmethod		
	def main(cls, args):
		cfg = ConfigParser.ConfigParser()
		cfg.read(os.path.dirname(__file__) + '/clnote.cfg')

		login = cfg.get('CLNOTE', 'LOGIN')
		password = cfg.get('CLNOTE', 'PASSWORD')
		url = cfg.get('CLNOTE', 'URL')
		
		CLNote.COLOR_DATE = '\033[9' + cfg.get('COLOR', 'DATE') + 'm'
		#CLNote.GREEN = '\033[9' + cfg.get('COLOR', 'GREEN') + 'm'
		CLNote.COLOR_ID = '\033[9' + cfg.get('COLOR', 'ID') + 'm'
		CLNote.COLOR_TEXT = '\033[9' + cfg.get('COLOR', 'TEXT') + 'm'
		CLNote.COLOR_LABELS = '\033[9' + cfg.get('COLOR', 'LABELS') + 'm'
		CLNote.COLOR_ERRORS = '\033[9' + cfg.get('COLOR', 'ERRORS') + 'm'

		args = args[1:]
		note = CLNote(login, password, url, args)
		note.process()

	def __init__(self, login, password, url, args):
		if len(args) < 1:
			args = ['list']
		self.login = login
		self.password = password
		self.url = url
		self.args = args

	def process(self):
		command = self.args[0]
		if(command == 'add'):
			if len(self.args) < 2:
				raise Exception("Incorrect paramter count")
			self.doAddCommand()
		elif(command == 'list'):
			self.doListCommand()
		else:
			raise Exception("Unknown command");


	def doAddCommand(self):
		message = self.args[1]
		labels = '' if len(self.args) <= 2 else self.args[2]
		url = "%s/api/add" % self.url
		params = {
			'note': message,
			'labels': labels
		}
		self.executeRequest(url, params)

	def doListCommand(self):
		url = "%s/api/list" % self.url
		labels = self.args[1] if len(self.args) > 1 else ''
		data = self.executeRequest(url, {'labels': labels})
		for item in data['rows']:
			print "%s%s%s %s%s%s %s%s%s" % (CLNote.COLOR_ID, item['note_id'], CLNote.ENDC, 
				CLNote.COLOR_DATE, item['creation_date'] + " " + "-" * 40, CLNote.ENDC,
				CLNote.COLOR_LABELS, item['label'], CLNote.ENDC)
			print "%s%s%s" % (CLNote.COLOR_TEXT, item['note'], CLNote.ENDC)


	def executeRequest(self, url, params):
		params['login'] = self.login
		params['password'] = self.password
		params = urllib.urlencode(params)
		res = urllib2.urlopen(url, params)
		ret = json.load(res)
		if not ret['success']:
			self.printError(ret)
			exit()
		return ret

	def printError(self, res):
		print "%sError: %s%s" % (CLNote.COLOR_ERRORS, res['error']['message'], CLNote.ENDC)

CLNote.main(sys.argv)
