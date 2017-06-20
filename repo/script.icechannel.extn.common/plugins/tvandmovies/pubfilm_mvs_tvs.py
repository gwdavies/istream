'''
    PubFilm    
    Copyright (C) 2013 Mikey1234
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin


class pubfilm(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
    name = "PubFilm"
    display_name = "PubFilm"
    base_url = 'http://pubfilm.ac'
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
    source_enabled_by_default = 'true'




    def GetFileHosts(self, url, list, lock, message_queue,type,season,episode):

        from entertainment.net import Net


        import itertools,re

        net = Net(cached=False)

        headers={'User-Agent':self.User_Agent, 'Referer':self.base_url}

        content = net.http_GET(url,headers=headers).content

        host = self.base_url.split('//')[1].split('/')[0]
        headers={'Host': 'player.%s' %host, 'Referer': url, 'User-Agent': self.User_Agent}

        match=re.compile('<a href="(.+?player.+?)"target="EZWebPlayer".+?>(.+?)<').findall(content)

        for URL , EP in match:

            EPISODE = EP.replace('EPISODE','').replace('episode','').replace('SERVER','').replace('server','').replace(':','').strip()
            FINAL_URL = []
            QUALITY = []

            if type == 'tv_episodes':
                if EPISODE == '00':
                    EPISODE = int(EPISODE)+1
                EPISODE = int(EPISODE)
                if int(episode) == EPISODE:
                    try:
                        CONTENT = net.http_GET(URL,headers=headers).content

                        match = re.findall(r'file":"(.*?)"', str(CONTENT), re.I|re.DOTALL)
                        match2 = re.findall(r'label":"(.*?)"', str(CONTENT), re.I|re.DOTALL)

                        for url in match:
                            FINAL_URL.append(url)

                        for label in match2:
                            label = label.upper()   
                            if label == '1080P':
                                label = '1080P'
                            elif label == '720P':
                                label = '720P'                
                            elif label == '480P':
                                label = 'HD'
                            else:
                                label = 'SD'

                            QUALITY.append(label)

                        for url, qual in itertools.izip_longest(FINAL_URL,QUALITY):
                            HOST = url.split('//')[1].split('/')[0]
                            if qual == None:
                                qual = 'Unknown'
                            self.AddFileHost(list, qual, url, host=HOST.upper())
                    except:pass  
            else:

                try:
                    CONTENT = net.http_GET(URL,headers=headers).content

                    #data = re.findall(r'sources:(.*?)playerInstance', str(CONTENT), re.I|re.DOTALL)[0].replace(' ','')
                    match = re.findall(r'file":"(.*?)"', str(CONTENT), re.I|re.DOTALL)
                    match2 = re.findall(r'label":"(.*?)"', str(CONTENT), re.I|re.DOTALL)

                    for url in match:
                        FINAL_URL.append(url)

                    for label in match2:
                        label = label.upper()   
                        if label == '1080P':
                            label = '1080P'
                        elif label == '720P':
                            label = '720P'                
                        elif label == '480P':
                            label = 'HD'
                        else:
                            label = 'SD'

                        QUALITY.append(label)

                    for url, qual in itertools.izip_longest(FINAL_URL,QUALITY):
                        HOST = url.split('//')[1].split('/')[0]
                        if qual == None:
                            qual = 'Unknown'
                        self.AddFileHost(list, qual, url, host=HOST.upper())
                except:pass



    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 


      from entertainment.net import Net


      import re
      net = Net(cached=False)
        
      name = self.CleanTextForSearch(name.lower())

      headers = {'User-Agent':self.User_Agent, 'Referer': self.base_url}
      new_url = '%s/search/%s' %(self.base_url,name.replace(' ','+'))
      content = net.http_GET(new_url,headers=headers).content
      
      matched = re.compile('<h3 class="post-box-title"><a href="(.+?)" rel="bookmark">(.+?)</a>').findall(content)
      for URL, TITLE in matched:
              
          if type == 'tv_episodes':
            if name.lower() in self.CleanTextForSearch(TITLE.lower()):
              if 'season '+season in TITLE.lower():
                self.GetFileHosts(URL, list, lock, message_queue,type,season,episode)
        
          else:
            if name.lower() in self.CleanTextForSearch(TITLE.lower()):
              if year in TITLE.lower():  
                self.GetFileHosts(URL, list, lock, message_queue,type,season,episode)




    def Resolve(self, url):
        from entertainment import istream
        url = url.replace('amp;','')
        resolved = istream.ResolveUrl(url)
        return resolved
