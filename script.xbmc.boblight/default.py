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
import xbmc
import xbmcaddon
import xbmcgui
import os

__addon__      = xbmcaddon.Addon()
__cwd__        = __addon__.getAddonInfo('path')
__scriptname__ = __addon__.getAddonInfo('name')
__version__    = __addon__.getAddonInfo('version')
__icon__       = __addon__.getAddonInfo('icon')
__ID__         = __addon__.getAddonInfo('id')
__language__   = __addon__.getLocalizedString

__profile__    = xbmc.translatePath( __addon__.getAddonInfo('profile') )
__resource__   = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'lib' ) )

sys.path.append (__resource__)

from settings import *
from tools import *

log( "[%s] - Version: %s Started" % (__scriptname__,__version__))

capture_width  = 32
capture_height = 32
settings       = settings()
capture        = xbmc.RenderCapture()
useLegacyApi   = True

class MyPlayer( xbmc.Player ):
  def __init__( self, *args, **kwargs ):
    xbmc.Player.__init__( self )
    self.playing = False
    log('MyPlayer - init')
        
  def onPlayBackStopped( self ):
    self.playing = False
    myPlayerChanged( 'stop' )

  def onPlayBackPaused( self ):
    myPlayerChanged( 'paused' )

  
  def onPlayBackEnded( self ):
    self.playing = False
    myPlayerChanged( 'stop' )     
  
  def onPlayBackStarted( self ):
    self.playing = True
    myPlayerChanged( 'start' )
    if not useLegacyApi:
      capture.capture(capture_width, capture_height)
  
  def isPlaying( self ):
    return self.playing

class MyMonitor( xbmc.Monitor ):
  def __init__( self, *args, **kwargs ):
    xbmc.Monitor.__init__( self )
    log('MyMonitor - init')
        
  def onSettingsChanged( self ):
    settings.start()
    if not settings.reconnect:
      check_state()
      
  def onScreensaverDeactivated( self ):
    settings.setScreensaver(False)
      
  def onScreensaverActivated( self ):    
    settings.setScreensaver(True)

class Main():
  def __init__( self, *args, **kwargs ):
    self.warning   = 0
  
  def connectBoblight(self):
    bob.bob_set_priority(255)
    
    if settings.hostip == None:
      log("connecting to local boblightd")
    else:
      log("connecting to boblightd %s:%s" % (settings.hostip, str(settings.hostport)))
  
    ret = bob.bob_connect(settings.hostip, settings.hostport)
  
    if not ret:
      log("connection to boblightd failed: %s" % bob.bob_geterror())
      if self.warning < 3 and settings.other_misc_notifications:
        xbmc.executebuiltin("XBMC.Notification(%s,%s,%s,%s)" % (__scriptname__,
                                                                localize(32500),
                                                                750,
                                                                __icon__))
        self.warning += 1
      settings.reconnect = True
      settings.run_init = True
      settings.force_update = True
      return False
    else:
      self.warning = 0
      if settings.other_misc_notifications:
        xbmc.executebuiltin("XBMC.Notification(%s,%s,%s,%s)" % (__scriptname__,
                                                                localize(32501),
                                                                750,
                                                                __icon__))
      log("connected to boblightd")
      bob.bob_set_priority(128)  
      return True
  
  def startup(self):
    platform = get_platform()
    libpath  = get_libpath(platform)
    loaded   = bob.bob_loadLibBoblight(libpath,platform)
  
    if loaded == 1:                                #libboblight not found                                               
      if platform == 'linux':
        xbmcgui.Dialog().ok(__scriptname__,
                            localize(32504),
                            localize(32505),
                            localize(32506))
      
      else:
        # ask user if we should fetch the lib for osx, ios, android and windows
        if xbmcgui.Dialog().yesno(__scriptname__,
                                  localize(32504),
                                  localize(32509)):
          tools_downloadLibBoblight(platform,settings.other_misc_notifications)
          loaded = bob.bob_loadLibBoblight(libpath,platform)
      
        
    elif loaded == 2:         #no ctypes available
      xbmcgui.Dialog().ok(__scriptname__,
                          localize(32507),
                          localize(32508))
  
    return loaded  

def check_state(): 
  if xbmc.Player().isPlaying():
    state = 'start'
  else:
    state = 'stop'  
  myPlayerChanged( state )    

