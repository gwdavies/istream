import xbmc
import xbmcgui

# xbmc global Variable
iStreamProgressDialog = ""
yume = ""

class Player(xbmc.Player):
    def setVars(self, p_YUME):
        self.yume = p_YUME
                
    def onPlayBackStarted(self):
        import threading        
        threading.Thread(target=self.yume.playerTracker).start()
    
    def onPlayBackEnded(self):
        self.yume.force = True

    
        
class YUME:
    def __init__(self):
        
        import xbmcgui
        self.force = False
        self.win = xbmcgui.Window(10000)
        self.YumeUrlSep = "||YUME-URL-SEP||"
        self.YumeAdRequestUrl = self.win.getProperty("YUME-AD-REQUEST-URL")
        self.YumeVideoAd = self.win.getProperty("YUME-VIDEO-AD")
        self.YumeVideoAdDur = self.ConvertStringToInt(self.win.getProperty("YUME-VIDEO-AD-DURATION"))
        self.YumeVideoAd000PctTrackUrls = self.win.getProperty("YUME-VIDEO-AD-000-PCT-URL-CSV")
        self.YumeVideoAd025PctTrackUrls = self.win.getProperty("YUME-VIDEO-AD-025-PCT-URL-CSV")
        self.YumeVideoAd050PctTrackUrls = self.win.getProperty("YUME-VIDEO-AD-050-PCT-URL-CSV")
        self.YumeVideoAd075PctTrackUrls = self.win.getProperty("YUME-VIDEO-AD-075-PCT-URL-CSV")
        self.YumeVideoAd100PctTrackUrls = self.win.getProperty("YUME-VIDEO-AD-100-PCT-URL-CSV")
        self.YumeClientIP = self.win.getProperty("YUME-CLIENT-IP")
        if not self.YumeClientIP or len(self.YumeClientIP) <= 0 or self.YumeClientIP == '0.0.0.0':
            self.YumeClientIP = self.get_external_ip()
            self.win.setProperty('YUME-CLIENT-IP', self.YumeClientIP )
        
    def get_external_ip(self):
        
        import urllib
        import re
        try:
            site = urllib.urlopen("http://checkip.dyndns.org/").read()
            grab = re.findall('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', site)
            address = grab[0]
        except:
            address = "0.0.0.0"
        
        return address
    def ConvertStringToInt(self, s):
        try: 
            return int(s)
        except ValueError:
            return 0
            
    def load(self, ad_request_url="http://plg1.yumenetworks.com/dynamic_preroll_playlist.xml?domain=1992TRzjSSba", force=False):
        
        self.YumeAdRequestUrl = ad_request_url
        
        self.win.setProperty('YUME-AD-REQUEST-URL', self.YumeAdRequestUrl)
                
        ad_ip_append = ""
        if self.YumeClientIP and len(self.YumeClientIP) > 0 and self.YumeClientIP != "0.0.0.0":
            ad_ip_append = "&client_ip=" + self.YumeClientIP
        import urllib2
        headers = { 'User-Agent' : 'Mozilla/5.0' }
        
        video_url = None
        video_url_retry = 3
        
        while video_url == None and video_url_retry > 0:
            
            video_url_retry = video_url_retry - 1
            req = urllib2.Request(self.YumeAdRequestUrl, None, headers)
            yume_ad_data = urllib2.urlopen(req).read()
            
            
            import re
            #video_url = re.search('(?s)<flash_streaming_url.+?(http.+?\.flv)', yume_ad_data)
            video_url = re.search('(?s)<mp4_streaming_url.+?(http.+?\.mp4)', yume_ad_data)
        
        if not video_url:
            
            self.YumeVideoAd = ""
            self.win.setProperty('YUME-VIDEO-AD', self.YumeVideoAd )
            self.YumeVideoAdDur = 0
            self.win.setProperty('YUME-VIDEO-AD-DURATION', str(self.YumeVideoAdDur) )
            self.YumeVideoAd000PctTrackUrls = ""
            self.win.setProperty('YUME-VIDEO-AD-000-PCT-URL-CSV', self.YumeVideoAd000PctTrackUrls) 
            self.YumeVideoAd025PctTrackUrls = ""
            self.win.setProperty('YUME-VIDEO-AD-025-PCT-URL-CSV', self.YumeVideoAd025PctTrackUrls) 
            self.YumeVideoAd050PctTrackUrls = ""
            self.win.setProperty('YUME-VIDEO-AD-050-PCT-URL-CSV', self.YumeVideoAd050PctTrackUrls) 
            self.YumeVideoAd075PctTrackUrls = ""
            self.win.setProperty('YUME-VIDEO-AD-075-PCT-URL-CSV', self.YumeVideoAd075PctTrackUrls) 
            self.YumeVideoAd100PctTrackUrls = ""
            self.win.setProperty('YUME-VIDEO-AD-100-PCT-URL-CSV', self.YumeVideoAd100PctTrackUrls) 
            return
            
        video_url = video_url.group(1)
        self.YumeVideoAd = video_url
        self.win.setProperty('YUME-VIDEO-AD', self.YumeVideoAd )
        
        self.YumeVideoAdDur = self.ConvertStringToInt(re.search('<duration>(.+?)</duration>', yume_ad_data).group(1))
        self.win.setProperty('YUME-VIDEO-AD-DURATION', str(self.YumeVideoAdDur) )
        
        yume_000_pcts = ""
        pct_000 = 0
        for yume_000_pct in re.finditer('(?s)<tracking.+?<impressiontracker[>\t\n\r\f\v ]+(http.+?)[<\t\n\r\f\v]', yume_ad_data):
            if pct_000 > 0:
                yume_000_pcts += self.YumeUrlSep
            yume_000_pcts += yume_000_pct.group(1)
            pct_000 += 1
        self.YumeVideoAd000PctTrackUrls = yume_000_pcts
        self.win.setProperty('YUME-VIDEO-AD-000-PCT-URL-CSV', self.YumeVideoAd000PctTrackUrls) 
        
        yume_025_pcts = ""
        pct_025 = 0
        for yume_025_pct in re.finditer('(?s)<impressiontracker begin="25%".+?(http.+?)[<\t\n\r\f\v]', yume_ad_data):
            if pct_025 > 0:
                yume_025_pcts += self.YumeUrlSep
            yume_025_pcts += yume_025_pct.group(1)
            pct_025 += 1
        self.YumeVideoAd025PctTrackUrls = yume_025_pcts
        self.win.setProperty('YUME-VIDEO-AD-025-PCT-URL-CSV', self.YumeVideoAd025PctTrackUrls) 
       
        yume_050_pcts = ""
        pct_050 = 0
        for yume_050_pct in re.finditer('(?s)<impressiontracker begin="50%".+?(http.+?)[<\t\n\r\f\v]', yume_ad_data):
            if pct_050 > 0:
                yume_050_pcts += self.YumeUrlSep
            yume_050_pcts += yume_050_pct.group(1)
            pct_050 += 1
        self.YumeVideoAd050PctTrackUrls = yume_050_pcts
        self.win.setProperty('YUME-VIDEO-AD-050-PCT-URL-CSV', self.YumeVideoAd050PctTrackUrls) 
    
        yume_075_pcts = ""
        pct_075 = 0
        for yume_075_pct in re.finditer('(?s)<impressiontracker begin="75%".+?(http.+?)[<\t\n\r\f\v]', yume_ad_data):
            if pct_075 > 0:
                yume_075_pcts += self.YumeUrlSep
            yume_075_pcts += yume_075_pct.group(1)
            pct_075 += 1
        self.YumeVideoAd075PctTrackUrls = yume_075_pcts
        self.win.setProperty('YUME-VIDEO-AD-075-PCT-URL-CSV', self.YumeVideoAd075PctTrackUrls) 
            
        yume_100_pcts = ""
        pct_100 = 0
        for yume_100_pct in re.finditer('(?s)<impressiontracker begin="100%".+?(http.+?)[<\t\n\r\f\v]', yume_ad_data):
            if pct_100 > 0:
                yume_100_pcts += self.YumeUrlSep
            yume_100_pcts += yume_100_pct.group(1)
            pct_100 += 1
        self.YumeVideoAd100PctTrackUrls = yume_100_pcts        
        self.win.setProperty('YUME-VIDEO-AD-100-PCT-URL-CSV', self.YumeVideoAd100PctTrackUrls)
        
        

    def getAd(self, ad_request_url="http://plg1.yumenetworks.com/dynamic_preroll_playlist.xml?domain=1992TRzjSSba"):
        self.load(ad_request_url)        
    
    def trackUrls(self, urls):
        
        import urllib2
        headers = { 'User-Agent' : 'Mozilla/5.0' }
        for url in urls:
            try:    
                
                req = urllib2.Request(url.replace("&amp;","&"), None, headers)
                urllib2.urlopen(req)
            except:
                pass
        
    
    def playerTracker(self, force=False):
        
        self.pct_000_trackers_called = True
        self.trackUrls(filter(None, self.YumeVideoAd000PctTrackUrls.split(self.YumeUrlSep)))
        
        import time
        import threading
        while True:
            if self.pct_025_trackers_called == False and (self.force == True or (self.player.isPlaying() and self.player.getTime() / self.YumeVideoAdDur >= 0.25) ):
                self.pct_025_trackers_called = True
                self.trackUrls(filter(None,self.YumeVideoAd025PctTrackUrls.split(self.YumeUrlSep)))
            if self.pct_050_trackers_called == False and (self.force==True or (self.player.isPlaying() and self.player.getTime() / self.YumeVideoAdDur >= 0.5) ):
                self.pct_050_trackers_called = True
                self.trackUrls(filter(None,self.YumeVideoAd050PctTrackUrls.split(self.YumeUrlSep)))
            if self.pct_075_trackers_called == False and (self.force==True or (self.player.isPlaying() and self.player.getTime() / self.YumeVideoAdDur >= 0.75) ):
                self.pct_075_trackers_called = True
                self.trackUrls(filter(None,self.YumeVideoAd075PctTrackUrls.split(self.YumeUrlSep)))
            if self.pct_025_trackers_called == True and self.pct_050_trackers_called == True and self.pct_075_trackers_called == True:
                break
            time.sleep(3)            
        
        self.pct_100_trackers_called = True
        self.trackUrls(filter(None,self.YumeVideoAd100PctTrackUrls.split(self.YumeUrlSep)))
        
        del self.player
        self.player = ""
        del self
        self=""
    
    def playAd(self, ad_request_url="http://plg1.yumenetworks.com/dynamic_preroll_playlist.xml?domain=1992TRzjSSba"):
        
        self.getAd(ad_request_url)                
        self.player = Player()
        self.player.setVars(self)
        
        self.pct_000_trackers_called = False
        self.pct_025_trackers_called = False
        self.pct_050_trackers_called = False
        self.pct_075_trackers_called = False
        self.pct_100_trackers_called = False
        
        
        self.player.play(self.YumeVideoAd, xbmcgui.ListItem('AD'), True)
        
        
    def stopAd(self):
        
        import xbmc 
        try:
            while self.player.isPlaying() and self.player.getTime() <= 15:
                xbmc.sleep(1000)
            if self.player.isPlaying():
                
                self.player.stop()
        except:
            
            pass
        

        
