#!/usr/bin/python
"""
Module for mapping naga razer side buttons to actions in linux.

It uses linux tool xdotool.
"""


import json
from evdev import InputDevice, categorize, ecodes, event_factory
from evdev.ecodes import keys
import os
import copy
import pprint
from subprocess import call, Popen, PIPE
import threading
import sys



CONFIG = "/home/miguel/.config/NagaRazer"
XDOTOOL = {
    'key' : 'key'
}

NAGA_BUTTON = {
    "KEY_1" : "01",
    "KEY_2" : "02",
    "KEY_3" : "03",
    "KEY_4" : "04",
    "KEY_5" : "05",
    "KEY_6" : "06",
    "KEY_7" : "07",
    "KEY_8" : "08",
    "KEY_9" : "09",
    "KEY_0" : "10",
    "KEY_MINUS" : "11",
    "KEY_EQUAL" : "12",
    "BTN_EXTRA" : "BTN_EXTRA",
    "BTN_SIDE"  : "BTN_SIDE"
}




class NagaDaemon:
    """
    Class that implements naga razer macro mappings
    """

    def __init__(self, config_dir = '/home/miguel/.config/NagaRazer'):

        config_file = config_dir + "/" + "naga_config.json"
        print config_file
        try:
            fd = open(config_file)
        except:
            print("- Error: config json file cannot be opened (%s)" % config_file)
            return None

        try:
            self.config_data = json.load(fd)
        except:
            print "--- Error Json file {} is not valid".format(config_file)
            fd.close()
            return None
        fd.close()

        #print(self.config_data)
        self.user = self.config_data['properties']['user']
        self.map_index = 0
        self.current = {}
        self._load_mapping(self.map_index)
        self.print_current_mapping()
        self.dev = {}


        #verify user who called NagaDaemon
        #self._get_current_user()

        #open device
        try:
            device = self.config_data['properties']['devices']['sidebuttons']
            self.dev['sidebuttons'] = InputDevice(device)
        except:
            print("+++ Error: {} does not exists sidebuttons".format(device))
            return None
        try:
            device = self.config_data['properties']['devices']['frontbuttons']
            self.dev['frontbuttons'] = InputDevice(device)
        except:
            print("+++ Error: {} does not exists".format(device))
            return None

        #init loop
        threading.Thread(target=self._listen_events, args=('sidebuttons',True,)).start()
        threading.Thread(target=self._listen_events, args=('frontbuttons',False,)).start()
        #self._listen_events('sidebuttons')


    def _load_mapping(self, id):
        self.current = copy.deepcopy(self.config_data['mappings'][id])
        return 1

    def _toggle_mapping(self):
        next_index = ( self.map_index + 1 ) % len(self.config_data['mappings'])
        self._load_mapping(next_index)
        self.map_index = next_index
        print("+++ current index {}".format(self.map_index))
        return 1


    def print_current_mapping(self):
        print(json.dumps(self.current, indent = 3, sort_keys = True))


    def _listen_events(self, panel, grab):
        if grab:
            self.dev[panel].grab()
        for event in self.dev[panel].read_loop():
            if event.type == ecodes.EV_KEY and event.value == 1:
                keycode = keys[event.code]
                try:
                    if NAGA_BUTTON[keycode] in self.current[panel]:
                        print self.current[panel][NAGA_BUTTON[keycode]]
                        self._execute_action(self.current[panel][NAGA_BUTTON[keycode]])
                    print keys[event.code]
                    print event
                    print categorize(event)
                except:
                    continue
                

    def _get_current_user(self):
        proc=Popen(['who','am','i'],stdout = PIPE)
        output = proc.stdout.read()
        self.user = output.split(' ')[0]
        print "user: {}  pid= {}".format(self.user,proc.pid)



    def _execute_action(self,actions):
        for i in range(len(actions)):
            if 'type' in actions[i]:
                if actions[i]['type'] == 'toggle':
                    self._toggle_mapping()
                    self.print_current_mapping()
                    return 1
                elif actions[i]['type'] == 'key':
                    print(actions[i]['action'])
                    call(["xdotool",'key',actions[i]['action']])
                elif actions[i]['type'] == 'run':
                    if 'user' in actions[i]:
                        user = actions[i]['user']
                    else:
                        user = self.user
                    if 'command' in actions[i]:
                        command = actions[i]['command']
                        if 'params' in actions[i]:
                            for j in range(len(actions[i]['params'])):
                                command = command + " " + actions[i]['params'][j]
                        pcommand = ['su', '-', '-c', command, user]
                        print pcommand
                        Popen(pcommand)
                elif actions[i]['type'] == 'click':
                    if actions[i]['button'] == 'left':
                        button = '1'
                    elif actions[i]['button'] == 'right':
                        button = '3'
                    elif actions[i]['button'] == 'middle':
                        button = '2'
                    else:
                        continue
                    print(button)
                    call(['xdotool', 'click', button])
                elif actions[i]['type'] == 'position':
                    try:
                        call(['xdotool', 'mousemove', actions[i]['x'], actions[i]['y']])
                    except:
                        print('+++ error in position')
                        return 0
            else:
                print("No action")






                



def main(args):
    length = len(args)
    if length == 1:
        naga = NagaDaemon(args[0])
    elif length == 0:
        naga = NagaDaemon()
    else:
        print("""
Usage: naga_razer.py [config_dir]
  Configuration file must be named naga_config.json
""")


if __name__ == "__main__":
    main(sys.argv[1:])