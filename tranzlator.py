#!/usr/bin/env python

import argparse

def parse_map(filename):
    keymap = {}
    # xmodmap modifiers
    # 0  Key
    # 1  Shift+Key
    # 2  mode_switch+Key
    # 3  mode_switch+Shift+Key
    # 4  AltGr+Key
    # 5  AltGr+Shift+Key
    
    chars_dict = dict()

    with open(filename) as map_file:
        for line in map_file.readlines():
            line = line.split()
            
            try:
                chars_dict[line[1]] = line[3]
                character = line[3]
                char_code = line[1]
            except IndexError:
                continue
    return chars_dict

def argument_parser():
    arguments = argparse.ArgumentParser(description='Zlogger Translator')
    arguments.add_argument('charmap', metavar = '[Character Map]', help='Character map file.')
    arguments.add_argument('log', metavar = '[Log]', help='Log file to translate.')
    arguments.add_argument('out', metavar = '[Out]', help='File to save result to.')

    return vars(arguments.parse_args())



arguments = argument_parser()
charmap = parse_map(arguments['charmap'])
print(charmap)



