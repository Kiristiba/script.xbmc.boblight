# -*- coding: utf-8 -*- 
'''
    Boblight for Kodi
    Copyright (C) 2012 Team XBMC

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys
import datetime
import time
import xbmc, xbmcgui

__scriptname__ = sys.modules[ "__main__" ].__scriptname__
__addon__      = sys.modules[ "__main__" ].__addon__
__cwd__        = sys.modules[ "__main__" ].__cwd__
__icon__       = sys.modules[ "__main__" ].__icon__
__language__   = sys.modules[ "__main__" ].__language__
__ID__   = sys.modules[ "__main__" ].__ID__

from boblight import *
from tools import log

try:
    throwaway = datetime.datetime.strptime('20110101','%Y%m%d')
except TypeError:
    throwaway = datetime.datetime(*(time.strptime('20110101','%Y%m%d')[0:6]))

bob = Boblight()

BLING = [[255,0,0],[0,255,0],[0,0,255],[0,0,0]]
OPTS  = ['saturation','value','speed','autospeed','interpolation','threshold']

class settings():
  def __init__( self, *args, **kwargs ):
    log('settings() - __init__')
    self.staticBobActive            = False
    self.run_init                   = True
    self.category                   = "static"
    self.networkaccess              = __addon__.getSetting("networkaccess") == "true"
    if not self.networkaccess:
      self.hostip   = None
      self.hostport = -1
    else:
      self.hostip                     = __addon__.getSetting("hostip")
      self.hostport                   = int(__addon__.getSetting("hostport")) 
    self.start()
     
  def start(self):
    log('settings() - start')
    self.reconnect                  = False
    self.force_update               = True  
    self.networkaccess              = __addon__.getSetting("networkaccess") == "true"  
    self.overwrite_cat              = __addon__.getSetting("overwrite_cat") == "true"
    self.overwrite_cat_val          = int(__addon__.getSetting("overwrite_cat_val"))
    self.bobdisableonscreensaver    = __addon__.getSetting("bobdisableonscreensaver") == "true"
    self.bobdisable                 = __addon__.getSetting("bobdisable") == "true"
    self.bobdisableon3d             = __addon__.getSetting("bobdisableon3d") == "true"
    try:
      self.enabledfrom                = datetime.datetime.strptime(__addon__.getSetting("enfrom"), '%H:%M')
      self.enabledto                  = datetime.datetime.strptime(__addon__.getSetting("ento"), '%H:%M')
    except TypeError:
      self.enabledfrom                = datetime.datetime(*(time.strptime(__addon__.getSetting("enfrom"), '%H:%M:%S')[0:6]))
      self.enabledto                  = datetime.datetime(*(time.strptime(__addon__.getSetting("ento"), '%H:%M:%S')[0:6]))
    self.current_option             = ""
    
    if not self.networkaccess:
      self.hostip   = None
      self.hostport = -1
      self.reconnect = True
    else:
      hostip                   = __addon__.getSetting("hostip")
      hostport                 = int(__addon__.getSetting("hostport"))
      if ((self.hostip != hostip) or (self.hostport != hostport)):
        self.hostip   = hostip
        self.hostport = hostport        
        self.reconnect = True

    self.frame_capture_interval        = int(float(__addon__.getSetting("frame_capture_interval")))
    self.frame_capture_width           = int(float(__addon__.getSetting("frame_capture_width")))
    self.frame_capture_height          = int(float(__addon__.getSetting("frame_capture_height")))
    
    # Other settings
    self.other_static_bg            = __addon__.getSetting("other_static_bg") == "true"
    self.other_static_red           = int(float(__addon__.getSetting("other_static_red")))
    self.other_static_green         = int(float(__addon__.getSetting("other_static_green")))
    self.other_static_blue          = int(float(__addon__.getSetting("other_static_blue")))
    self.other_misc_initialflash    = __addon__.getSetting("other_misc_initialflash") == "true"
    self.other_misc_notifications   = __addon__.getSetting("other_misc_notifications") == "true"
    
    # Movie settings
    self.movie_saturation           = float(__addon__.getSetting("movie_saturation"))
    self.movie_value                = float(__addon__.getSetting("movie_value"))
    self.movie_speed                = float(__addon__.getSetting("movie_speed"))
    self.movie_autospeed            = float(__addon__.getSetting("movie_autospeed"))
    self.movie_interpolation        = int(__addon__.getSetting("movie_interpolation") == "true")
    self.movie_threshold            = float(__addon__.getSetting("movie_threshold"))
    self.movie_preset               = int(__addon__.getSetting("movie_preset"))
    self.movie_scan_v               = float(__addon__.getSetting("movie_scan_v"))
    self.movie_scan_h               = float(__addon__.getSetting("movie_scan_h"))
    self.movie_scan_threshold       = int(float(__addon__.getSetting("movie_scan_threshold")))
    self.movie_scan_range           = float(__addon__.getSetting("movie_scan_range"))

    # TV Shows settings
    self.tvshow_saturation           = float(__addon__.getSetting("tvshow_saturation"))
    self.tvshow_value                = float(__addon__.getSetting("tvshow_value"))
    self.tvshow_speed                = float(__addon__.getSetting("tvshow_speed"))
    self.tvshow_autospeed            = float(__addon__.getSetting("tvshow_autospeed"))
    self.tvshow_interpolation        = int(__addon__.getSetting("tvshow_interpolation") == "true")
    self.tvshow_threshold            = float(__addon__.getSetting("tvshow_threshold"))
    self.tvshow_preset               = int(__addon__.getSetting("tvshow_preset"))
    self.tvshow_scan_v               = float(__addon__.getSetting("tvshow_scan_v"))
    self.tvshow_scan_h               = float(__addon__.getSetting("tvshow_scan_h"))
    self.tvshow_scan_threshold       = int(float(__addon__.getSetting("tvshow_scan_threshold")))
    self.tvshow_scan_range           = float(__addon__.getSetting("tvshow_scan_range"))

    # LiveTV settings
    self.livetv_saturation           = float(__addon__.getSetting("livetv_saturation"))
    self.livetv_value                = float(__addon__.getSetting("livetv_value"))
    self.livetv_speed                = float(__addon__.getSetting("livetv_speed"))
    self.livetv_autospeed            = float(__addon__.getSetting("livetv_autospeed"))
    self.livetv_interpolation        = int(__addon__.getSetting("livetv_interpolation") == "true")
    self.livetv_threshold            = float(__addon__.getSetting("livetv_threshold"))
    self.livetv_preset               = int(__addon__.getSetting("livetv_preset"))
    self.livetv_scan_v               = float(__addon__.getSetting("livetv_scan_v"))
    self.livetv_scan_h               = float(__addon__.getSetting("livetv_scan_h"))
    self.livetv_scan_threshold       = int(float(__addon__.getSetting("livetv_scan_threshold")))
    self.livetv_scan_range           = float(__addon__.getSetting("livetv_scan_range"))

    # Files settings
    self.files_saturation           = float(__addon__.getSetting("files_saturation"))
    self.files_value                = float(__addon__.getSetting("files_value"))
    self.files_speed                = float(__addon__.getSetting("files_speed"))
    self.files_autospeed            = float(__addon__.getSetting("files_autospeed"))
    self.files_interpolation        = int(__addon__.getSetting("files_interpolation") == "true")
    self.files_threshold            = float(__addon__.getSetting("files_threshold"))
    self.files_preset               = int(__addon__.getSetting("files_preset"))
    self.files_scan_v               = float(__addon__.getSetting("files_scan_v"))
    self.files_scan_h               = float(__addon__.getSetting("files_scan_h"))
    self.files_scan_threshold       = int(float(__addon__.getSetting("files_scan_threshold")))
    self.files_scan_range           = float(__addon__.getSetting("files_scan_range"))

    # Music Video settings
    self.music_saturation           = float(__addon__.getSetting("musicvideo_saturation"))
    self.music_value                = float(__addon__.getSetting("musicvideo_value"))
    self.music_speed                = float(__addon__.getSetting("musicvideo_speed"))
    self.music_autospeed            = float(__addon__.getSetting("movie_autospeed"))
    self.music_interpolation        = int(__addon__.getSetting("musicvideo_interpolation") == "true")
    self.music_threshold            = float(__addon__.getSetting("musicvideo_threshold"))
    self.music_preset               = int(__addon__.getSetting("musicvideo_preset"))
    self.music_scan_v               = float(__addon__.getSetting("musicvideo_scan_v"))
    self.music_scan_h               = float(__addon__.getSetting("musicvideo_scan_h"))
    self.music_scan_threshold       = int(float(__addon__.getSetting("musicvideo_scan_threshold")))
    self.music_scan_range           = float(__addon__.getSetting("musicvideo_scan_range"))

  def resetBobDisable(self):
    # reset the bobdisable setting from settings
    self.bobdisable = __addon__.getSetting("bobdisable") == "true" 
    if not self.bobdisable:#if we are not disabled in general
      if self.category == "static":
        self.handleStaticBgSettings()#turns on or off the lights based on static settings
      else:#we are playing something - turn the lights on
        bob.bob_set_priority(128) #lights on

  def setScreensaver(self, enabled):
    if self.bobdisableonscreensaver and enabled:
      self.bobdisable = True
    else:
      # reset the bobdisable setting from settings
      self.resetBobDisable()

  #handle boblight configuration from the "Movie" category
  #returns the new settings
  def setupForMovie(self):
    log('settings() - setupForMovie')
  
    if self.movie_preset == 1:       #preset smooth
      saturation    = 3.0
      value         = 10.0
      speed         = 20.0
      autospeed     = 0.0 
      interpolation = 0
      threshold     = 0.0
      self.scan_v          =  0.0
      self.scan_h          =  0.0
      self.scan_threshold  =  0
      self.scan_range      =  0.0
    elif self.movie_preset == 2:     #preset action
      saturation    = 3.0
      value         = 10.0
      speed         = 80.0
      autospeed     = 0.0  
      interpolation = 0
      threshold     = 0.0
      self.scan_v          =  0.0
      self.scan_h          =  0.0
      self.scan_threshold  =  0
      self.scan_range      =  0.0
    elif self.movie_preset == 3:     #preset disabled
      saturation    = 0.0
      value         = 0.0
      speed         = 0.0
      autospeed     = 0.0  
      interpolation = 0
      threshold     = 0.0
      self.scan_v          =  0.0
      self.scan_h          =  0.0
      self.scan_threshold  =  0
      self.scan_range      =  0.0
    elif self.movie_preset == 0:     #custom
      saturation      =  self.movie_saturation
      value           =  self.movie_value
      speed           =  self.movie_speed
      autospeed       =  self.movie_autospeed
      interpolation   =  self.movie_interpolation
      threshold       =  self.movie_threshold
      self.scan_v          =  self.movie_scan_v
      self.scan_h          =  self.movie_scan_h
      self.scan_threshold  =  self.movie_scan_threshold
      self.scan_range      =  self.movie_scan_range
    return (saturation,value,speed,autospeed,interpolation,threshold)

  #handle boblight configuration from the "TVShows" category
  #returns the new settings
  def setupForTVShow(self):
    log('settings() - setupForTVShow')
  
    if self.tvshow_preset == 1:       #preset smooth
      saturation    = 3.0
      value         = 10.0
      speed         = 20.0
      autospeed     = 0.0 
      interpolation = 0
      threshold     = 0.0
      self.scan_v          =  0.0
      self.scan_h          =  0.0
      self.scan_threshold  =  0
      self.scan_range      =  0.0
    elif self.tvshow_preset == 2:     #preset action
      saturation    = 3.0
      value         = 10.0
      speed         = 80.0
      autospeed     = 0.0  
      interpolation = 0
      threshold     = 0.0
      self.scan_v          =  0.0
      self.scan_h          =  0.0
      self.scan_threshold  =  0
      self.scan_range      =  0.0
    elif self.tvshow_preset == 3:     #preset disabled
      saturation    = 0.0
      value         = 0.0
      speed         = 0.0
      autospeed     = 0.0  
      interpolation = 0
      threshold     = 0.0
      self.scan_v          =  0.0
      self.scan_h          =  0.0
      self.scan_threshold  =  0
      self.scan_range      =  0.0
    elif self.tvshow_preset == 0:     #custom
      saturation      =  self.tvshow_saturation
      value           =  self.tvshow_value
      speed           =  self.tvshow_speed
      autospeed       =  self.tvshow_autospeed
      interpolation   =  self.tvshow_interpolation
      threshold       =  self.tvshow_threshold
      self.scan_v          =  self.tvshow_scan_v
      self.scan_h          =  self.tvshow_scan_h
      self.scan_threshold  =  self.tvshow_scan_threshold
      self.scan_range      =  self.tvshow_scan_range
    return (saturation,value,speed,autospeed,interpolation,threshold)

  #handle boblight configuration from the "LiveTV" category
  #returns the new settings
  def setupForLiveTV(self):
    log('settings() - setupForLiveTV')
  
    if self.livetv_preset == 1:       #preset smooth
      saturation    = 3.0
      value         = 10.0
      speed         = 20.0
      autospeed     = 0.0 
      interpolation = 0
      threshold     = 0.0
      self.scan_v          =  0.0
      self.scan_h          =  0.0
      self.scan_threshold  =  0
      self.scan_range      =  0.0
    elif self.livetv_preset == 2:     #preset action 
      saturation    = 3.0
      value         = 10.0
      speed         = 80.0
      autospeed     = 0.0  
      interpolation = 0
      threshold     = 0.0
      self.scan_v          =  0.0
      self.scan_h          =  0.0
      self.scan_threshold  =  0
      self.scan_range      =  0.0
    elif self.livetv_preset == 3:     #preset disabled
      saturation    = 0.0
      value         = 0.0
      speed         = 0.0
      autospeed     = 0.0  
      interpolation = 0
      threshold     = 0.0
      self.scan_v          =  0.0
      self.scan_h          =  0.0
      self.scan_threshold  =  0
      self.scan_range      =  0.0
    elif self.livetv_preset == 0:     #custom
      saturation      =  self.livetv_saturation
      value           =  self.livetv_value
      speed           =  self.livetv_speed
      autospeed       =  self.livetv_autospeed
      interpolation   =  self.livetv_interpolation
      threshold       =  self.livetv_threshold
      self.scan_v          =  self.livetv_scan_v
      self.scan_h          =  self.livetv_scan_h
      self.scan_threshold  =  self.livetv_scan_threshold
      self.scan_range      =  self.livetv_scan_range
    return (saturation,value,speed,autospeed,interpolation,threshold)

  #handle boblight configuration from the "files" category
  #returns the new settings
  def setupForFiles(self):
    log('settings() - setupForFiles')
  
    if self.files_preset == 1:       #preset smooth
      saturation    = 3.0
      value         = 10.0
      speed         = 20.0
      autospeed     = 0.0 
      interpolation = 0
      threshold     = 0.0
      self.scan_v          =  0.0
      self.scan_h          =  0.0
      self.scan_threshold  =  0
      self.scan_range      =  0.0
    elif self.files_preset == 2:     #preset action
      saturation    = 3.0
      value         = 10.0
      speed         = 80.0
      autospeed     = 0.0  
      interpolation = 0
      threshold     = 0.0
      self.scan_v          =  0.0
      self.scan_h          =  0.0
      self.scan_threshold  =  0
      self.scan_range      =  0.0
    elif self.files_preset == 3:     #preset disabled
      saturation    = 0.0
      value         = 0.0
      speed         = 0.0
      autospeed     = 0.0  
      interpolation = 0
      threshold     = 0.0
      self.scan_v          =  0.0
      self.scan_h          =  0.0
      self.scan_threshold  =  0
      self.scan_range      =  0.0
    elif self.files_preset == 0:     #custom
      saturation      =  self.files_saturation
      value           =  self.files_value
      speed           =  self.files_speed
      autospeed       =  self.files_autospeed
      interpolation   =  self.files_interpolation
      threshold       =  self.files_threshold
      self.scan_v          =  self.files_scan_v
      self.scan_h          =  self.files_scan_h
      self.scan_threshold  =  self.files_scan_threshold
      self.scan_range      =  self.files_scan_range
    return (saturation,value,speed,autospeed,interpolation,threshold)
    
  #handle boblight configuration from the "MusicVideo" category
  #returns the new settings
  def setupForMusicVideo(self):
    log('settings() - setupForMusicVideo')
  
    if self.music_preset == 1:       #preset Ballad
      saturation    = 3.0
      value         = 10.0
      speed         = 20.0  
      autospeed     = 0.0
      interpolation = 1
      threshold     = 0.0
      self.scan_v          =  0.0
      self.scan_h          =  0.0
      self.scan_threshold  =  0
      self.scan_range      =  0.0
    elif self.music_preset == 2:     #preset Rock
      saturation    = 3.0
      value         = 10.0
      speed         = 80.0
      autospeed     = 0.0  
      interpolation = 0
      threshold     = 0.0
      self.scan_v          =  0.0
      self.scan_h          =  0.0
      self.scan_threshold  =  0
      self.scan_range      =  0.0
    elif self.music_preset == 3:     #preset disabled
      saturation    = 0.0
      value         = 0.0
      speed         = 0.0
      autospeed     = 0.0  
      interpolation = 0
      threshold     = 0.0
      self.scan_v          =  0.0
      self.scan_h          =  0.0
      self.scan_threshold  =  0
      self.scan_range      =  0.0
    elif self.music_preset == 0:     #custom
      saturation      =  self.music_saturation
      value           =  self.music_value
      speed           =  self.music_speed
      autospeed       =  self.music_autospeed
      interpolation   =  self.music_interpolation
      threshold       =  self.music_threshold    
      self.scan_v          =  self.music_scan_v
      self.scan_h          =  self.music_scan_h
      self.scan_threshold  =  self.music_scan_threshold
      self.scan_range      =  self.music_scan_range
    return (saturation,value,speed,autospeed,interpolation,threshold)
  
  #handle boblight configuration from the "other" category
  #returns the new settings
  def setupForOther(self):
    log('settings() - setupForOther')
  # FIXME don't use them for now - reactivate when boblight works on non rendered scenes (e.x. menu)
  #  saturation      =  float(__addon__.getSetting("other_saturation"))
  #  value           =  float(__addon__.getSetting("other_value"))
  #  speed           =  float(__addon__.getSetting("other_speed"))
  #  autospeed       =  float(__addon__.getSetting("other_autospeed"))
  #  interpolation   =  __addon__.getSetting("other_interpolation") == "true"
  #  threshold       =  float(__addon__.getSetting("other_threshold"))
    self.scan_v          =  0.0
    self.scan_h          =  0.0
    self.scan_threshold  =  0
    self.scan_range      =  0.0
    return self.setupForStatic()
  
  #handle boblight configuration for static lights
  #returns the new settings
  def setupForStatic(self):
    log('settings() - setupForStatic')
    saturation    = 4.0
    value         = 1.0
    speed         = 50.0
    autospeed     = 0.0 
    interpolation = 1
    threshold     = 0.0
    self.scan_v          =  0.0
    self.scan_h          =  0.0
    self.scan_threshold  =  0
    self.scan_range      =  0.0
    return (saturation,value,speed,autospeed,interpolation,threshold)

  #handle all settings according to the static bg light
  #this is used until category "other" can do real boblight
  #when no video is rendered

  def handleStaticBgSettings(self):
    log('settings() - handleStaticBgSettings')
    if (self.category == "static" and                 # only for 'static' category
            self.other_static_bg):                    # only if we want it displayed on static

      bob.bob_set_priority(128)                       # allow lights to be turned on
      rgb = (c_int * 3)(self.other_static_red,
                        self.other_static_green,
                        self.other_static_blue)
      ret = bob.bob_set_static_color(byref(rgb))
      self.staticBobActive = True
    else:
      bob.bob_set_priority(255)
      self.staticBobActive = False

  #handles the boblight configuration of all categorys
  #and applies changed settings to boblight
  #"movie","musicvideo","files","livetv","tvshows","other and "static"
  def handleGlobalSettings(self):
    log('settings() - handleGlobalSettings')
    if (self.current_option != self.category) or self.force_update:
      #call the right setup function according to category
      #switch case in python - dictionary with function pointers
      option = { "movie"      : self.setupForMovie,
                 "tvshow"     : self.setupForTVShow,
                 "livetv"     : self.setupForLiveTV,
                 "files"      : self.setupForFiles,
                 "musicvideo" : self.setupForMusicVideo,
                 "other"      : self.setupForOther,
                 "static"     : self.setupForStatic, 
      }
      saturation,value,speed,autospeed,interpolation,threshold = option[self.category]()
      for opt in OPTS:
        ret = bob.bob_setoption("%s    %s" % (opt,str(locals()[opt])))
        log("changed %s    to %s ret:  %s" % (opt,str(locals()[opt]),ret))          
      self.current_option = self.category
      self.force_update = False
  
  #handle change of category we are calling
  def handleCategory(self, category):
    log('settings() - handleCategory(%s)' % category)
    self.category = category
    self.handleGlobalSettings()
    self.handleStaticBgSettings()

  def handleStereoscopic(self, isStereoscopic):
    log('settings() - handleStereoscopic(%s) - disableon3d (%s)' % (isStereoscopic, self.bobdisableon3d))
    if self.bobdisableon3d and isStereoscopic:
      log('settings()- disable due to 3d')
      self.bobdisable = True
    else:
      self.resetBobDisable()

  def bob_init(self):
    if self.run_init:
      log('bob_init')
      nrLights = bob.bob_getnrlights()
      log("settings() - Found %s lights" % str(nrLights))
      for i in range(nrLights):
        lightname = bob.bob_getlightname(i)
        log("settings() - Light[%.2d] - %s" % (i+1, lightname))
      
      self.handleGlobalSettings()
      bob.bob_set_priority(128)           # allow lights to be turned on, we will switch them off
                                          # in 'handleStaticBgSettings()' if they are not needed
      if self.other_misc_initialflash:
        for i in range(len(BLING)):
          rgb = (c_int * 3)(BLING[i][0],BLING[i][1],BLING[i][2])
          bob.bob_set_static_color(byref(rgb))
          xbmc.sleep(1000)
      else:
        rgb = (c_int * 3)(0,0,0)
        bob.bob_set_static_color(byref(rgb))
      self.run_init = False
      xbmc.sleep(500)
    return True  

  def is_working_time(self):

  #If from and do are the same then it is always enabled
    if self.enabledfrom == self.enabledto:
      return True

  #Get current time
    tmNow  = datetime.datetime.now()

  #Adjust current time to match with from and to
    tmFrom = self.enabledfrom.replace(year = tmNow.year, month = tmNow.month, day = tmNow.day)
    tmTo   = self.enabledto.replace(year = tmNow.year, month = tmNow.month, day = tmNow.day)

  #Compare
    if tmTo < tmFrom:
      return (tmNow >= tmFrom or tmNow <= tmTo)

    if tmTo > tmFrom:
      return (tmNow >= tmFrom and tmNow <= tmTo)

  #Impossible
    return False