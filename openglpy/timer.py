
import wx
import time

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="With wx.Timer", size=(500,500))

        #### Variables
        self.will_continue = True
        self.i = 0
        self.total = 5
        self.mili = 1000

        #### Widgets
        # Parent panel
        self.panel = wx.Panel(self)
        # Button
        self.button  = wx.Button(self.panel, label="Start", pos=(50, 50))
        self.button2 = wx.Button(self.panel, label="Button", pos=(50 ,100))

        #### Timer Notice that wx.Timer is own by the frame itself
        self.timer = wx.Timer(self)

        #### Bind
        self.button.Bind(wx.EVT_BUTTON, self.OnStart)
        self.Bind(wx.EVT_TIMER, self.OnCheck, self.timer)

    def OnStart(self, event):
        ## OnStart, disable the button and change its label and start the timer.
        ## Notice with Button that the GUI remain responsive
        ## while the timer runs
        if self.will_continue:
            print(self.i)
            print(time.ctime())
            self.button.SetLabel("Running")
            self.button.Disable()
            self.timer.Start(self.mili)
        ## When finish waiting reset everything so the start button can run 
        ## again and stop the timer
        else:
            self.timer.Stop()
            self.button.SetLabel("Start")
            self.button.Enable()
            self.will_continue = True
            self.i = 0            

    def OnCheck(self, event):
        print('OC')
        self.i += 1 
        if self.i > self.total:
            self.will_continue = False
        else:
            pass
        self.OnStart(event)


# Run the program
if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()

