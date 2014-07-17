"""show cpu and memory performance infomation"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt


def keep_peak(orig_data, step=7, peak_range=5):
    """wave filtration

    if max-min <= peak_range, return 2 middle data
    else return max and min row"""

    res=[]
    for i in range(0, len(orig_data), step):
        cut=orig_data[i:i+step]
        cut.sort()
        if float(cut[-1])-float(cut[0])<peak_range:
            # if delta is small, take the two middle value.
            n=int(step/2)
            res.extend(orig_data[int(step/2)-1:int(step/2)+1])
        else:
            # take the max and min in the orig sequence
            if orig_data[i:i+step].index(cut[0])<orig_data[i:i+step].index(cut[-1]):
                res.extend([cut[0], cut[-1]])
            else:
                res.extend([cut[-1], cut[0]])
    return res


def read_data(filename, dataToRead=None):
    """ read performance data from file

    return a dictionary(performance_index:data)"""

    with open(filename, 'r') as f:
        def get_title(f):
            """skip line before title, and read title line"""
            line=f.readline()
            while '%' not in line:
                line=f.readline()
            else:
                title=line.split()
                title[0]='time'
            return title

        # init title tag
        title=get_title(f)
        data={}
        for tag in title:
            data[tag]=[]
        # read data
        for line in f.readlines():
            for tag, value in zip(title, line.split()):
                data[tag].append(value)
    return data


def plot(data):  # data:dict
    """plot data"""

    for y in data.values():
        plt.plot(y)
    plt.legend(data.keys())
    plt.title("cpu and memory performance figure")
    plt.show()


def data_to_show(data):
    """format useful info of cpu performance"""
    res={}
    for key in set(data.keys()) & {'%user', '%usr', '%system', '%sys', '%idle', '%memused'}:
        res[key]=keep_peak(data[key])

    return res


def main(filename_pre='test_03041503'):
    filterd={}
    filterd.update(data_to_show(read_data(filename_pre+'_cpu.txt')))
    filterd.update(data_to_show(read_data(filename_pre+'_mem.txt')))
    plot(filterd)

filename_pre=sys.argv[1]
main(filename_pre)
