'''
    http://moviehdmax.com/    
    Copyright (C) 2013 Mikey1234
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common
import os,xbmc

class moviehdmax(MovieSource,TVShowSource):

    implements = [MovieSource,TVShowSource]
    
    name = 'moviehdmax'
    display_name = 'Movie HD Max'
    base_url = 'http://moviehdmax.com'
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
   
    source_enabled_by_default = 'true'

    cookie_file = os.path.join(common.cookies_path, 'moviehdmax.cookie')            
    
    def GetFileHosts(self, url, list, lock, message_queue,type,season,episode):

        import re,json
        from entertainment.net import Net
        net = Net(cached=False)
         

        headers={'Host':'moviehdmax.com',
               'Connection':'keep-alive',
               'Accept':'text/plain, */*; q=0.01',
               'X-Requested-With':'XMLHttpRequest',
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
               'Accept-Encoding':'gzip, deflate, sdch',
               'Accept-Language':'en-US,en;q=0.8'}
        
        net.set_cookies(self.cookie_file)                         
     
   
        

        if type == 'tv_episodes':
            
            headers={'Host':'moviehdmax.com',
                   'Connection':'keep-alive',
                   'Referer':url,
                   'X-Requested-With':'XMLHttpRequest',
                   'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                   'Accept-Encoding':'gzip, deflate, sdch',
                   'Accept-Language':'en-US,en;q=0.8'}

            data={'p':episode}
            POST=url.replace('/watch/','/getepisode/')
            content = net.http_POST(POST,data,headers=headers).content
            link=json.loads(content)
            data=link['sources']
            for field in data:
                quality=field['quality']+'P'
                FINAL_URL=field['host']
                if '1080P' in quality.upper():
                    Q ='1080P'
                elif '720P' in quality.upper():
                    Q ='720P'                
                elif '480P' in quality.upper():
                    Q ='HD'
                else:
                    Q ='SD'
                self.AddFileHost(list, Q, FINAL_URL)
                
        else:
            content = net.http_GET(url,headers=headers).content
            match=re.compile('<source src="(.+?)".+?data-res="(.+?)"').findall(content)
            for FINAL_URL , quality in match:
                
                if '1080' in quality.upper():
                    Q ='1080P'
                elif '720' in quality.upper():
                    Q ='720P'                
                elif '480' in quality.upper():
                    Q ='HD'
                else:
                    Q ='SD'
                self.AddFileHost(list, Q, FINAL_URL)
    
        
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        from entertainment import requests
        from entertainment import cloudflare
        import re

        name = self.CleanTextForSearch(name.lower())

        if type == 'tv_episodes':
            search = '%s/search/result?s=%s+%s&selected=false' %(self.base_url,name.replace(' ','+'),season)
        else:
            search = '%s/search/result?s=%s&selected=false' %(self.base_url,name.replace(' ','+'))

        headers = {'User-Agent':self.User_Agent}
        link = requests.get(search,headers=headers)

        try:

            if link.headers['server'].lower() == 'cloudflare-nginx':

                link = cloudflare.solve(search, UA=self.User_Agent)

            else:
                link = link.content

        except:
            link = link.content

        match = re.compile('<a href="\.\./(.+?)">(.+?)</a>').findall(str(link))

        for url, title in match:

            item_url = '%s/%s' %(self.base_url,url)

            if name in self.CleanTextForSearch(title.lower()):

                if type == 'tv_episodes':
                    if 'season-'+season in item_url or '-%s-' %season in item_url:
                        self.GetFileHosts(item_url, list, lock, message_queue,type,season,episode)
                else:
                    if year in title:
                        self.GetFileHosts(item_url, list, lock, message_queue,type,season,episode)
           
       

