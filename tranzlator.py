#!/usr/bin/env python

# Script to translate char codes logged by zloggger to readable characters
# By Zaid Sabih / Zaid Al Quraishi

from __future__ import print_function

import argparse


def generate_chars_dict(file):    
    chars_dict = dict()

    with open(file) as map_file:
        for line in map_file.readlines():
            line = line.split()
            
            try:
                chars_dict[line[1]] = (process_key(line[3]), process_key(line[4]))
                character = line[3]
            except IndexError:
                continue
    return chars_dict

def process_key(key):
    if len(key) == 1:
        return key
    elif key == "Return":
        return "\n"
    elif key == "space":
        return " "
    elif key == "Shift_L" or key == "Shift_R":
        return "shift" 
    else:
        return "<" + key + ">"        

def translate_log(file, chars_dict):
    shift = False
    with open(file) as log_file:
        for line in log_file.readlines():
            line = line.split()
            char_code = line[2]

            if shift and chars_dict[char_code][0] == "shift":
                shift = False

            # print("shift is still " + str(shift))
            if line[1] == 'press':
                key = chars_dict[char_code][0]
                if key == "shift":
                    shift = True
                    continue

                if shift:
                    key = chars_dict[char_code][1] 
                print(key, end='')



def argument_parser():
    arguments = argparse.ArgumentParser(description='Zlogger Translator')
    arguments.add_argument('charmap', metavar = '[Character Map]', help='Character map file.')
    arguments.add_argument('log', metavar = '[Log]', help='Log file to translate.')

    return vars(arguments.parse_args())


arguments = argument_parser()
chars_dict = generate_chars_dict(arguments['charmap'])

translate_log(arguments['log'], chars_dict)
print("\n")



