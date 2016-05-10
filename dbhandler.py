from filehandler import FileHandler
from pymongo import MongoClient

class DbHandler:
	'Class for interfacing with MongoDB'

	def __init__(self):
		self.client = MongoClient()
		self.db = self.client.musicplayer
		self.coll = self.db.tracks

	def __str__(self):
		cursor = self.coll.find()
		return '\n'.join([str(i) for i in cursor])

	''' Go through the database records upon boot and ensure that they match the contents of the music files in storage '''
	def initmetadata(self):
		tracks = coll.find()

		for track in tracks:
			filename = track[filename]
			if not FileHandler.checkexists(filename):
				# If the filename on an existing record doesn't exist, delete the record
				self.delrecord(filename)
			elif not FileHandler.getupdate(filename) == track[update]:
				# If the filename on an existing record exists, but the file itself has been modified, update the record with the new metadata
				self.replacerecord(filename)

	''' Return the record specified by the filename '''
	def getrecord(self, filename):
		cursor = self.coll.find({'filename': filename})
		if cursor.count() > 1:
			raise RuntimeError('More than one record with the same filename was found')
		return cursor.next()

	''' Delete the record(s) specified by the filename '''
	def delrecord(self, filename):
		self.coll.delete_many({'filename': filename})

	''' Update the record specified by the filename with the file's current metadata, retrieved from storage '''
	def replacerecord(self, filename):
		self.coll.replace_one(
			{'filename': filename},
			FileHandler.getmetadata(filename)
		)

	''' Create a new record with metadata retrieved from storage '''
	def createrecord(self, filename):
		self.coll.insert_one(FileHandler.getmetadata(filename))