def myPlayerChanged(state):
  log('PlayerChanged(%s)' % state)
  xbmc.sleep(1000)
  if state == 'stop':
    ret = "static"
  else:
    ret = "movie"
    # Possible Videoplayer options: files, movies, episodes, musicvideos, livetv
    if xbmc.getCondVisibility("Player.HasVideo()"):
      if xbmc.getCondVisibility('VideoPlayer.Content(movies)'):
        ret = "movie"
      elif xbmc.getCondVisibility("VideoPlayer.Content(musicvideos)"):
        ret = "musicvideo"
      elif xbmc.getCondVisibility("VideoPlayer.Content(episodes)"):
        ret = "tvshow"
      elif xbmc.getCondVisibility("VideoPlayer.Content(livetv)"):
        ret = "livetv"
      elif xbmc.getCondVisibility("VideoPlayer.Content(files)"):
        ret = "files"

      #handle overwritten category
      if settings.overwrite_cat:                  # fix his out when other isn't
        if settings.overwrite_cat_val == 0:       # the static light anymore
          ret = "movie"
        elif settings.overwrite_cat_val == 1:
          ret = "musicvideo"
        elif settings.overwrite_cat_val == 2:
          ret = "tvshow"
        elif settings.overwrite_cat_val == 3:
          ret = "livetv"
        elif settings.overwrite_cat_val == 4:
          ret = "files"

    elif xbmc.getCondVisibility("Player.HasAudio()"):
      ret = "static"
    else:
      ret = "movie"

  settings.handleCategory(ret)
  settings.handleStereoscopic(xbmc.getInfoLabel("System.StereoscopicMode") != "0")

def run_boblight():
  main = Main()
  xbmc_monitor   = MyMonitor()
  player_monitor = MyPlayer()
  player_monitor.playing = xbmc.Player().isPlaying()
  if main.startup() == 0:
    if useLegacyApi:
      capture.capture(settings.frame_capture_width, settings.frame_capture_height, xbmc.CAPTURE_FLAG_CONTINUOUS)

    while not xbmc.abortRequested:
      xbmc.sleep(settings.frame_capture_interval)
      if not settings.bobdisable:
        if not settings.is_working_time():
          bob.bob_set_priority(255)
          continue

        if not bob.bob_ping() or settings.reconnect:
          if not main.connectBoblight():
            continue
          if settings.bob_init():
            check_state()
          settings.reconnect = False
          
        if not settings.staticBobActive:
          startReadOut = False
          if useLegacyApi:
            capture.waitForCaptureStateChangeEvent(1000)
            if capture.getCaptureState() == xbmc.CAPTURE_STATE_DONE and player_monitor.isPlaying():
              startReadOut = True 
          else:
            pixels = capture.getImage(1000)
            if len(pixels) > 0 and player_monitor.isPlaying():
              startReadOut = True

          if startReadOut:
            width = capture.getWidth();
            if width == 0:
              return
            height = capture.getHeight();
            if useLegacyApi:
              pixels = capture.getImage(1000)

            pxl_width = width * 4
            range_x_min = int(width / 2 * (1 - settings.scan_range)) * 4
            range_x_max = int(width / 2 * (1 + settings.scan_range)) * 4
            range_y_min = int(height / 2 * (1 - settings.scan_range)) * pxl_width
            range_y_max = int(height / 2 * (1 + settings.scan_range)) * pxl_width
            found = False
            for yc in range(0, int(height * settings.scan_v) * pxl_width, pxl_width):
              for xi in range (range_x_min + yc, range_x_max + yc, 4):
                if pixels[xi] > settings.scan_threshold or pixels[xi + 1] > settings.scan_threshold or pixels[xi + 2] > settings.scan_threshold:
                  found = True
                  break
              if found:
                break
            yc = int(yc / pxl_width)
            found = False
            for xc in range(0, int(width * settings.scan_h) * 4, 4):
              for yi in range (range_y_min + xc, range_y_max + xc , pxl_width):
                if pixels[yi] > settings.scan_threshold or pixels[yi + 1] > settings.scan_threshold or pixels[yi + 2] > settings.scan_threshold:
                  found = True
                  break
              if found:
                break
            xc = int(xc / 4)
            bob.bob_setscanrange(width - xc * 2, height - yc * 2)
            rgb = (c_int * 3)()
            for y in range(yc, height - yc):
              for x in range(xc, width - xc):
                pxl = (y * width + x) * 4
                rgb[0] = pixels[pxl + 2]
                rgb[1] = pixels[pxl + 1]
                rgb[2] = pixels[pxl]
                bob.bob_addpixelxy(x - xc, y - yc, byref(rgb))
            bob.bob_set_priority(128)
            if not bob.bob_sendrgb():
              log("error sending values: %s" % bob.bob_geterror())
              return   
                        
      else:
        log('boblight disabled in Addon Settings')
        bob.bob_set_priority(255)
        continue

  del main                  #cleanup
  del player_monitor
  del xbmc_monitor

def localize(id):
    return __language__(id).encode('utf-8','ignore')

if ( __name__ == "__main__" ):
  try:
    capture.getCaptureState()
  except AttributeError:
    useLegacyApi = False
  run_boblight()
  bob.bob_set_priority(255) # we are shutting down, kill the LEDs     
  bob.bob_destroy()


