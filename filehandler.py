from mutagen.mp3 import MP3

class FileHandler:
	'Class for interfacing with media files and metadata tags; used from DbHandler for disk IO'

	# Check if the specified filepath exists
	@staticmethod
	def checkexists(filepath):
		return os.path.isfile(filepath)

	# Check if the specified filepath was updated at the same time as the given update time; i.e. whether or not the file has been updated since the record was updated
	@staticmethod
	def checkupdate(filepath, update):
		return os.path.getmtime(filepath) == update

	# Get all metadata in the form of a tuple from a specified file
	@staticmethod
	def getMetadata(filepath):
		track = MP3(filepath)
		trackinfo = track.info
		return ()
