#-*- coding: utf-8-*-
import wx
import monitor

from matplotlib.figure import Figure
from matplotlib import font_manager
import numpy as np
from matplotlib.backends.backend_wxagg import \
  FigureCanvasWxAgg as FigureCanvas


__app_name__ = 'PerfTrack'
__author__ = 'Jackon Yang'
__email__ = 'jiekunyang@gmail.com'

TIMER_ID = wx.NewId()
POINTS = 300

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
        self.proc_running = False
        self.proc_name_value.SetFocus()
        self.t = wx.Timer(self, TIMER_ID)

    def BuildUI(self):
        # ------- config box ------------
        # process name
        self.proc_name_label = wx.StaticText(parent=self, label='Process Name: ', style=wx.ALIGN_CENTER)
        self.proc_name_value = wx.TextCtrl(parent=self, value='', style=wx.TE_PROCESS_ENTER)
        self.proc_name_box = wx.BoxSizer(wx.HORIZONTAL)
        self.proc_name_box.Add(self.proc_name_label, 1, wx.ALIGN_CENTER, 5, 0)
        self.proc_name_box.Add(self.proc_name_value, 2, wx.ALIGN_CENTER, 5, 0)
        # input response
        self.proc_msg = wx.StaticText(parent=self, label='', size=(450, 30), style=wx.ALIGN_LEFT|wx.ST_NO_AUTORESIZE)
        # add to config box
        self.configBox= wx.BoxSizer(wx.VERTICAL)
        self.configBox.AddSpacer(10)
        self.configBox.Add(self.proc_name_box, 1, wx.LEFT, 5, 0)
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
        self.fig = Figure((6, 4), 100)
        # bind the Figure to the backend specific canvas
        self.canvas = FigureCanvas(self, wx.ID_ANY, self.fig)
        self.InitPlotUI()
        self.dispbox = wx.BoxSizer(wx.HORIZONTAL)
        self.dispbox.Add(self.track_log, 1, wx.ALL|wx.EXPAND, 5, 5)
        self.dispbox.Add(self.canvas, 5, wx.ALL|wx.EXPAND, 5, 5)
        # ------- main box(tool, tracklog) --------
        self.mainbox = wx.BoxSizer(wx.VERTICAL)
        self.mainbox.Add(self.toolbox, 1, wx.NORMAL, 0, 0)
        self.mainbox.Add(self.dispbox, 5, wx.ALL|wx.EXPAND, 5, 5)

        self.SetSizer(self.mainbox)
        self.CenterOnScreen()

        self.startBtn.Bind(wx.EVT_BUTTON, self.OnStartTrack)
        self.stopBtn.Bind(wx.EVT_BUTTON, self.OnStopTrack)
        self.proc_name_value.Bind(wx.EVT_TEXT, self.OnProcInputChanged)
        self.proc_name_value.Bind(wx.EVT_TEXT_ENTER, self.OnStartTrack)
        self.Bind(wx.EVT_ACTIVATE, self.OnWindowActivate)

    def OnStartTrack(self, event):
        if self.proc_running:
            return
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
        self.proc_running = True
        # deal with close proc while monitoring
        # plot
        self.t.Start(50)

    def OnStopTrack(self, event):
        self.startBtn.Enable()
        self.showBtn.Enable()
        self.stopBtn.Disable()
        # stop thread
        self.mem_watcher.stop()
        self.t.Stop()
        self.proc_running = False

    def OnWindowActivate(self, event):
        if not self.proc_running:
            self.MatchProcName(self.proc_name_value.GetValue().strip())

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

    def InitPlotUI(self):
        # add a subplot
        self.ax = self.fig.add_subplot(111)
        # limit the X and Y axes dimensions
        self.ax.set_ylim([0, 100])
        self.ax.set_xlim([0, POINTS])
       
        self.ax.set_autoscale_on(False)
        self.ax.set_xticks([])
        # we want a tick every 10 point on Y (101 is to have 10
        self.ax.set_yticks(range(0, 101, 10))
        # disable autoscale, since we don't want the Axes to ad
        # draw a grid (it will be only for Y)
        self.ax.grid(True)
        # generates first "empty" plots
        self.user = [None] * POINTS
        self.l_user,=self.ax.plot(range(POINTS),self.user,label='User %')

        # add the legend
        self.ax.legend(loc='upper center',
                           ncol=4,
                           prop=font_manager.FontProperties(size=10))
        # force a draw on the canvas()
        # trick to show the grid and the legend
        self.canvas.draw()
        # save the clean background - everything but the line
        # is drawn and saved in the pixel buffer background
        self.bg = self.canvas.copy_from_bbox(self.ax.bbox)
        # bind events coming from timer with id = TIMER_ID
        # to the onTimer callback function
        wx.EVT_TIMER(self, TIMER_ID, self.onTimer)

    def onTimer(self, evt):
        """callback function for timer events"""
        # restore the clean background, saved at the beginning
        self.canvas.restore_region(self.bg)
                # update the data
        temp =np.random.randint(10,80)
        self.user = self.user[1:] + [temp]
        # update the plot
        self.l_user.set_ydata(self.user)
        # just draw the "animated" objects
        self.ax.draw_artist(self.l_user)# It is used to efficiently update Axes data (axis ticks, labels, etc are not updated)
        self.canvas.blit(self.ax.bbox)

class MonitorUI(wx.App):

    def OnInit(self):
        frame = MonitorFrame()
        self.SetTopWindow(frame)
        frame.Show()
        return True


if '__main__' == __name__:
    app = MonitorUI()
    app.MainLoop()
