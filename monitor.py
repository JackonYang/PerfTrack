# -*- coding: utf-8-*-
import psutil
import time

def get_proc_by_name(pname):
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

def run(proc, interval=1):
    while(True):
        print proc.memory_info().rss
        time.sleep(interval)

if '__main__' == __name__:
    proc = get_proc_by_name("CHrome")
    run(proc)
