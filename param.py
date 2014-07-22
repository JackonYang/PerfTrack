#-*- coding: utf-8-*-
import json

def is_number(input):
    return isinstance(input, (int, float))

class Validator:
    
    def validate_process_name(self, name):
        return isinstance(name, basestring)

    def validate_interval(self, interval):
        return is_number(interval) and interval > 0

    def validate_points(self, points):
        return isinstance(points, int) and points > 0

    def validate_y(self, ymin, ymax, ystep):
        # check ystep value
        return is_number(ymax) and is_number(ymin) and is_number(ystep) and ymin < ymax


def load_conf(filename):
    required = ['process_name', 'interval', 'points', 'ymin', 'ymax', 'ystep']
    params = json.load(open(filename))
    return params
