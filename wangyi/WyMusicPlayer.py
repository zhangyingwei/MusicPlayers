import os
import uuid
from datetime import time

from requests import Response
from IMusicPlayer import IMusicPlayer
import requests
import pygame
from bs4 import BeautifulSoup
from wangyi.ModleCollection import PlayCollect
from wangyi.ModleCollection import Song

class WyMusicPlayer(IMusicPlayer):
    def __init__(self):
        self.login_form=""
        self.base_url = "https://music.163.com"
        self.player_utl = "http://music.163.com/song/media/outer/url?"
        self.http_header:dict = {
            "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-language":"zh-CN,zh;q=0.9",
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
        }

    def list_playlist(self,type:str="host"):
        """
        获取歌单
        type: new  hot
        :return:
        """
        list_url:str = "https://music.163.com/discover/playlist/"
        param:dict = {"order":type}
        result:Response = requests.get(url=list_url,params=param,headers=self.http_header)
        soup:BeautifulSoup = BeautifulSoup(result.text,"html5lib")
        container = soup.find(id="m-pl-container")

        resultList:list = list()
        for li in container.find_all("li"):
            info_a = li.find("p",attrs={'class':'dec'}).find("a")
            title:str = info_a["title"]
            href:str = info_a["href"]
            resultList.append(PlayCollect(title=title,url=href))
        return resultList

    def open_playlist(self,collects:list=None,name:str = None):
        """
        打开播放列表
        获取所有歌曲链接
        :param collect:
        :return:
        """
        collect = self.find_collect(collects,name)
        print("open "+collect.title)
        url = self.base_url+collect.url
        print(url,"https://music.163.com/playlist?id=2796426115")
        page = requests.get(url,headers=self.http_header)
        soup:BeautifulSoup = BeautifulSoup(page.text,"html5lib")
        music_count:int = soup.find(id="playlist-track-count").text
        print(collect.title+" music count: "+ music_count)
        a_list = soup.find_all("a",attrs={'href':True,'class':False,'data-res-action':False })
        song_list:list = list()
        for a_tag in a_list:
            href = a_tag['href']
            title = a_tag.text
            if "song" in href:
                href = href.split("?")[1]
                song_list.append(Song(title=title,url=href))
        return song_list

    def open_hotlist(self):
        """
        获取热点音乐列表
        :return:
        """
        url = "https://music.163.com/#/discover/toplist"
        response:Response = requests.get(url,headers=self.http_header)
        soup = BeautifulSoup(response.text,"html5lib")
        print(soup)

    def startPlay(self,random=False):
        playlist = self.list_playlist()
        if random:
            playlist = self.random_one(playlist)
        for play in playlist:
            songlist = self.open_playlist(playlist,play.title)
            for song in songlist:
                self.play(song=song)

    def play(self, random=False,songs:list=None,name:str = None):
        song = self.find_song(songs,name)
        self.play(song=song)

    def play(self, random=False, song: Song= None):
        print("play: "+song.title)
        song_url = self.player_utl + song.url + ".mp3"
        tmp_song_url = self.download_song(song_url)
        pygame.mixer.init()
        track = pygame.mixer.music.load(tmp_song_url)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pass
        self.remove_tmp_song(tmp_song_url)

    def search(self, name=None, type=None):
        return super().search(name, type)

    def download_song(self, song_url):
        response:Response = requests.get(song_url)
        song_id = uuid.uuid4()
        self.create_tmp_dir("./tmp")
        song_path = "./tmp/"+str(song_id)+".mp3"
        with open(song_path,"wb") as song_file:
            song_file.write(response.content)
        return song_path

    def create_tmp_dir(self, name):
        if not os.path.exists(name):
            os.mkdir(name)

    def remove_tmp_song(self, tmp_song_url):
        # os.remove(tmp_song_url)
        for song in os.listdir("./tmp"):
            url = "./tmp/"+song
            try:
                os.remove(url)
            except Exception:
                print(url)

    def find_collect(self, collects, name):
        for collect in collects:
            if name == collect.title or name in collect.title:
                return collect

    def find_song(self, songs, name):
        for song in songs:
            if name == song.title or name in song.title:
                return song

if __name__ == '__main__':
    player = WyMusicPlayer()
    # play_list = player.list_playlist()
    # song_list = player.open_playlist(play_list,name="一人之下")
    # player.play(songs=song_list,name="八荒")
    # player.open_hotlist()
    player.startPlay()