#!/usr/bin/env python
# encoding: utf-8
"""
screengrab.py
 Based on creation by Alex Snet on 2011-10-10.
Copyright (c) 2011 CodeTeam. All rights reserved.
"""
 import sys
 from PIL import Image
 class screencap:
    def __init__(self):
        self.screen = None
        try:
            import PyQt4
            # TODO: Qt5
        except ImportError:
            pass
        else:
            self.screen = self.getScreenByQt4
            from PyQt4.QtGui import QApplication
            self.app = QApplication(sys.argv)
            return
         try:
            import Xlib
        except ImportError:
            pass
        else:
            self.screen = self.getScreenByXlib
            from Xlib import display, X
            dsp = display.Display()
            self.root = dsp.screen().root
            geom = self.root.get_geometry()
            self.width = geom.width
            self.height = geom.height
            self.pixmap = X.ZPixmap
            return
         try:
            import ImageGrab
        except ImportError:
            pass
        else:
            self.screen = self.getScreenByPIL
            return
         try:
            import wx
        except ImportError:
            pass
        else:
            self.screen = self.getScreenByWx
            return
     def getScreenByQt4(self):
        from PyQt4.Qt import QBuffer
        import StringIO
        from PyQt4.Qt import QIODevice
        from PyQt4.QtGui import QPixmap
        from PyQt4.QtGui import QApplication
        buffer = QBuffer()
        rootwin = QApplication.desktop().winId()
        buffer.open(QIODevice.ReadWrite)
        strio = StringIO.StringIO()
        QPixmap.grabWindow(rootwin).save(buffer, 'jpg')
        strio.write(buffer.data())
        strio.seek(0)
        buffer.close()
        return Image.open(strio)
     def getScreenByPIL(self):
        import ImageGrab
        img = ImageGrab.grab()
        return img
     def getScreenByWx(self):
        import wx
        wx.App()  # Need to create an App instance before doing anything
        screen = wx.ScreenDC()
        size = screen.GetSize()
        bmp = wx.EmptyBitmap(size[0], size[1])
        mem = wx.MemoryDC(bmp)
        mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
        del mem  # Release bitmap
        #bmp.SaveFile('screenshot.png', wx.BITMAP_TYPE_PNG)
        myWxImage = wx.ImageFromBitmap( myBitmap )
        PilImage = Image.new( 'RGB', (myWxImage.GetWidth(), myWxImage.GetHeight()) )
        PilImage.fromstring( myWxImage.GetData() )
        return PilImage
     def getScreenByXlib(self):
        raw = self.root.get_image(0, 0, self.width, self.height, self.pixmap, 0xffffffff)
        image = Image.fromstring("RGB", (self.width, self.height), raw.data, "raw", "BGRX")
        return image
 if __name__ == '__main__':
    s = screencap()
    screen = s.screen()
    screen.show()