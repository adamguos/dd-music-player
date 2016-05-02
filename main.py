from dbhandler import DbHandler

class Main:
	'Main class for executing program functions'

	def __init__(self):
		self.dbh = DbHandler()
		self.dbh.initmetadata()

	def close(self):
		self.dbh.close()
