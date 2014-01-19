#!/usr/bin/env python
import wx
import opencv.cv as cv
import opencv.highgui as gui


class CvMovieFrame(wx.Frame):
    TIMER_PLAY_ID = 101
    def __init__(self, parent):        

        wx.Frame.__init__(self, parent, -1,)        

        sizer = wx.BoxSizer(wx.VERTICAL)         

        self.capture = gui.cvCreateCameraCapture(0)
        frame = gui.cvQueryFrame(self.capture)
        cv.cvCvtColor(frame, frame, cv.CV_BGR2RGB)

        self.SetSize((frame.width + 300, frame.height + 100))

        self.bmp = wx.BitmapFromBuffer(frame.width, frame.height, frame.imageData)
        self.displayPanel= wx.StaticBitmap(self, -1, bitmap=self.bmp)
        sizer.Add(self.displayPanel, 0, wx.ALL, 10)

        self.shotbutton = wx.Button(self,-1, "Shot")
        sizer.Add(self.shotbutton,-1, wx.GROW)

        self.retrybutton = wx.Button(self,-1, "Retry")
        sizer.Add(self.retrybutton,-1, wx.GROW)     
        self.retrybutton.Hide()   

        #events
        self.Bind(wx.EVT_BUTTON, self.onShot, self.shotbutton)
        self.Bind(wx.EVT_BUTTON, self.onRetry, self.retrybutton)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.playTimer = wx.Timer(self, self.TIMER_PLAY_ID)
        wx.EVT_TIMER(self, self.TIMER_PLAY_ID, self.onNextFrame)

        self.fps = 8;
        self.SetSizer(sizer)
        sizer.Layout()
        self.startTimer()        

    def startTimer(self):
        if self.fps!=0: self.playTimer.Start(1000/self.fps)#every X ms
        else: self.playTimer.Start(1000/15)#assuming 15 fps        

    def onRetry(self, event):
        frame = gui.cvQueryFrame(self.capture)
        cv.cvCvtColor(frame, frame, cv.CV_BGR2RGB)
        self.bmp = wx.BitmapFromBuffer(frame.width, frame.height, frame.imageData)
        self.startTimer()
        self.shotbutton.Show()
        self.retrybutton.Hide()
        self.hasPicture = False
        self.Layout()
        event.Skip()    

    def onShot(self, event):
        frame = gui.cvQueryFrame(self.capture)
        self.playTimer.Stop()
        gui.cvSaveImage("foo.png", frame)        

        self.hasPicture = True
        self.shotbutton.Hide()
        self.retrybutton.Show()
        self.Layout()
        event.Skip()

    def onClose(self, event):
        try:
            self.playTimer.Stop()
        except:
            pass

        self.Show(False)
        self.Destroy()      

    def onPaint(self, evt):
        if self.bmp:
            self.displayPanel.SetBitmap(self.bmp)
        evt.Skip()

    def onNextFrame(self, evt):

        frame = gui.cvQueryFrame(self.capture)
        if frame:
            cv.cvCvtColor(frame, frame, cv.CV_BGR2RGB)
            self.bmp = wx.BitmapFromBuffer(frame.width, frame.height, frame.imageData)
            self.Refresh()        
        evt.Skip()

if __name__=="__main__":
    app = wx.App()
    f = CvMovieFrame(None)
    f.Centre()
    f.Show(True)
    app.MainLoop()