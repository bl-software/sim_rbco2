import wx

class Input(object):
    def __init__(self,canvas):
        self.canvas= canvas

        # has user quit ?
        self.quit= False
        self.need_refresh=0x0

        # lists to store keystates
        # down, up: discrete event, 1 iteration
        # pressed: continuous even betwee down and up
        self.keyDownSet    = set()
        self.keyPressedList = []

        self.mx_down = self.mx_delta = 0
        self.my_down = self.my_delta = 0

        self.canvas.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown  )
        self.canvas.Bind(wx.EVT_LEFT_UP  , self.OnMouseUp    )
        self.canvas.Bind(wx.EVT_MOTION   , self.OnMouseMotion)

        self.canvas.Bind(wx.EVT_KEY_DOWN , self.OnKeyDown    )
        self.canvas.Bind(wx.EVT_KEY_UP   , self.OnKeyUp      )


    def update(self):
        #print('inputUpdate')
        if self.keyPressedList:
            print(f'    pressedlist {self.keyPressedList}')
        #if self.isKeyPressed( ord('B'), consume=True ):
        nr= self.need_refresh
        self.need_refresh= 0x0
        return nr

    def isKeyDown(self, keyCode):
        return keyCode in self.keyDownSet
    def isKeyUp(self, keyCode):
        return keyCode not in self.keyDownSet

    def isKeyPressed(self, keyCode, consume=True):
        if consume:
            try:
                self.keyPressedList.remove(keyCode)
                print(f'isKeyPressed {keyCode} - comsuming')
                return True
            except ValueError as e:
                print(f'isKeyPressed: {keyCode} {e}')
                return False
        else:
            return keyCode in self.keyPressedList

    def consume_pressed_key(self):
        try:
            keyCode= self.keyPressedList.pop(0)
            l= len(self.keyPressedList) # Remaining Len
            print(f'consume_pressed_key: popped {keyCode}')
            return keyCode, l
        except IndexError:
            return -1, None

    #def clearKeyPressed(self, keyCode):
    #    self.keyPressedList = [ v for v in self.keyPressedList if v != keyCode ]

    def OnKeyDown(self, e):
        self.need_refresh=0x111
        keyCode= e.GetUnicodeKey()
        #print(f'OnKeyDown -->{keyCode}<-- --->', '%c'%keyCode)
        if keyCode != wx.WXK_NONE:
            if keyCode == 27: # ESC
                self.quit=True
                return
            self.keyDownSet.add( keyCode )
            self.keyPressedList.append( keyCode )
            #print(f'     downlist {self.keyDownSet}')
            #print(f'  pressedlist {self.keyPressedList}')

    def OnKeyUp(self, e):
        self.need_refresh=0x112
        keyCode= e.GetUnicodeKey()
        #print(f'OnKeyUp -->{keyCode}<--')
        if keyCode != wx.WXK_NONE:
            try:
                self.keyDownSet.remove( keyCode )
            except KeyError:
                pass
            #print(f'     downlist {self.keyDownSet}')
            #print(f'  pressedlist {self.keyPressedList}')

#    def consume_mouse_movement(self):
#        try:
#            return self.mdragList.pop(0), len(self.mdragList) # Remaining Len
#        except IndexError:
#            return (None,None), None

    def OnMouseDown(self, event):
        self.need_refresh=0x101
        #print('OMDown')
        if self.canvas.HasCapture():
            self.canvas.ReleaseMouse()
        self.canvas.CaptureMouse()
        self.mx_down, self.my_down = event.GetPosition()
        #print('DownXY:',self.mx_down, self.my_down)
        #event.Skip()

    def OnMouseUp(self, event):
        self.need_refresh=0x103
        #print('OMUp')
        if self.canvas.HasCapture():
            self.canvas.ReleaseMouse()
        #self.mdragList.append( (self.mx_delta, self.my_delta) )
        self.mx_delta=0
        self.my_delta=0
        #event.Skip()

    def mmot(self):
        return (self.mx_delta, self.my_delta)
    def OnMouseMotion(self, event):
        self.need_refresh=0x102
        dr= event.Dragging()
        lid= event.LeftIsDown()
        #print(f'Mot Drag>{dr}<  LIsDown:{lid}  E:{event} C:{self.canvas}')
        if dr and lid:
            _mx_mot, _my_mot = event.GetPosition()
            #print('MMoveXY',_mx_mot, _my_mot)
            self.mx_delta= _mx_mot - self.mx_down
            self.my_delta= _my_mot - self.my_down
            self.canvas.Refresh(False)
            #print('MMoveDeltaXY',self.mx_delta, self.my_delta)

            #TODO --- DO I NEEDT HIS REFRESH ???
            self.canvas.Refresh(False)
        #event.Skip()


