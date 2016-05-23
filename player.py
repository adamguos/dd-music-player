from filehandler import FileHandler
import vlc

class Player:
	'Class for controlling local media playback'

	def __init__(self):
		self.media_dir = FileHandler.mediadir
		self.vlc_instance = vlc.Instance()
		self.vlc_player = self.vlc_instance.media_player_new()

	def set_media(self, filename):
		vlc_media = self.vlc_instance.media_new(self.media_dir + filename)
		self.vlc_player.set_media(vlc_media)

	def play(self):
		self.vlc_player.play()

	def toggle_pause(self):
		self.vlc_player.pause()

p = Player()
