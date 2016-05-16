from filehandler import FileHandler
from pymongo import MongoClient

class DbHandler:
	'Class for interfacing with MongoDB'

	def __init__(self):
		self.client = MongoClient()
		self.db = self.client.musicplayer
		self.coll = self.db.tracks

	''' Go through the database records upon boot and ensure that they match the contents of the music files in storage '''
	def initmetadata(self):
		tracks = FileHandler.getallfiles()

		numCreated = 0
		numUpdated = 0
		numRemoved = 0

		for filename in tracks:
			record = self.getrec(filename)

			# If the record retrieved doesn't exist, then create it
			if not record:
				self.createrec(filename)
				print('Created:', filename)
				numCreated += 1
			# If the file has been updated since the record was created, then update the record
			elif not FileHandler.getupdate(filename) == record['update']:
				self.reprec(filename)
				print('Updated:', filename)
				numUpdated += 1

		records = self.coll.find()

		for record in records:

			if not FileHandler.checkexists(record['filename']):
				# If the filename on an existing record doesn't exist, delete the record
				self.delrec(record['filename'])
				print('Deleted:', record['filename'])
				numRemoved += 1

		print('Number of records created:', numCreated)
		print('Number of records updated:', numUpdated)
		print('Number of records removed:', numRemoved)

	''' Return the record specified by the filename '''
	def getrec(self, filename):
		cursor = self.coll.find({'filename': filename})
		if cursor.count() > 1:
			raise RuntimeError('More than one record with the same filename was found')

		# Attempt to return the first item found by the cursor; if it doesn't exist, return None
		try:
			return cursor.next()
		except StopIteration:
			return None

	''' Return all records '''
	def getallrecs(self):
		cursor = self.coll.find()
		return list(cursor)

	''' Return list of all filenames stored '''
	def getallfilenames(self):
		cursor = self.coll.find()
		names = []
		for document in cursor:
			names.append(document['filename'])
		return names

	''' Return the number of records in the database '''
	def numofrecs(self):
		cursor = self.coll.find()
		return cursor.count()

	''' Delete the record(s) specified by the filename '''
	def delrec(self, filename):
		self.coll.delete_many({'filename': filename})

	''' Delete all records '''
	def dropcoll(self):
		self.coll.delete_many({})

	''' Update the record specified by the filename with the file's current metadata, retrieved from storage '''
	def reprec(self, filename):
		self.coll.replace_one(
			{'filename': filename},
			FileHandler.getmetadata(filename)
		)

	''' Create a new record with metadata retrieved from storage '''
	def createrec(self, filename):
		self.coll.insert_one(FileHandler.getmetadata(filename))

dbh = DbHandler()
