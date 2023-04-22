import os
import copy
import collections
from decimal import *
import config
import shutil
import time
import subprocess

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def pretty_print(msg, type='normal'):
    if type == 'normal':
        print(msg)
    else:
        types = type.split('/')
        code = ''
        endcode = ''
        for type in types:
            formatted_type = type.upper()
            code += getattr(bcolors, formatted_type)
            endcode += bcolors.ENDC
        print()
        print("------------------------------------------")
        print('{}{}{}'.format(code, msg, endcode))
        print("------------------------------------------")
        print()

def value_for(endpoint, data, default='', encoding=None):
    new_data = copy.deepcopy(data)
    points = endpoint.split('.')
    value = ''
    for i, e in enumerate(points):
        if e in new_data:
            new_data = new_data[e]
            value = new_data
            if value is None:
                value = default
                break
        else:
            value = default
            break
    if encoding is not None:
        value = value.encode(encoding)
    return value


def set_value(endpoint, value, data, initial=True):
    if initial:
        current_data = copy.deepcopy(data)
    else:
        current_data = data
    endpoint = endpoint.strip().strip('.')

    points = endpoint.split('.')
    if len(points) < 2:
        current_data[points[0]] = value
    else:
        word = points[0]
        if word == '':
            print("woops  ", endpoint)
        if word not in current_data or not isinstance(current_data[word], collections.Mapping):
            current_data[word] = {}

        sliced_points = points[1:]
        new_endpoint = '.'.join(sliced_points)
        set_value(new_endpoint, value, current_data[word], initial=False)

    return current_data


def make_number(data, digits=None, labels=False):
    try:
        new_data = copy.deepcopy(data)
        new_data = float(new_data)
    except ValueError:
        if new_data == "<LOQ":
            new_data = "&ltLOQ"
        if not labels:
            new_data = float(0)

    output = new_data
    if digits is not None and isinstance(new_data, float):
        quantizer = '1.'
        if int(digits) > 0:
            zeros = '.'
            for i in range(int(digits - 1)):
                zeros += '0'
            quantizer = zeros + '1'
        dec = Decimal(new_data).quantize(Decimal(quantizer))
        output = str(dec)
    if not labels:
        output = float(output)
    return output


def _init_bin(executable_name):
    start = time.clock()
    if not os.path.exists(config.BIN_DIR):
        print("Creating bin folder")
        os.makedirs(config.BIN_DIR)
    print("Copying binaries for "+executable_name+" in /tmp/bin")
    currfile = os.path.join(config.CURR_BIN_DIR, executable_name)
    newfile  = os.path.join(config.BIN_DIR, executable_name)
    shutil.copy2(currfile, newfile)
    print("Giving new binaries permissions for lambda")
    os.chmod(newfile, 0o755)
    elapsed = (time.clock() - start)
    print(executable_name+" ready in "+str(elapsed)+'s.')
