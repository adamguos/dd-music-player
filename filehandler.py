from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.m4a import M4A

class FileHandler:
	'Class for interfacing with media files and metadata tags; used from DbHandler for disk IO'

	mediadir = 'Music/'

	''' Check if the specified filepath exists '''
	@staticmethod
	def checkexists(filepath):
		return os.path.isfile(mediadir + filepath)

	''' Check if the specified filepath was updated at the same time as the given update time; i.e. whether or not the file has been updated since the record was updated '''
	@staticmethod
	def checkupdate(filepath, update):
		return os.path.getmtime(filepath) == update

	''' Get all metadata in the form of a tuple from a specified file '''
	@staticmethod
	def getmetadata(filepath):
		codec = getcodec(filepath)
		tagsdict = None

		# Each codec requires a different module and different processing; at the end of this construct, no matter what the codec is, a dictionary with tag names as keys and tag values as values is created
		if codec == 'mp3':
			tagsdict = parse_mp3(filepath)
		elif codec == 'flac':
			tagsdict = parse_flac(filepath)
		elif codec == 'm4a':
			tagsdict = parse_m4a(filepath)


		track = MP3(filepath)
		trackinfo = track.info
		return ()

	''' Determine what file format (and therefore codec, in this simplified case) the file is in '''
	@staticmethod
	def getcodec(filepath):
		ext = filepath.split('.')[1]
		return ext.lower()

	''' Open an MP3 file and create a dict storing its metadata in a standard form used across the module '''
	@staticmethod
	def parse_mp3(filepath):
		# Create an EasyID3 object representing MP3 file; metadata is stored in key-value pairs, easily convertible to a regular dict
		audio = EasyID3(mediadir + filepath)
		d = dict(audio)

		# All values in the dict are further stored inside lists; this removes that unnecessary extra layer
		for key in d:
			d[key] = d[key][0]

		# Renames 'performer' to 'albumartist'
		d['albumartist'] = d['performer']
		del d['performer']

		# Removes total from disc and track number values
		d['tracknumber'] = d['tracknumber'].split('/')[0]
		d['discnumber'] = d['discnumber'].split('/')[0]

		return d

	''' Open a FLAC file and create a dict storing its metadata in a standard form used across the module '''
	@staticmethod
	def parse_flac(filename):
		# FLAC() creates a FLAC object that can be conveniently converted into a dictionary
		audio = FLAC(mediadir + filepath)
		d = dict(audio)

		# All values in the dict are further stored inside lists; this removes that unnecessary layer
		for key in d:
			d[key] = d[key][0]

		return d

	''' Open an M4A file and create a dict storing its metadata in a standard form used across the module '''
	@staticmethod
	def parse_m4a(filename):
		
