#-*- coding:utf-8 -*-
import wx
import webbrowser
from utils.rand_select import rand_sample
cartoon_size = (cartoon_width,cartoon_high) = (256,256)

class transient_popup(wx.PopupTransientWindow):
    def __init__(self,parent,style):
        wx.PopupTransientWindow.__init__(self,parent,style)
        panel = wx.Panel(self)
        panel.SetBackgroundColour('#66ccff')
        
        st = wx.StaticText(panel,-1,label='你想抽取几个学生？')
        spin = wx.SpinCtrl(panel,-1,'上下点击选择抽取个数')
        self.spin = spin
        self.Bind(wx.EVT_SPINCTRL,self.onspin,spin)
        btn = wx.Button(panel,-1,'召唤')
        btn.Bind(wx.EVT_BUTTON,self.pressed)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(st, 0, wx.ALL, 5)
        sizer.Add(btn, 0, wx.ALL, 5)
        sizer.Add(spin, 0, wx.ALL, 5)
        panel.SetSizer(sizer)
        sizer.Fit(panel)
        sizer.Fit(self)
        self.Layout()
    def onspin(self,evt):
        self.value = self.spin.GetValue()
    def pressed(self,evt):
        sample = rand_sample(self.value)
        dlg = wx.MessageDialog(self, sample,
                               '命运选中之人是！',
                               wx.OK | wx.ICON_INFORMATION
                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
        dlg.ShowModal()
        dlg.Destroy()
        


class MyFrame(wx.Frame):
    def __init__(self):
        [Display_width,Display_high] = wx.DisplaySize()
        cartoon_pos = [Display_width*0.95-cartoon_width,Display_high*0.92-cartoon_high]

        wx.Frame.__init__(self, parent=None, pos=cartoon_pos, size=cartoon_size,
                          style=wx.FRAME_SHAPED|wx.STAY_ON_TOP)

        img = wx.Image('assets/mask.png')
        img.ConvertAlphaToMask()
        self.bitmap = wx.Bitmap(img)
        r = wx.Region(self.bitmap)
        self.SetShape(r)

        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftClickDown)
        self.Bind(wx.EVT_LEFT_UP,self.OnLeftClickUp)
        self.Bind(wx.EVT_MOTION,self.OnMouseMotion)
        self.Bind(wx.EVT_PAINT,self.OnPaint)
        self.Bind(wx.EVT_CONTEXT_MENU,self.OnRightClickDown)

    def OnLeftClickDown(self, event):
        self.CaptureMouse()
        pos = event.GetPosition()
        self.pt = wx.Point(pos.x,pos.y)
        with open('recognition.py') as r:
            exec(r.read())

    def OnLeftClickUp(self, event):
        self.ReleaseMouse()

    def OnMouseMotion(self, event):
        if event.Dragging() and event.LeftIsDown():
            pos = self.ClientToScreen(event.GetPosition())
            self.Move((pos.x-self.pt.x,pos.y-self.pt.y))

    def OnRightClickDown(self, event):
        if not hasattr(self,'randid'):
            self.randid = wx.NewIdRef()
            self.dashid = wx.NewIdRef()
            self.exid = wx.NewIdRef()

            self.Bind(wx.EVT_MENU,self.randselect,id=self.randid)
            self.Bind(wx.EVT_MENU,self.opendash,id=self.dashid)
            self.Bind(wx.EVT_MENU,self.ex,id=self.exid)
            print('Bind success')
        menu = wx.Menu()
        rand = wx.MenuItem(menu,id=self.randid,text='随机选择学生')
        dash = wx.MenuItem(menu,id=self.dashid,text='启动Dash')
        ex = wx.MenuItem(menu,id=self.exid,text='退出')
        menu.Append(rand)
        menu.Append(dash)
        menu.Append(ex)
        self.PopupMenu(menu)
        menu.Destroy()

    def randselect(self,evt):
        width,height = wx.DisplaySize()
        win = transient_popup(self,
                            wx.SIMPLE_BORDER)
        win.Position((width/2,height/2),(0,28))
        win.Popup()
    
    def opendash(self,event):
        with open('dashboard.py') as d:
            exec(d.read())

    def ex(self,event):
        self.Destroy()

    def OnPaint(self,event):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bitmap, 0, 0)

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame()
        self.frame.Show(True)
        return True

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()