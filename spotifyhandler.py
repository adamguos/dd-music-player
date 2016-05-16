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
		loop = spotify.EventLoop(self.session)
		loop.start()
		self.session.on(spotify.SessionEvent.CONNECTION_STATE_UPDATED, connection_state_listener)

		from secrets import username
		from secrets import password
		self.session.login(username, password)

		logged_in_event.wait()

		print('Logged in as', username)

	''' Set up Config object for initialising the pyspotify session '''
	def configsession(self):
		config = spotify.Config()
		# Insert configuration here
		return config
