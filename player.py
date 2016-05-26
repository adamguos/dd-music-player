from filehandler import FileHandler
import vlc

class Player:
	'Class for controlling local media playback'

	def __init__(self):
		self.media_dir = FileHandler.mediadir
		self.playlist = []
		self.cur_track = 0
		self.vlc_instance = vlc.Instance()
		self.vlc_player = self.vlc_instance.media_player_new()
		self.vlc_event_manager = self.vlc_player.event_manager()
		self.vlc_event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, self.song_finished, 1)

	def set_playlist(self, playlist, cur_track):
		self.playlist = playlist
		self.cur_track = cur_track
		self.set_media()

	def set_media(self):
		print(11)
		vlc_media = self.vlc_instance.media_new_path(self.media_dir + self.playlist[self.cur_track])
		print(12)
		self.vlc_player.set_media(vlc_media)
		print(13)

	def play(self, *args):
		cur_playing = ''
		try:
			cur_playing = self.playlist[self.cur_track]
		except IndexError:
			cur_playing = ''

		to_be_played = cur_playing
		if len(args) == 2:
			to_be_played = args[0][args[1]]

		if not cur_playing == to_be_played:
			self.set_playlist(args[0], args[1])
		self.vlc_player.play()

	def stop(self):
		self.vlc_player.stop()

	def pause(self):
		self.vlc_player.pause()

	def song_finished(self, *args):
		self.next()

	def next(self):
		print('next')
		try:
			self.cur_track += 1
			self.set_media()
			self.play()
		except IndexError:
			print('Index error')
			self.cur_track -= 1
			pass

	def prev(self):
		print('prev')
		try:
			self.cur_track -= 1
			self.set_media()
			self.play()
		except IndexError:
			print('Index error')
			self.cur_track += 1
			pass

	def get_state(self):
		return self.vlc_player.get_state()
