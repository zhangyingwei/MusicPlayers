from wangyi.ModleCollection import Song


class IMusicPlayer:
    def play(self, random=False,songs:list=None,name:str = None):
        raise Exception("必须实现播放方法")
    def play(self, random=False,song:Song=None):
        raise Exception("必须实现播放方法")
    def startPlay(self,random=False):
        raise Exception("必须实现播放方法")
    def search(self,name=None,type=None):
        raise Exception("必须实现搜索方法")