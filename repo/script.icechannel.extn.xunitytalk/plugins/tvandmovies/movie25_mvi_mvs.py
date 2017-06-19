'''
    iStream
    Movie25 - by Coolwave    
    
'''

from entertainment.plugnplay.interfaces import MovieIndexer
from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common
import re



class movie25(MovieIndexer, MovieSource):
    implements = [MovieIndexer, MovieSource]
    
    name = "movie25"
    display_name ="Movie25"
    base_url = 'http://tinklepad.ag/'
    img='https://raw.githubusercontent.com/Coolwavexunitytalk/images/master/movie25.png'
    default_indexer_enabled = 'false'
    source_enabled_by_default = 'true'


    def ExtractContentAndAddtoList(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''): 

        if page == '':
            page = '1'


        
        from entertainment.net import Net
        
        net = Net(cached=False)
        import urllib
        url = urllib.unquote_plus(url)
        new_url = self.base_url+section+'/'
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'}
        html = net.http_GET(new_url+str(page),headers=headers).content
     
        if total_pages == '':
            lastlist = '/'+section+'/'
            r= ">Next</a>&nbsp;&nbsp;&nbsp;<a href='%s(.+?)/'>Last</a>" % lastlist
            total_pages = re.compile(r).findall(html)[0]
            
        self.AddInfo(list, indexer, section, '', type, str(page), total_pages)

        if section == 'featured' or 'new-release' or 'latest-added' or 'latest-hd' or 'most-popular' or 'most-voted' or 'az' or 'genres':
            match=re.compile('<div class="movie_pic"><a href="(.+?)".+?target="_self".+?title="Watch (.+?) \((.+?)\)',re.DOTALL).findall(html.replace(' Online Free',''))
            for url,name,year in match:
                name = self.CleanTextForSearch(name)
                self.AddContent(list,indexer,common.mode_File_Hosts,name + ' (' + year +')' ,'',type, url=url, name=name, year=year)

        
            

    def GetSection(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''):
        
        from entertainment.net import Net
        
        net = Net(cached=False)
    
        url_type = ''
        content_type = ''

        
        if indexer == common.indxr_Movies:
            url_type = 'movies/'
        

        if section == 'main':
            self.AddSection(list, indexer,'featured','Featured',self.base_url +'featured/',indexer)
            self.AddSection(list, indexer,'new-release','New Releases',self.base_url +'new-release/',indexer)
            self.AddSection(list, indexer,'latest-added','Latest Added',self.base_url +'latest-added/',indexer)
            self.AddSection(list, indexer,'latest-hd','Latest HD',self.base_url +'latest-hd/',indexer)
            self.AddSection(list, indexer,'most-popular','Most Popular',self.base_url +'most-popular/',indexer)
            self.AddSection(list, indexer,'most-voted','Most Voted',self.base_url +'most-voted/',indexer)
            self.AddSection(list, indexer,'az','A-Z',self.base_url,indexer)
            self.AddSection(list, indexer,'genres','Genres',self.base_url,indexer)
            #self.AddSection(list, indexer,'year','Year','http://www.movie25.so/',indexer)

        elif section == 'az':
            self.AddSection(list, indexer,'0-9','0-9',self.base_url +'0-9/',indexer)
            self.AddSection(list, indexer,'a','A',self.base_url +'a/',indexer)
            self.AddSection(list, indexer,'b','B',self.base_url +'b/',indexer)
            self.AddSection(list, indexer,'c','C',self.base_url +'c/',indexer)
            self.AddSection(list, indexer,'d','D',self.base_url +'d/',indexer)
            self.AddSection(list, indexer,'e','E',self.base_url +'e/',indexer)
            self.AddSection(list, indexer,'f','F',self.base_url +'f/',indexer)
            self.AddSection(list, indexer,'g','G',self.base_url +'g/',indexer)
            self.AddSection(list, indexer,'h','H',self.base_url +'h/',indexer)
            self.AddSection(list, indexer,'i','I',self.base_url +'i/',indexer)
            self.AddSection(list, indexer,'j','J',self.base_url +'j/',indexer)
            self.AddSection(list, indexer,'k','K',self.base_url +'k/',indexer)
            self.AddSection(list, indexer,'l','L',self.base_url +'l/',indexer)
            self.AddSection(list, indexer,'m','M',self.base_url +'m/',indexer)
            self.AddSection(list, indexer,'n','N',self.base_url +'n/',indexer)
            self.AddSection(list, indexer,'o','O',self.base_url +'o/',indexer)
            self.AddSection(list, indexer,'p','P',self.base_url +'p/',indexer)
            self.AddSection(list, indexer,'q','Q',self.base_url +'q/',indexer)
            self.AddSection(list, indexer,'r','R',self.base_url +'r/',indexer)
            self.AddSection(list, indexer,'s','S',self.base_url +'s/',indexer)
            self.AddSection(list, indexer,'t','T',self.base_url +'t/',indexer)
            self.AddSection(list, indexer,'u','U',self.base_url +'u/',indexer)
            self.AddSection(list, indexer,'v','V',self.base_url +'v/',indexer)
            self.AddSection(list, indexer,'w','W',self.base_url +'w/',indexer)
            self.AddSection(list, indexer,'x','X',self.base_url +'x/',indexer)
            self.AddSection(list, indexer,'y','Y',self.base_url +'y/',indexer)
            self.AddSection(list, indexer,'z','Z',self.base_url +'z/',indexer)
                        
        elif section == 'genres':
            self.AddSection(list, indexer,'action','Action',self.base_url +'action/',indexer)
            self.AddSection(list, indexer,'adventure','Adventure',self.base_url +'adventure/',indexer)
            self.AddSection(list, indexer,'animation','Animation',self.base_url +'animation/',indexer)
            self.AddSection(list, indexer,'biography','Biography',self.base_url +'biography/',indexer)
            self.AddSection(list, indexer,'comedy','Comedy',self.base_url +'comedy/',indexer)
            self.AddSection(list, indexer,'crime','Crime',self.base_url +'crime/',indexer)
            self.AddSection(list, indexer,'documentary','Documentary',self.base_url +'documentary/',indexer)
            self.AddSection(list, indexer,'drama','Drama',self.base_url +'drama/',indexer)
            self.AddSection(list, indexer,'family','Family',self.base_url +'family/',indexer)
            self.AddSection(list, indexer,'fantasy','Fantasy',self.base_url +'fantasy/',indexer)
            self.AddSection(list, indexer,'history','History',self.base_url +'history/',indexer)
            self.AddSection(list, indexer,'horror','Horror',self.base_url +'horror/',indexer)
            self.AddSection(list, indexer,'music','Music',self.base_url +'music/',indexer)
            self.AddSection(list, indexer,'musical','Musical',self.base_url +'musical/',indexer)
            self.AddSection(list, indexer,'mystery','Mystery',self.base_url +'mystery/',indexer)
            self.AddSection(list, indexer,'romance','Romance',self.base_url +'romance/',indexer)
            self.AddSection(list, indexer,'sci-fi','Sci-Fi',self.base_url +'sci-fi/',indexer)
            self.AddSection(list, indexer,'short','Short',self.base_url +'short/',indexer)
            self.AddSection(list, indexer,'thriller','Thriller',self.base_url +'thriller/',indexer)
            self.AddSection(list, indexer,'war','War',self.base_url +'war/',indexer)
            self.AddSection(list, indexer,'western','Western',self.base_url +'western/',indexer)
            
            

        elif section == 'year':

            from entertainment.net import Net
        

        else:
            self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)
            


          
    def GetFileHosts(self, url, list, lock, message_queue):
        import re
        
        from entertainment.net import Net
        net = Net(cached=False)
        
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'}

        content = net.http_GET(url,headers=headers).content

        
        QUALITY  = content.split('>Links - Quality')[1]
        quality=QUALITY.split('</h1')[0].strip()


        link = content.split('<li id="link_name"')
  
        for p in link:
            p=p.replace('\n','').replace('\t','')
            try:
                match=re.compile('>(.+?)</li>.+?li id="playing_button"><a href="(.+?)"',re.DOTALL).findall(p)
                for host , url in match:
                    host = host.replace(' ','')
                    
                    res = 'SD'
                    
                    if 'HD' in quality:
                        res = '720P'                
                    elif 'DVD' in quality:
                        res = 'DVD'
                    elif 'CAM' in quality:
                        res= 'CAM'
                    if not 'hdsponsor' in host.lower():    
                        self.AddFileHost(list, res, url, host.upper())
            except:pass
            


            

    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        if type!= 'movies': return
        import re
        
        from entertainment.net import Net
        net = Net(cached=False)

        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)

        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'}

        import urllib
       
        movie_url = self.base_url + ( 'search.php?q=%s' % name.replace(' ','+') + '+' + year.replace(' ','+') ) 
        
        content = net.http_GET(movie_url,headers=headers).content

        DATA=re.compile('type="submit" name=".+?" id="(.+?)" value="(.+?)"').findall(content)
        
        content = net.http_POST(movie_url,{DATA[0][0]:DATA[0][1]},headers=headers).content
      
        search_result = re.search(r'<div class="movie_pic"><a href="(.+?)"', content)
        if search_result:
            search_result = search_result.group(1)
        
            self.GetFileHosts(search_result, list, lock, message_queue)
            

        

    def Resolve(self, url):

        from entertainment.net import Net
        import re


        net = Net(cached=False)
        headers={'Referer': url,'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
        data={url.split('?')[1].replace('=',''):'','chtc':'Click Here to Continue'}
        html = net.http_POST(url,data,headers=headers).content

        #print html.encode('ascii','ignore')
        
        match2=re.compile('id="showvideo" src="(.+?)"').findall(html)[0]
        xbmc.log(match2)
        from entertainment import istream
        play_url = istream.ResolveUrl(match2)
        return play_url
