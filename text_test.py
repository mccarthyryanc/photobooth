import wx

app=wx.PySimpleApp()
frame=wx.Frame(None)
text=wx.StaticText(frame, label="Colored text", size=(50,50))
text.SetForegroundColour((255,0,0)) # set text color
# text.SetBackgroundColour((0,0,255)) # set text back color
frame.Show(True)
app.MainLoop()