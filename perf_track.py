#-*- coding: utf-8-*-
import wx
import monitor


class MonitorFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=-1,
                title="PerfTrack",
                pos=(100, 100), size=(800, 600))
        self.conf = dict()
        self.BuildUI()
        # self.InitSearchCtrls()

    def BuildUI(self):
        # config box
        self.proc_name_label = wx.StaticText(parent=self, label='Process: ', style=wx.ALIGN_CENTER)
        self.proc_name_value = wx.TextCtrl(parent=self, value='python')
        self.proc_name_box = wx.BoxSizer(wx.HORIZONTAL)
        self.proc_name_box.Add(self.proc_name_label, 1, wx.ALIGN_CENTER, 5, 0)
        self.proc_name_box.Add(self.proc_name_value, 2, wx.ALIGN_CENTER, 5, 0)

        self.proc_msg = wx.TextCtrl(parent=self, value='Please input a process name or ID', size=(450, 30), style=wx.TE_READONLY|wx.BORDER_NONE|wx.ST_NO_AUTORESIZE)
        self.proc_msg.SetBackgroundColour(self.proc_name_label.BackgroundColour)
        msg_font = wx.Font(10, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.proc_msg.SetFont(msg_font)
        #self.proc_name = wx.SearchCtrl(self)
        self.configBox= wx.BoxSizer(wx.VERTICAL)
        self.configBox.AddSpacer(10)
        self.configBox.Add(self.proc_name_box, 0, wx.LEFT, 5, 0)
        self.configBox.Add(self.proc_msg, 1, wx.LEFT, 5, 0)
        #self.configBox.Add(self.proc_name, 1, wx.ALL | wx.EXPAND, 5, 0)

        # toolbox, start stop
        self.startBtn = wx.Button(parent=self, label="Start", size=(60, 60))
        self.stopBtn = wx.Button(parent=self, label="Stop")
        self.showBtn = wx.Button(parent=self, label="Show")
        self.controlBox = wx.BoxSizer(wx.HORIZONTAL)
        self.controlBox.Add(self.startBtn, 1, wx.ALL | wx.EXPAND, 5, 0)
        self.controlBox.Add(self.showBtn, 1, wx.ALL | wx.EXPAND, 5, 0)
        self.controlBox.Add(self.stopBtn, 1, wx.ALL | wx.EXPAND, 5, 0)

        self.startBtn.Enable()
        self.stopBtn.Disable()

        self.toolbox = wx.BoxSizer(wx.HORIZONTAL)
        self.toolbox.Add(self.configBox, 3, wx.ALL, 5, 0)
        self.toolbox.Add(self.controlBox, 2, wx.RIGHT, 5, 0)

        # perf log box
        self.perf_log = wx.TextCtrl(parent=self,
                style=wx.TE_AUTO_SCROLL | wx.TE_MULTILINE)
        self.perf_log.SetEditable(False)
 
        # main box
        self.mainbox = wx.BoxSizer(wx.VERTICAL)
        self.mainbox.Add(self.toolbox, 0, wx.NORMAL, 0, 0)
        self.mainbox.Add(self.perf_log, 1, wx.ALL | wx.EXPAND, 5, 5)

        self.SetSizer(self.mainbox)
        self.CenterOnScreen()

        self.startBtn.Bind(wx.EVT_BUTTON, self.OnStartScan)
        self.stopBtn.Bind(wx.EVT_BUTTON, self.OnStopScan)
        #self.proc_name_value.Bind(wx.EVT_KILL_FOCUS, self.OnProcInput)
        self.proc_name_value.Bind(wx.EVT_TEXT, self.OnProcInputChanged)

    def OnStartScan(self, event):
        # clear log if too big
        if len(self.perf_log.GetValue()) > 1024:
            self.perf_log.SetValue('')
        self.startBtn.Disable()
        self.showBtn.Disable()
        self.stopBtn.Enable()
        # start thread
        def update_log(*args):
            wx.CallAfter(self.perf_log.AppendText, *args)

        proc = monitor.find_proc(self.proc_name_value.GetValue())
        self.mem_watcher = monitor.ProcWatcher(proc, update_log, 1)
        self.mem_watcher.start()

    def OnStopScan(self, event):
        self.startBtn.Enable()
        self.showBtn.Enable()
        self.stopBtn.Disable()
        # stop thread
        self.mem_watcher.stop()

    def OnProcInputChanged(self, event):
        input_text = self.proc_name_value.GetValue().strip()
        self.InitPid(input_text)

    def InitPid(self, input_text):
        if input_text.isdigit():  # Process ID
            self.conf['pid'] = self.MatchProcID(int(input_text))
            if self.conf['pid'] is not None:
                return
        self.conf['pid'] = self.MatchProcName(input_text)  # else Process name

    def MatchProcID(self, pid):
        proc = monitor.init_proc(pid)
        if proc is not None:  # get process by Name
            self.proc_msg.SetValue('Proc ID: %s, Process Name: %s' % (proc.pid, proc.name()))
            return pid
        else:
            return None

    def MatchProcName(self, pname):
        if 0 == len(pname):
            self.proc_msg.SetValue('Please input a process name or ID')
            return None
        proc = monitor.get_procs(pname)
        if 0 == len(proc):
            self.proc_msg.SetValue('Proc not exists or AccessDenied')
        elif len(proc) > 1:
            self.proc_msg.SetValue('Multi Processes Match, use Process ID instead')
        else:
            self.proc_msg.SetValue('Proc ID: %s' % proc.pop().pid)

class MonitorUI(wx.App):

    def OnInit(self):
        frame = MonitorFrame()
        self.SetTopWindow(frame)
        frame.Show()
        return True


if '__main__' == __name__:
    app = MonitorUI()
    app.MainLoop()
