from dbhandler import DbHandler
from player import Player
from spotifyhandler import SpotifyHandler
import sys
import os
import vlc

class Browser:
	'Class for traversing the browser structure and controlling local media playback'

	def __init__(self):
		self.dbh = DbHandler()
		self.dbh.initmetadata()
		self.player = Player()
		self.sh = SpotifyHandler()
		self.rootnode = self.initbrowsernodes()
		self.curnode = self.rootnode
		self.mostrecentplayer = ''

	def initbrowsernodes(self):
		root = BrowserNode('root', self.dbh, self.sh)

		localmedia = BrowserNode('Local media', self.dbh, self.sh)
		spotify = BrowserNode('Spotify', self.dbh, self.sh, 'spotify playlists')
		restart = BrowserNode('Restart', self.dbh, self.sh, 'restart')

		albumartists = BrowserNode('Album artists', self.dbh, self.sh, 'tags', 'albumartist')
		artists = BrowserNode('Artists', self.dbh, self.sh, 'tags', 'artist')
		composers = BrowserNode('Composers', self.dbh, self.sh, 'tags', 'composer')
		genres = BrowserNode('Genres', self.dbh, self.sh, 'tags', 'genre')

		localmedia.addchild(albumartists)
		localmedia.addchild(artists)
		localmedia.addchild(composers)
		localmedia.addchild(genres)

		root.addchild(localmedia)
		root.addchild(spotify)
		root.addchild(restart)

		return root

	def curlist(self):
		children = []
		for child in self.curnode.getchildren():
			children.append(str(child))
		return children

	def select(self, index):
		selection = self.curnode.getchild(index)
		if selection.querytarget == 'play local':
			self.mostrecentplayer = 'local'
			self.sh.stop()
			filenames = []
			for child in self.curnode.getchildren():
				filenames.append(child.querysearch)
			self.player.play(filenames, index)
		elif selection.querytarget == 'play spotify':
			self.mostrecentplayer = 'spotify'
			self.player.stop()
			self.sh.selecttrack(selection.querysearch)
			self.sh.play()
		elif selection.querytarget == 'restart':
			self.restart_program()
		else:
			self.curnode = self.curnode.getchild(index)
		return self.curlist()

	def back(self):
		parent = self.curnode.getparent()
		if parent:
			self.curnode = parent
		return self.curlist()

	def togglepause(self):
		if self.mostrecentplayer == 'local':
			self.player.pause()
		elif self.mostrecentplayer == 'spotify':
			self.sh.togglepause()

	def next(self):
		if self.mostrecentplayer == 'local':
			self.player.next()
		elif self.mostrecentplayer == 'spotify':
			self.sh.next()

	def prev(self):
		if self.mostrecentplayer == 'local':
			self.player.prev()
		elif self.mostrecentplayer == 'spotify':
			self.sh.prev()

	def restart_program(self):
		python = sys.executable
		os.execl(python, python, *sys.argv)

class BrowserNode:
	'Class representing each selectable item in the browser'

	# label: the text that will be displayed
	# dbh: reference to DbHandler instance
	# querytarget: if passed, determines what data will be retrieved from the database to populate children; possible values are 'tags', 'albums', 'tracks', 'play local', 'spotify playlists'
	# querysearch: the search term or dict to be used to search for elements to populate children
	def __init__(self, label, dbh, sh, querytarget = '', querysearch = ''):
		self.label = label
		self.dbh = dbh
		self.sh = sh
		self.querytarget = querytarget
		self.querysearch = querysearch
		self.children = []
		self.parent = None

	def __str__(self):
		return self.label

	def getchildren(self):
		if self.querytarget == 'tags':
			self.children = []
			for item in self.dbh.querytags(self.querysearch):
				self.addchild(BrowserNode(item, self.dbh, self.sh, 'albums', {self.querysearch: item}))
		elif self.querytarget == 'albums':
			self.children = []
			for item in self.dbh.queryalbums(self.querysearch):
				self.addchild(BrowserNode(item, self.dbh, self.sh, 'tracks', dict(self.querysearch, **{'album': item})))
		elif self.querytarget == 'tracks':
			self.children = []
			for item in self.dbh.querytracks(self.querysearch):
				self.addchild(BrowserNode(item[0], self.dbh, self.sh, 'play local', item[1]))
		elif self.querytarget == 'spotify playlists':
			self.children = []
			playlists = self.sh.getplaylistnames()
			for index in range(len(playlists)):
				self.addchild(BrowserNode(playlists[index], self.dbh, self.sh, 'spotify tracks', index))
		elif self.querytarget == 'spotify tracks':
			self.children = []
			self.sh.selectplaylist(self.querysearch)
			tracks = self.sh.gettracknames()
			for index in range(len(tracks)):
				self.addchild(BrowserNode(tracks[index], self.dbh, self.sh, 'play spotify', index))

		return self.children

	def getchild(self, index):
		return self.children[index]

	def addchild(self, child):
		if not child in self.children:
			child.setparent(self)
			self.children.append(child)

	def removechild(self, child):
		del self.children[self.children.index(child)]

	def getparent(self):
		return self.parent

	def setparent(self, parent):
		self.parent = parent

b = Browser()
