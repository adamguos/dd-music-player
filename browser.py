from dbhandler import DbHandler

class Browser:
	'Class for traversing the browser structure and controlling local media playback'

	def __init__(self):
		self.dbh = DbHandler()
		self.dbh.initmetadata()
		self.rootnode = self.initbrowsernodes()
		self.curnode = self.rootnode

	def initbrowsernodes(self):
		main = BrowserNode('main', self.dbh)

		localmedia = BrowserNode('Local media', self.dbh)
		spotify = BrowserNode('Spotify', self.dbh)
		restart = BrowserNode('Restart', self.dbh)

		albumartists = BrowserNode('Album artists', self.dbh, 'tags', 'albumartist')
		artists = BrowserNode('Artists', self.dbh, 'tags', 'artist')
		composers = BrowserNode('Composers', self.dbh, 'tags', 'composer')
		genres = BrowserNode('Genres', self.dbh, 'tags', 'genre')

		localmedia.addchild(albumartists)
		localmedia.addchild(artists)
		localmedia.addchild(composers)
		localmedia.addchild(genres)

		main.addchild(localmedia)
		main.addchild(spotify)
		main.addchild(restart)

		return main

	def curlist(self):
		children = []
		for child in self.curnode.getchildren():
			children.append(str(child))
		return children

	def select(self, index):
		self.curnode = self.curnode.getchild(index)
		return self.curlist()

	def back(self):
		self.curnode = self.curnode.getparent()
		return self.curlist()

class BrowserNode:
	'Class representing each selectable item in the browser'

	# label: the text that will be displayed
	# dbh: reference to DbHandler instance
	# querytarget: if passed, determines what data will be retrieved from the database to populate children; possible values are 'tags', 'albums', and 'tracks'
	# querysearch: the search term or dict to be used to search for elements to populate children
	def __init__(self, label, dbh, querytarget = '', querysearch = ''):
		self.label = label
		self.dbh = dbh
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
				self.addchild(BrowserNode(item, self.dbh, 'albums', {self.querysearch: item}))
		elif self.querytarget == 'albums':
			self.children = []
			for item in self.dbh.queryalbums(self.querysearch):
				self.addchild(BrowserNode(item, self.dbh, 'tracks', dict(self.querysearch, **{'album': item})))
		elif self.querytarget == 'tracks':
			self.children = []
			for item in self.dbh.querytracks(self.querysearch):
				self.addchild(BrowserNode(item[0], self.dbh))

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
