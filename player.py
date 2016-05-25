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
		if len(args) == 2:
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
			print(1)
			self.cur_track += 1
			print(2)
			self.set_media()
			print(3)
			self.play()
			print(4)
		except IndexError:
			print('Index error')
			self.cur_track -= 1
			pass

	def prev(self):
		print('prev')
		try:
			print(1)
			self.cur_track -= 1
			print(2)
			self.set_media()
			print(3)
			self.play()
			print(4)
		except IndexError:
			print('Index error')
			self.cur_track += 1
			pass