class DialogiStreamProgress( xbmcgui.WindowXMLDialog ):

    def onInit(self):
        self.getControl(1).setLabel( self.header )
        
        self.progressMessageList = self.getControl(3)
        self.addUpdateItem(self.first_list_item)
        
    def setVars(self, header, first_list_item):
        self.header = header
        self.first_list_item = first_list_item
        
    def waitForInit(self):
        import time
        initialized = False
        while initialized == False :
            try:
                self.progressMessageList.size()
                initialized = True
            except:
                time.sleep(0.2)
            
             
    def onFocus( self, controlID ): pass
    
    def onClick( self, controlID ): pass
        
    def onAction( self, action ):            
        #if action in [ 5, 6, 7, 8, 9, 10, 92, 117 ] or action.getButtonCode() in [ 275, 257, 261 ]:
        #    self.close()
        pass
            
    def addItem(self, label):
        self.waitForInit()
        self.progressMessageList.addItem(label)
        self.progressMessageList.selectItem(self.progressMessageList.size() - 1)
    
    def updateItem(self, label, index):
        self.waitForInit()
        self.progressMessageList.getListItem(index).setLabel(label)
        self.progressMessageList.selectItem(index)
        
    def addUpdateItem(self, label, index=-1):
        self.waitForInit()
        if (index == -1 or index >= self.progressMessageList.size()):
            self.addItem(label)
        else:
            self.updateItem(label, index)   
    
            
def show(header="", first_list_item=""):
        
    global iStreamProgressDialog
    if iStreamProgressDialog and iStreamProgressDialog != "":
        iStreamProgressDialog.show()
    
    import xbmcaddon
    addon_id = 'script.istream.dialogs'
    ADDON = xbmcaddon.Addon(id = addon_id)
    iStreamProgressDialog = DialogiStreamProgress("DialogiStreamProgress.xml",ADDON.getAddonInfo('path'),'istream')
    iStreamProgressDialog.setVars(header, first_list_item)
    iStreamProgressDialog.show()
    import xbmc
    xbmc.sleep(1000)
    
    global yume
    yume = YUME()
    yume.playAd()

def addUpdateItem( label, index = -1 ):
    global iStreamProgressDialog
    iStreamProgressDialog.addUpdateItem(label, index)
    
def close():
    global yume
    yume.stopAd()
    
    global iStreamProgressDialog
    iStreamProgressDialog.close()
    del iStreamProgressDialog
    iStreamProgressDialog = ""
    
    