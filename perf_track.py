#-*- coding: utf-8-*-
import wx
import monitor
import time

import param

from matplotlib.figure import Figure
import numpy as np
from matplotlib import font_manager
from matplotlib.backends.backend_wxagg import \
  FigureCanvasWxAgg as FigureCanvas


__app_name__ = 'PerfTrack'
__author__ = 'Jackon Yang'
__email__ = 'jiekunyang@gmail.com'

TIMER_ID = wx.NewId()


def getSizeInMb(sizeInBytes):
    return sizeInBytes * 1.0 / 1024 / 1024


def format_proc(proc):
    """brief description of proc in string format

    get all info from proc to make sure that they in correct case
    """
    return 'Process Name: %s, ID: %s, Memory(RSS): %s MB.' % (proc.name(), proc.pid, getSizeInMb(monitor.get_rss_mem(proc)))


_log_cache = []

def avg(data):
    return sum(data)/len(data)

def timestamp():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

class MonitorFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=-1,
                title=__app_name__,
                pos=(10, 10), size=(1200, 620))
        self.LoadParam()
        self.BuildUI()
        self.InitUiParam()
        self.proc_name_value.SetFocus()
        self.t = wx.Timer(self, TIMER_ID)

    def LoadParam(self):
        self.settings = param.load_param('config.json')
        if 'xmin' not in self.settings:
            self.settings['xmin'] = 0
        if 'xmax' not in self.settings:
            self.settings['xmax'] = self.settings['points']

    def BuildUI(self):
        # ------- config box ------------
        # process name
        self.proc_name_label = wx.StaticText(parent=self, label='Process Name: ', style=wx.ALIGN_CENTER)
        self.proc_name_value = wx.TextCtrl(parent=self, value='', style=wx.TE_PROCESS_ENTER)
        self.proc_name_box = wx.BoxSizer(wx.HORIZONTAL)
        self.proc_name_box.Add(self.proc_name_label, 1, wx.ALIGN_CENTER, 5, 0)
        self.proc_name_box.Add(self.proc_name_value, 2, wx.ALIGN_CENTER, 5, 0)
        # input response
        self.proc_msg = wx.StaticText(parent=self, label='', size=(800, 30), style=wx.ALIGN_LEFT|wx.ST_NO_AUTORESIZE)
        # add to config box
        self.configBox= wx.BoxSizer(wx.VERTICAL)
        self.configBox.Add(self.proc_name_box, 1, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5, 0)
        self.configBox.Add(self.proc_msg, 1, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5, 0)

        # ------- control box ------------
        self.startBtn = wx.Button(parent=self, label="Start", size=(60, 60))
        self.stopBtn = wx.Button(parent=self, label="Stop")
        self.showBtn = wx.Button(parent=self, label="Show")
        self.controlBox = wx.BoxSizer(wx.HORIZONTAL)
        self.controlBox.Add(self.startBtn, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5, 0)
        self.controlBox.Add(self.showBtn, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5, 0)
        self.controlBox.Add(self.stopBtn, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5, 0)

        self.startBtn.Enable()
        self.stopBtn.Disable()

        # ------- tool box(config, control) -------
        self.toolbox = wx.BoxSizer(wx.HORIZONTAL)
        self.toolbox.AddSpacer(20)
        self.toolbox.Add(self.configBox, 5, wx.ALL|wx.ALIGN_CENTER, 5, 0)
        self.toolbox.Add(self.controlBox, 2, wx.ALL|wx.ALIGN_CENTER, 5, 0)
        # ------- track log box -------------------
        self.track_log = wx.TextCtrl(parent=self, style=wx.TE_AUTO_SCROLL | wx.TE_MULTILINE)
        self.track_log.SetEditable(False)
        self.fig = self.InitPlotUI()
        self.canvas = FigureCanvas(self, wx.ID_ANY, self.fig)
        self.canvas.draw()
        self.bg = self.canvas.copy_from_bbox(self.ax.bbox)
        self.dispbox = wx.BoxSizer(wx.HORIZONTAL)
        self.dispbox.Add(self.track_log, 1, wx.ALL|wx.EXPAND, 5, 5)
        self.dispbox.Add(self.canvas, 0, wx.ALL|wx.EXPAND, 5, 5)
        # ------- main box(tool, tracklog) --------
        self.mainbox = wx.BoxSizer(wx.VERTICAL)
        self.mainbox.Add(self.toolbox, 1, wx.NORMAL, 0, 0)
        self.mainbox.Add(self.dispbox, 0, wx.EXPAND, 5, 5)

        self.SetSizer(self.mainbox)
        self.CenterOnScreen()

        self.startBtn.Bind(wx.EVT_BUTTON, self.OnStartTrack)
        self.stopBtn.Bind(wx.EVT_BUTTON, self.OnStopTrack)
        self.proc_name_value.Bind(wx.EVT_TEXT, self.OnProcInputChanged)
        self.proc_name_value.Bind(wx.EVT_TEXT_ENTER, self.OnStartTrack)
        self.Bind(wx.EVT_ACTIVATE, self.OnWindowActivate)
        wx.EVT_TIMER(self, TIMER_ID, self.onTimer)

    def InitUiParam(self):
        self.proc_name_value.SetValue(self.settings['process_name'])
        self.proc_tracking = None
        self.is_track_running = False

    def OnStartTrack(self, event):
        if self.is_track_running:
            return

        proc_name = self.proc_name_value.GetValue().strip()

        if 0 == len(proc_name):
            msg = 'Please input a process name!'
            dlg = wx.MessageDialog(None, msg, "%s Error" % __app_name__, wx.ICON_ERROR)
            dlg.ShowModal()
            return None

        if self.proc_tracking is None:
            self.MatchProcName(proc_name)
            if self.proc_tracking is None:
                msg = 'No such process!\nGo on to track %s?' % proc_name
                dlg = wx.MessageDialog(None, msg, "%s Error" % __app_name__, wx.YES_NO|wx.ICON_QUESTION)
                if dlg.ShowModal() != wx.ID_YES:
                    return None

        # transfer button status
        self.startBtn.Disable()
        self.showBtn.Disable()
        self.stopBtn.Enable()
        self.proc_name_value.Disable()
        # clear log
        self.track_log.SetValue('')
        wx.CallAfter(self.StartTrack, self.proc_tracking, self.proc_name_value.GetValue())

    def update_log(self, disp_data):
        global _log_cache
        _log_cache.append(disp_data)
        if len(_log_cache) >= (1000.0/self.settings['interval']):
            wx.CallAfter(self.track_log.AppendText, '%s | %.4f MB\n' % (timestamp(), avg(_log_cache)))
            _log_cache = []

    def StartTrack(self, proc, proc_name):
        self.is_track_running = True
        self.t.Start(self.settings['interval'])

    def OnStopTrack(self, event):
        self.startBtn.Enable()
        self.showBtn.Enable()
        self.stopBtn.Disable()
        self.proc_name_value.Enable()
        # stop thread
        self.t.Stop()
        self.is_track_running = False

    def OnWindowActivate(self, event):
        if not self.is_track_running:
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
            self.proc_msg.SetLabel('Warning! Multi Processes Match. use %s' % format_proc(self.proc_tracking))
        else:
            self.proc_msg.SetLabel(format_proc(self.proc_tracking))
        return self.proc_tracking

    def InitPlotUI(self):
        plot_points = self.settings['points']
        fig = Figure(figsize=(9, 5), dpi=100)
        self.ax = fig.add_subplot(111)

        self.ax.set_ylim([self.settings['ymin'], self.settings['ymax']])
        self.ax.set_xlim([self.settings['xmin'], self.settings['xmax']])
        self.ax.set_autoscale_on(False)

        self.ax.set_xticks([])
        self.ax.set_yticks(range(self.settings['ymin'], self.settings['ymax']+1, self.settings['ystep']))

        self.ax.grid(True)

        self.mem_rss_data = [None] * plot_points
        self.l_mem_rss,=self.ax.plot(range(plot_points), self.mem_rss_data, label='Memory(RSS) %')

        # add the legend
        self.ax.legend(loc='upper center',
                           ncol=4,
                           prop=font_manager.FontProperties(size=10))
        return fig

    def onTimer(self, evt):
        """callback function for timer events"""
        # restore the clean background, saved at the beginning
        self.canvas.restore_region(self.bg)
        # get new perf data
        if self.proc_tracking is None:
            proc_name = self.proc_name_value.GetValue().strip()
            self.proc_tracking = monitor.find_proc(proc_name)
        rss_mem = getSizeInMb(monitor.get_rss_mem(self.proc_tracking))
        # update log
        wx.CallAfter(self.update_log, rss_mem)
        # plot
        self.mem_rss_data = self.mem_rss_data[1:] + [rss_mem]
        self.l_mem_rss.set_ydata(self.mem_rss_data)
        self.ax.draw_artist(self.l_mem_rss)
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
