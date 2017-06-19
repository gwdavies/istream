'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveTVIndexer
from entertainment.plugnplay import Plugin
from entertainment import common

class itv3_1(LiveTVIndexer):
    implements = [LiveTVIndexer]
    
    display_name = 'ITV3+1'
    
    name = 'itv3_1'
    
    other_names = 'itv3_plus_1'
    
    import xbmcaddon
    import os
    addon_id = 'script.icechannel.extn.uk'
    addon = xbmcaddon.Addon(addon_id)
    img = "http://static.filmon.com/couch/channels/1823/extra_big_logo.png"
    
    regions = [ 
            {
                'name':'United Kingdom', 
                'img':addon.getAddonInfo('icon'), 
                'fanart':addon.getAddonInfo('fanart')
                }, 
        ]
        
    languages = [ 
        {'name':'English', 'img':'', 'fanart':''}, 
        ]
        
    genres = [ 
        {'name':'Entertainment', 'img':'', 'fanart':''} 
        ]
    
    addon = None
    
