from filehandler import FileHandler
from pymongo import MongoClient

class DbHandler:
	'Class for interfacing with MongoDB'

	def __init__(self):
		self.client = MongoClient()
		self.db = self.client.musicplayer
		self.coll = self.db.tracks

	def initmetadata(self):
		tracks = coll.find()

		for track in tracks:
			if not FileHandler.checkexists(track.filepath):
				# If the filepath on an existing record doesn't exist, delete the record
				self.delRecord(track.filepath)
			elif not FileHandler.checkupdate(track.filepath, track.update):
				# If the filepath on an existing record exists, but the file itself has been modified, update the record with the new metadata
				self.replaceRecord(track.filepath, )


	def delRecord(self, filepath):
		self.coll.delete_many({"filepath": filepath})
