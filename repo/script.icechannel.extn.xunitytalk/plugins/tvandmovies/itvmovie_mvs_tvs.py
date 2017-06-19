

#iStream Extension
#iTVMovie
#Copyright (C) 2017 mucky duck


from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common
import xbmc


class iTVMovie(MovieSource,TVShowSource):

    implements = [MovieSource,TVShowSource]
    
    name = 'iTVMovie'
    display_name = 'iTVMovie'
    base_url = 'http://itvmovie.se'
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    
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




    def GetMedia(self, list, res,  data, ref):

        from entertainment import requests
        import re

        params = re.compile('var params = "lnk=(.+?)\&type=(.+?)"').findall(str(data))
        
        for param1, param2 in params:

            form_data = {'lnk': param1, 'type': param2}
            request_url = self.base_url + '/ajax/player'
            headers = {'origin': self.base_url, 'referer': ref, 'user-agent':self.User_Agent,'x-requested-with':'XMLHttpRequest'}
            final_link = requests.post(request_url, data=form_data, headers=headers).content

            if 'google' in param2:

                data = re.findall(r'"file":"([^"]+)".*?"label":"([^"]+)"', str(final_link), re.I|re.DOTALL)
                self.AddMedia(list,data)

            else:
                
                final_url = re.findall(r'<iframe[^>]+?src="([^"]+?)"', str(final_link), re.I|re.DOTALL)[0]
                self.AddFileHost(list, res, final_url)




    def GetFileHosts(self, url, list, lock, message_queue, season, episode, year, type):

        from entertainment import requests
        import re

        headers = {'User-Agent':self.User_Agent}
        link = requests.get(url, headers=headers).content

        res = ''
        media_year = ''


        try:
            
            match = link.split('>Release:<')[1:]

            for p in match:

                media_year = re.findall(r'<dd>([^<]+)</', str(p), re.I|re.DOTALL)[0].upper()
                res = re.findall(r'class="quality">([^<]+)</', str(p), re.I|re.DOTALL)[0]
                
                if '1080' in res:
                    res='1080P'                   
                elif '720' in res:
                    res='720P'
                elif 'HDCAM' in res:
                    res='CAM'
                elif 'HDTC' in res:
                    res='CAM'
                elif 'HD' in res:
                    res='HD'
                elif  '480' in res:
                    res='DVD'
                elif '360' in res:
                    res='SD'
                elif 'SD' in res:
                    res='SD'
                elif 'TC' in res:
                    res='CAM'
                elif 'CAM' in res:
                    res='CAM'
                else:
                    res='DVD'

        except:pass

        try:

            match2 = re.compile('href="([^"]+)".+?type="embed\|.+?>([^<]+)</').findall(link)

            for item_url, epi in match2:

                if type == 'tv_episodes':

                    if int(epi) == int(episode):
                        link2 = requests.get(item_url, headers=headers).content
                        self.GetMedia(list, res, link2, item_url)

                else:

                    if int(media_year) == int(year):
                        link2 = requests.get(item_url, headers=headers).content
                        self.GetMedia(list, res, link2, item_url)

        except:pass




    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):
        
        from entertainment import requests
        import re

        name = self.CleanTextForSearch(name.lower())
        headers = {'User-Agent':self.User_Agent}
        search = '%s/search/movie=%s' %(self.base_url,name.replace(' ','+'))
        link = requests.get(search, headers=headers).content

        try:

            links = link.split('item">')[1:]
            for p in links:

                media_url = re.compile('href="(.+?)"').findall(p)[0]
                if self.base_url not in media_url:
                    media_url = self.base_url + media_url
                media_title = re.compile('alt="(.+?)"').findall(p)[0].strip()

                if type == 'tv_episodes':
                    if '%s  season %s' %(name,season) in self.CleanTextForSearch(media_title.lower()):
                        self.GetFileHosts(media_url, list, lock, message_queue, season, episode, year, type)

                else:
                    if name in self.CleanTextForSearch(media_title.lower()):
                        self.GetFileHosts(media_url, list, lock, message_queue, '', '', year, type)

        except:pass
 
