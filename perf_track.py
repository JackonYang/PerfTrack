# -*- coding: utf-8-*-
import wx
import monitor


class MonitorFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=-1,
                title="PerfTrack",
                pos=(100, 100), size=(500, 600))
        self.BuildUI()

    def BuildUI(self):
        # perf log box
        self.perf_log = wx.TextCtrl(parent=self,
                style=wx.TE_AUTO_SCROLL | wx.TE_MULTILINE)
        self.perf_log.SetEditable(False)

        # toolbox, start stop
        self.startBtn = wx.Button(parent=self, label="Start")
        self.stopBtn = wx.Button(parent=self, label="Stop")
        self.showBtn = wx.Button(parent=self, label="Show")

        self.proc_name_label = wx.StaticText(parent=self, label='Process Name', style=wx.ALIGN_CENTER)
        self.proc_name_value = wx.TextCtrl(parent=self, value='python')

        self.startBtn.Enable()
        self.stopBtn.Disable()

        self.toolbox = wx.BoxSizer(wx.VERTICAL)
        self.toolbox.Add(self.proc_name_label, 1, wx.ALL | wx.EXPAND, 5, 0)
        self.toolbox.Add(self.proc_name_value, 1, wx.ALL | wx.EXPAND, 5, 0)
        self.toolbox.Add(self.startBtn, 1, wx.ALL | wx.EXPAND, 5, 0)
        self.toolbox.Add(self.showBtn, 1, wx.ALL | wx.EXPAND, 5, 0)
        self.toolbox.Add(self.stopBtn, 1, wx.ALL | wx.EXPAND, 5, 0)
 
        # main box
        self.mainbox = wx.BoxSizer(wx.HORIZONTAL)
        self.mainbox.Add(self.perf_log, 1, wx.ALL | wx.EXPAND, 5, 5)
        self.mainbox.Add(self.toolbox, 0, wx.NORMAL, 0, 0)

        self.SetSizer(self.mainbox)
        self.CenterOnScreen()

        self.startBtn.Bind(wx.EVT_BUTTON, self.OnStartScan)
        self.stopBtn.Bind(wx.EVT_BUTTON, self.OnStopScan)

    def OnStartScan(self, event):
        # clear log if too big
        if len(self.perf_log.GetValue()) > 1024:
            self.perf_log.SetValue('')
        self.startBtn.Disable()
        self.showBtn.Disable()
        self.stopBtn.Enable()
        # start thread
        proc = monitor.get_proc_by_name(self.proc_name_value.GetValue())
        self.mem_watcher = monitor.ProcWatcher(proc, self.perf_log.AppendText, 1)
        self.mem_watcher.start()

    def OnStopScan(self, event):
        self.startBtn.Enable()
        self.showBtn.Enable()
        self.stopBtn.Disable()
        # stop thread
        self.mem_watcher.stop()


class MonitorUI(wx.App):

    def OnInit(self):
        frame = MonitorFrame()
        self.SetTopWindow(frame)
        frame.Show()
        return True

if '__main__' == __name__:
    app = MonitorUI()
    app.MainLoop()
