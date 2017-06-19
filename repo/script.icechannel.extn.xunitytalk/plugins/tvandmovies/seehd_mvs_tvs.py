

#iStream Extension
#SeeHD
#Copyright (C) 2017 mucky duck


from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
import xbmc

class seehd(MovieSource,TVShowSource):

    implements = [MovieSource,TVShowSource]

    name = 'SeeHD'
    display_name = 'SeeHD'
    base_url = 'http://www.seehd.ws'
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'

    source_enabled_by_default = 'true'




    def AddMedia(self, list, data):

        for final_url, res in data: 

            if '.srt' not in final_url:
                if '1080' in res:
                    res='1080P'                   
                elif '720' in res:
                    res='720P'
                elif  '480' in res:
                    res='DVD'
                elif '360' in res:
                    res='SD'
                else:
                    res='DVD'

                self.AddFileHost(list, res, final_url)




    def GetFileHosts(self, url, list, lock, message_queue, season, episode, type):

        from entertainment import requests
        from entertainment import jsunpack
        import urlresolver,re

        referer = url
        
        headers = {'User-Agent':self.User_Agent}
        sources = []

        link = requests.get(url, headers=headers, timeout=15).content

        try:
            RES = re.findall(r'Quality:</strong>([^<>]*)<', str(link), re.I|re.DOTALL)[0].upper()
        except:
            RES = ''

        if '4K' in RES:
            res='4K'
        elif '3D' in RES:
            res='3D'
        elif '1080' in RES:
            res='1080P'                   
        elif '720' in RES:
            res='720P'
        elif 'HD' in RES:
            res='HD'
        elif 'DVD' in RES:
            res='DVD'
        elif 'HDTS' in RES:
            res='TS'
        elif 'TS' in RES:
            res='TS'
        elif 'CAM' in RES:
            res='CAM'
        elif 'HDCAM' in RES:
            res='CAM'
        else:
            res='720P'

        try:
            url2 = re.findall(r'<source src="([^"]+)"', str(link), re.I|re.DOTALL)[0]
            sources.append(url2)
        except:pass

        try:
            iframe_url = re.findall(r'iframe.*?src="([^"]+)"', str(link), re.I|re.DOTALL)
            for url3 in iframe_url:
                if 'songs2dl' in url3:
                    headers = {'User-Agent':self.User_Agent, 'Referer':referer}
                    link2 = requests.get(url3, headers=headers, timeout=15).content
                    if jsunpack.detect(link2):
                        js_data = jsunpack.unpack(link2)
                        match = re.findall(r'"file":"([^"]+)".*?"label":"([^"]+)"', str(js_data), re.I|re.DOTALL)
                        self.AddMedia(list,match)
                
                else:
                    if urlresolver.HostedMediaFile(url3):
                        sources.append(url3)
        except:pass

        try:
            mirror_url = re.findall(r'href="([^"]+)" rel="nofollow">', str(link), re.I|re.DOTALL)
            for url4 in mirror_url:
                if urlresolver.HostedMediaFile(url4):
                    sources.append(url4)
        except:pass
            
        for final_url in sources:
            self.AddFileHost(list, res, final_url)




    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        from entertainment import requests
        import re

        name = self.CleanTextForSearch(name.lower())
        search =  '%s/?s=%s' %(self.base_url,name.replace(' ','+'))
        headers = {'User-Agent':self.User_Agent}
        link = requests.get(search, headers=headers, timeout=15).content

        try:
            
            links = link.split('article id=')[2:]
            
            for p in links:

                media_url = re.compile('href="([^"]+)"',re.DOTALL).findall(p)[0]
                media_title = re.compile('<p>([^<>]*)</p>',re.DOTALL).findall(p)[0]

                if type == 'tv_episodes':
                    if name in self.CleanTextForSearch(media_title.lower()):
                        season_pull = "0%s"%season if len(season)<2 else season
                        episode_pull = "0%s"%episode if len(episode)<2 else episode
                        sep = 's%se%s' %(season_pull,episode_pull)
                        if sep in self.CleanTextForSearch(media_title.lower()):
                            self.GetFileHosts(media_url, list, lock, message_queue, season, episode, type)
                else:
                    if name in self.CleanTextForSearch(media_title.lower()):
                        if year in media_title:
                            self.GetFileHosts(media_url, list, lock, message_queue, '', '', type)

        except:pass
            
