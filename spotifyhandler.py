import spotify
import threading

class SpotifyHandler:
	'Class for interfacing with pyspotify (and libspotify)'

	def __init__(self):
		print('Start logging in')

		logged_in_event = threading.Event()

		def connection_state_listener(session):
			if session.connection.state is spotify.ConnectionState.LOGGED_IN:
				logged_in_event.set()

		self.session = spotify.Session(self.configsession())
		self.audio = spotify.AlsaSink(self.session)
		loop = spotify.EventLoop(self.session)
		loop.start()
		self.session.on(spotify.SessionEvent.CONNECTION_STATE_UPDATED, connection_state_listener)

		from secrets import username
		from secrets import password
		self.session.login(username, password)

		# Blocks the thread until the log in operation completes
		logged_in_event.wait()

		print('Logged in as', username)

		def endtrack(session, errortype):
			if errortype is spotify.ErrorType.OK:


		# Set up listeners for when the currently playing track finishes
		self.session.on(spotify.SessionEvent.END_OF_TRACK, endtrack)

	''' Set up Config object for initialising the pyspotify session '''
	def configsession(self):
		config = spotify.Config()
		# Insert configuration here
		return config

	''' Get list of playlist names saved by user '''
	def getplaylistnames(self):
		names = []

		for i in range(len(self.session.playlist_container)):
			playlist = self.session.playlist_container[i]
			# The following blocking operation, performed at every iteration, can potentially cause dramatic slowdowns
			playlist.load()
			names.append(playlist.name)

		return names

	''' Get list of track names in the currently selected playlist '''
	def gettracknames(self):
		names = []

		for i in range(len(self.playlist.tracks)):
			track = self.playlist.tracks[i]
			# The following blocking operation, performed at every iteration, can potentially cause dramatic slowdowns
			track.load()
			names.append(track.name)

		return names

	''' Get name of currently selected track '''
	def getseltrackname(self):
		return self.track.name

	''' Select a certain playlist (by index according to the list passed by getplaylistnames()) by assigning to an instance variable '''
	def selectplaylist(self, index):
		self.playlist = self.session.playlist_container[index]
		self.playlist.load()

	''' Select a certain track (by index according to the list returned by gettracknames()) in the currently selected playlist by assigning to an instance variable '''
	def selecttrack(self, index):
		self.track = self.playlist.tracks[index]
		self.track.load()

	''' Play the currently selected track through ALSAAudio '''
	def play(self):
		player = self.session.player

		if player.state == 'playing' or player.state == 'paused':
			if self.track == self.curplaytrack:
				player.play()
				return
		else:
			player.load(self.track)
			player.play()
			self.curplaytrack = self.track

	''' Pause the currently playing track '''
	def pause(self):
		player = self.session.player

		if player.state == 'playing':
			player.pause()

	''' Stop the currently playing track '''
	def stop(self):
		player = self.session.player

		if player.state == 'playing' or player.state == 'paused':
			player.unload()

sh = SpotifyHandler()
