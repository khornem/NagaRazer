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



CONFIG = "/home/miguel/Dropbox/20_Programacion/04_python/13_naga"
XDOTOOL = {
    'key' : 'key'
}




class NagaDaemon:
    """
    Class that implements naga razer macro mappings
    """

    def __init__(self):

        config_file = CONFIG + "/" + "naga_config.json"
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

        #verify user who called NagaDaemon
        #self._get_current_user()

        #open device
        try:
            device = self.config_data['properties']['devices']['sidebuttons']
            self.dev = InputDevice(device)
        except:
            print("+++ Error: {} does not exists".format(device))

        #init loop
        self._listen_events()


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
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.current) 


    def _listen_events(self):
        #self.dev.grab()
        for event in self.dev.read_loop():
            if event.type == ecodes.EV_KEY and event.value == 1:
                keycode = keys[event.code]
                if keycode in self.current['sidebuttons']:
                    print self.current['sidebuttons'][keycode]
                    self._execute_action(self.current['sidebuttons'][keycode])
                print keys[event.code]
                print event
                print categorize(event)

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






                



def main():
    naga=NagaDaemon()


if __name__ == "__main__":
    main()