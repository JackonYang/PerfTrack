# -*- coding: utf-8-*-
import psutil

def get_proc(pname):
    """ get process by name
    
    return the 1st process if there are more than one
    """
    procs = psutil.get_process_list()
    for proc in procs:
        if proc.name().lower() == pname.lower():
            return proc
    return None

if '__main__' == __name__:
    print get_proc("CHrome")
    print get_proc("gnome-terminal")
    print get_proc("python")
