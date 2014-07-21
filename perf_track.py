#-*- coding: utf-8-*-
import wx
import monitor


__app_name__ = 'PerfTrack'
__author__ = 'Jackon Yang'
__email__ = 'jiekunyang@gmail.com'


def format_proc(proc):
    """brief description of proc in string format

    get all info from proc to make sure that they in correct case
    """
    return 'Process Name: %s, ID: %s.' % (proc.name(), proc.pid)


class MonitorFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=-1,
                title=__app_name__,
                pos=(100, 100), size=(800, 600))
        self.conf = dict()
        self.BuildUI()
        # self.InitSearchCtrls()
        self.proc_tracking = None
        self.proc_name_value.SetFocus()

    def BuildUI(self):
        # ------- config box ------------
        # process name
        self.proc_name_label = wx.StaticText(parent=self, label='Process Name: ', style=wx.ALIGN_CENTER)
        self.proc_name_value = wx.TextCtrl(parent=self, value='')
        self.proc_name_box = wx.BoxSizer(wx.HORIZONTAL)
        self.proc_name_box.Add(self.proc_name_label, 1, wx.ALIGN_CENTER, 5, 0)
        self.proc_name_box.Add(self.proc_name_value, 2, wx.ALIGN_CENTER, 5, 0)
        # input response
        self.proc_msg = wx.StaticText(parent=self, label='', size=(450, 30), style=wx.ALIGN_LEFT|wx.ST_NO_AUTORESIZE)
        # add to config box
        self.configBox= wx.BoxSizer(wx.VERTICAL)
        self.configBox.AddSpacer(10)
        self.configBox.Add(self.proc_name_box, 0, wx.LEFT, 5, 0)
        self.configBox.AddSpacer(10)
        self.configBox.Add(self.proc_msg, 1, wx.LEFT, 5, 0)

        # ------- control box ------------
        self.startBtn = wx.Button(parent=self, label="Start", size=(60, 60))
        self.stopBtn = wx.Button(parent=self, label="Stop")
        self.showBtn = wx.Button(parent=self, label="Show")
        self.controlBox = wx.BoxSizer(wx.HORIZONTAL)
        self.controlBox.Add(self.startBtn, 1, wx.ALL | wx.EXPAND, 5, 0)
        self.controlBox.Add(self.showBtn, 1, wx.ALL | wx.EXPAND, 5, 0)
        self.controlBox.Add(self.stopBtn, 1, wx.ALL | wx.EXPAND, 5, 0)

        self.startBtn.Enable()
        self.stopBtn.Disable()

        # ------- tool box(config, control) -------
        self.toolbox = wx.BoxSizer(wx.HORIZONTAL)
        self.toolbox.Add(self.configBox, 3, wx.ALL, 5, 0)
        self.toolbox.Add(self.controlBox, 2, wx.RIGHT, 5, 0)
        # ------- track log box -------------------
        self.track_log = wx.TextCtrl(parent=self, style=wx.TE_AUTO_SCROLL | wx.TE_MULTILINE)
        self.track_log.SetEditable(False)
        # ------- main box(tool, tracklog) --------
        self.mainbox = wx.BoxSizer(wx.VERTICAL)
        self.mainbox.Add(self.toolbox, 0, wx.NORMAL, 0, 0)
        self.mainbox.Add(self.track_log, 1, wx.ALL | wx.EXPAND, 5, 5)

        self.SetSizer(self.mainbox)
        self.CenterOnScreen()

        self.startBtn.Bind(wx.EVT_BUTTON, self.OnStartScan)
        self.stopBtn.Bind(wx.EVT_BUTTON, self.OnStopScan)
        self.proc_name_value.Bind(wx.EVT_TEXT, self.OnProcInputChanged)

    def OnStartScan(self, event):
        proc_name = self.proc_name_value.GetValue().strip()
        if self.proc_tracking is None and len(proc_name) > 0:
            self.MatchProcName(proc_name)
        if self.proc_tracking is None:
            if 0 == len(proc_name):
                msg = 'Please input a process name!'
            else:
                msg = 'No such process!\nMake sure that %s is running and then start %s' % (proc_name, __app_name__)
            dlg = wx.MessageDialog(None, msg, "%s Error" % __app_name__, wx.ICON_ERROR)
            dlg.ShowModal()
            return None
        # transfer button status
        self.startBtn.Disable()
        self.showBtn.Disable()
        self.stopBtn.Enable()
        # clear log
        self.track_log.SetValue('')
        wx.CallAfter(self.StartTrack, self.proc_tracking, self.proc_name_value.GetValue())

    def update_log(self, *args):
        wx.CallAfter(self.track_log.AppendText, *args)

    def StartTrack(self, proc, proc_name):
        #while proc is None:
        #    proc = monitor.find_proc(proc_name)
        self.mem_watcher = monitor.ProcWatcher(proc, self.update_log, 1)
        self.mem_watcher.start()
        # deal with close proc while monitoring

    def OnStopScan(self, event):
        self.startBtn.Enable()
        self.showBtn.Enable()
        self.stopBtn.Disable()
        # stop thread
        self.mem_watcher.stop()

    def OnProcInputChanged(self, event):
        self.MatchProcName(self.proc_name_value.GetValue().strip())

    def MatchProcName(self, pname):
        self.proc_tracking = None
        if 0 == len(pname):
            self.proc_msg.SetLabel('Please input a process name')
            return None
        procs = monitor.get_procs(pname)
        if 0 == len(procs):
            self.proc_msg.SetLabel('Process not exists or AccessDenied')
            return None
        self.proc_tracking = procs[0]
        if len(procs) > 1:
            self.proc_msg.SetLabel('Multi Processes Match, use %s' % format_proc(self.proc_tracking))
        else:
            self.proc_msg.SetLabel(format_proc(self.proc_tracking))
        return self.proc_tracking


class MonitorUI(wx.App):

    def OnInit(self):
        frame = MonitorFrame()
        self.SetTopWindow(frame)
        frame.Show()
        return True


if '__main__' == __name__:
    app = MonitorUI()
    app.MainLoop()
