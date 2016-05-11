from mutagen.easyid3 import EasyID3
from mutagen.easymp4 import EasyMP4
from mutagen.flac import FLAC
import os

class FileHandler:
	'Class for interfacing with media files and metadata tags; used from DbHandler for disk IO'

	mediadir = 'Music/'

	''' Check if the specified filename exists '''
	@classmethod
	def checkexists(cls, filename):
		return os.path.isfile(cls.mediadir + filename)

	''' Get the time at which the specified file was last updated '''
	@classmethod
	def getupdate(cls, filename):
		return os.path.getmtime(cls.mediadir + filename)

	''' Get all metadata in the form of a dict from a specified file '''
	@classmethod
	def getmetadata(cls, filename):
		codec = cls.getcodec(filename)
		tagsdict = None

		# Each codec requires a different module and different processing; at the end of this construct, no matter what the codec is, a dictionary with tag names as keys and tag values as values is created
		if codec == 'mp3':
			tagsdict = dict(cls.parse_mp3(filename), **{'filename': filename, 'update': cls.getupdate(filename)})
		elif codec == 'flac':
			tagsdict = dict(cls.parse_flac(filename), **{'filename': filename, 'update': cls.getupdate(filename)})
		elif codec == 'm4a':
			tagsdict = dict(cls.parse_m4a(filename), **{'filename': filename, 'update': cls.getupdate(filename)})

		# Guaranteed attributes of tagsdict: date, title, tracknumber (no total), genre, album, albumartist, artist, discnumber (no total), filename (excluding media directory, including extension)
		return tagsdict

	''' Determine what file format (and therefore codec, in this simplified case) the file is in '''
	@classmethod
	def getcodec(cls, filename):
		ext = filename.split('.')[-1]
		if not cls.checkexists(filename):
			raise FileNotFoundError(filename)
		if not ext == 'mp3' and not ext == 'm4a' and not ext == 'flac':
			raise NotImplementedError(filename)

		return ext.lower()

	''' Open an MP3 file and create a dict storing its metadata in a standard form used across the module '''
	@classmethod
	def parse_mp3(cls, filename):
		# Create an EasyID3 object representing MP3 file; metadata is stored in key-value pairs, easily convertible to a regular dict
		audio = EasyID3(cls.mediadir + filename)
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
	@classmethod
	def parse_flac(cls, filename):
		# FLAC() creates a FLAC object that can be conveniently converted into a dictionary
		audio = FLAC(cls.mediadir + filename)
		d = dict(audio)

		# All values in the dict are further stored inside lists; this removes that unnecessary layer
		for key in d:
			d[key] = d[key][0]

		return d

	''' Open an M4A file and create a dict storing its metadata in a standard form used across the module '''
	@classmethod
	def parse_m4a(cls, filename):
		# EasyMP4() creates an EasyMP4 object that can be conveniently converted into a dictionary
		audio = EasyMP4(cls.mediadir + filename)
		d = dict(audio)

		# All values in the dict are further stored inside lists; this removes that unnecessary layer
		for key in d:
			d[key] = d[key][0]

		# Removes total from disc and track number values
		d['tracknumber'] = d['tracknumber'].split('/')[0]
		d['discnumber'] = d['discnumber'].split('/')[0]

		return d

	''' Recursively go through the directory structure within mediadir, and return a list of all music (.mp3, .m4a, .flac) files found '''
	@classmethod
	def getallfiles(cls):
		matches = []

		# Recursively goes through every file inside the given directory and its subdirectories, which may incur a heavy performance penalty and will have to be used moderately or changed
		# Each loop enters a new subdirectory
		for root, dirnames, filenames in os.walk(cls.mediadir):
			# root is the path leading up to the current directory, including mediadir; since mediadir is automatically added by all other methods in the class, this needs to be removed
			root = root.replace(cls.mediadir, '', 1)
			if len(root) > 0: root += '/'

			# For every file in the current directory, attempt to check the codec then append the filename to the matches list; getcodec will raise errors if necessary
			for filename in filenames:
				try:
					cls.getcodec(root + filename)
					matches.append(os.path.join(root, filename))
				# This should never occur
				except FileNotFoundError:
					print('get_allfiles found file that does not exist:', os.path.join(root, filename))
				# Non-music files may include cover art, etc. This is not a problem and is expected to occur
				except NotImplementedError:
					print('get_allfiles found non-music file:', os.path.join(root, filename))
					continue

		return matches
