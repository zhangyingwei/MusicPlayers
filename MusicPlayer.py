from IMusicPlayer import IMusicPlayer
from wangyi import WyMusicPlayer

class MusicPlayer(IMusicPlayer):
    def play(self, random=False, url=None):
        return super().play(random, url)

    def search(self, name=None, type=None):
        return super().search(name, type)