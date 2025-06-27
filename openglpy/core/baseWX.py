import sys
import datetime
import time

import wx
from wx import glcanvas 

from core.inputWX import Input

class Base(object):
    def __init__(self, parent, screenSize=[640,640], titlebartext='Graphics Window'):
        print(f'BaseWX: parent={parent}')
#        self.kwargs={}
#        for kwarg in sys.argv[1:]:
#            k,v=kwarg.split('=')
#            self.kwargs[k]=float(v)
#        print(f'BaseWX: self.kwargs= {self.kwargs}')

        self.parent=parent
        self.init=False
        self.paint_calls = 0
        self.paint_dbg_cnt = 0
        self.last_loop= ''
        self.deltaTime= 1/60
        #self.deltaTime= 1/4
        self.fpsperiod_ms= self.deltaTime * 1000 # 0.0166666

        self.glcanv = glcanvas.GLCanvas(parent, size=screenSize)

        ctxAttrs = wx.glcanvas.GLContextAttrs()
        ctxAttrs.CoreProfile().OGLVersion(4, 1).Robust().ResetIsolation().DebugCtx().EndList()
        self.context = glcanvas.GLContext(self.glcanv,ctxAttrs=ctxAttrs)

        dispAttrs = glcanvas.GLAttributes()
        dispAttrs.PlatformDefaults().MinRGBA(8, 8, 8, 8).DoubleBuffer().Depth(32).EndList()

        self.glcanv.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.glcanv.Bind(wx.EVT_PAINT           , self.OnPaint          )
 
        self.running= True

        self.clock= datetime.datetime #pygame.time.Clock()

        self.input = Input(self.glcanv)

        self.time= 0
        self.runcount=0

    def Destroy(self):
        print('OpenGl:baseWX.Destroy')
        if self.glcanv.HasCapture():
            self.glcanv.ReleaseMouse()
        self.glcanv.Destroy()

    def OnEraseBackground(self, event):
        pass # Do nothing, to avoid flashing on MSW.

    def initialize(self):
        pass

    def update(self):
        print('update')
        pass

    def run(self):
        self.runcount+=1
        if self.runcount %100 == 0:
            print(f'baseWx:run runcount={self.runcount}')

        try:
            self.glcanv
        except:
            return
        ## STARTUP ##
        need_refresh= 0x0
        if not self.glcanv.IsShownOnScreen():
            print('!!! NotYetOnScreen !!!' )
            wx.CallLater( 500, self.run)
            return

        if not self.init:
            print('\n\n!!! Initialize !!!')
            self.initialize()
            self.init = True
            self.startTime= self.clock.now()
            print('!!! Initialize DONE !!!\n\n')
            need_refresh |= 0x2

        # while self.running:
        self.loopClock= self.clock.now()

        ## process input ##
        need_refresh |= self.input.update()
        if self.input.quit:
            print('baseWX:run GOT QUIT\n')
            self.running= False
            
        # increment run time app has been running
        self.time += self.deltaTime

        ## update ##
        self.update()

        if not self.running:
            sys.exit()

        if need_refresh:
            #print(f'Refresh: {need_refresh:#06x}')
            self.glcanv.Refresh()

        elap= self.clock.now() - self.loopClock
        elapts= elap.total_seconds()
        timeToSleep= max(0, (self.fpsperiod_ms - elapts ))
        #print(f'now:{self.clock.now()}  elapts:{elapts}  tts:{timeToSleep}')

        wx.CallLater( int(timeToSleep), self.run )


    # OnPaint called by .Refresh and internal wx events
    # called a lot - so keep it tight
    def OnPaint(self, event, loop=False):
        #print(f'baseWx:OnPaint {event}')
        if not self.glcanv.IsShownOnScreen():
            return

        #dc = wx.PaintDC(self.glcanv)
        #print('VERSION OP2: ', glGetString(GL_VERSION))#self.context.IsOK() )
        self.glcanv.SetCurrent(self.context)
        self.glcanv.SwapBuffers()


