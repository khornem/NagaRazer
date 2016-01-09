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
from subprocess import call



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

        self.current = {}
        self._load_mapping(0)
        self.print_current_mapping()

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


    def print_current_mapping(self):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.current) 


    def _listen_events(self):
        self.dev.grab()
        for event in self.dev.read_loop():
            if event.type == ecodes.EV_KEY and event.value == 1:
                keycode = keys[event.code]
                if keycode in self.current['sidebuttons']:
                    print self.current['sidebuttons'][keycode]
                    self._execute_action(self.current['sidebuttons'][keycode])
                print keys[event.code]
                print event
                print categorize(event)


    def _execute_action(self,actions):
        for i in range(len(actions)):
            if 'action' in actions[i]:
                print(actions[i]['action'])
                call(["xdotool",'key',actions[i]['action']])


            elif 'string' in actions[i]:
                msg = actions[i]['string']
                for i in range(len(msg)):
                    call(["xdotool",'key',msg[i]])
            else:
                print("No action")






                



def main():
    naga=NagaDaemon()


if __name__ == "__main__":
    main()