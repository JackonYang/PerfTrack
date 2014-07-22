# -*- coding: utf-8-*-
import psutil
import time
import threading


def init_proc(pid):
    try:
        return psutil.Process(pid)
    except psutil.NoSuchProcess:
        return None


def find_proc(pname):
    """ get process by name
    
    return the first process if there are more than one
    """
    for proc in psutil.process_iter():
        try:
            if proc.name().lower() == pname.lower():
                return proc  # return if found one
        except psutil.AccessDenied:
            pass
        except psutil.NoSuchProcess:
            pass
    return None


def get_procs(pname):
    """ get all process named pname
    
    """
    procs = []
    for proc in psutil.process_iter():
        try:
            if proc.name().lower() == pname.lower():
                procs.append(proc)
        except psutil.AccessDenied:
            pass
        except psutil.NoSuchProcess:
            pass
    return procs


def get_rss_mem(proc, value_if_None=0):

    if proc is None:
        return value_if_None
    try:
        return proc.memory_info().rss
    except psutil.NoSuchProcess:
        return value_if_None


class ProcWatcher(threading.Thread):
    def __init__(self, proc, output, interval):
        threading.Thread.__init__(self)
        self.m_proc = proc
        self.thread_stop = False
        self.output = output
        self.interval = interval

    def run(self):
        while not self.thread_stop:
            self.output('%.4f MB\n' % (float(self.m_proc.memory_info().rss)/1024/1024))
            time.sleep(self.interval)

    def stop(self):
        self.thread_stop = True  


if '__main__' == __name__:
    def tout(msg):
        print msg
    mem_watcher = ProcWatcher(find_proc("CHrome"), tout, 1)
    mem_watcher.start()
    time.sleep(10)
    mem_watcher.stop()
