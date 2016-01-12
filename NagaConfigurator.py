#!/usr/bin/python


import json
import os
import sys
import copy








class NagaConfigurator:



    def __init__(self, config):

        self.config_original_data = {}
        self.config_file = config
        #Load configuration file if possible. Otherwise initialize file.
        if os.path.isfile(config):
            self.config_data = {}
            
            try:
                fd = open(config)
            except:
                print("- Error: config json file cannot be opened {}".format(config_file))
                return None
    
            try:
                self.config_original_data = json.load(fd)
            except:
                print "--- Error Json file {} is not valid".format(config_file)
                fd.close()
                return None
            fd.close()
            self.config_data = copy.deepcopy(self.config_original_data)
        else:
            self._init_config_file()



    def _init_config_file(self):

        initial_config = {
    "properties" : {
        "name" : "naga razer",
        "devices" : {
            "sidebuttons" : "/dev/input/by-id/usb-Razer_Razer_Naga-if01-event-kbd",
            "frontbuttons" : "/dev/input/by-id/usb-Razer_Razer_Naga-event-mouse"

        },
        "user" : "miguel"

    },
    "mappings" : [
        {
            "description" : "description",
            "id" : 1,
            "sidebuttons" : {
                "01" : [],
                "02" : [],
                "03" : [],
                "04" : [],
                "05" : [],
                "06" : [],
                "07" : [],
                "08" : [],
                "09" : [],
                "10" : [],
                "11" : [],
                "12" : []
            },
            "frontbuttons" : {
                "BTN_EXTRA" : [],
                "BTN_SIDE"  : []
            }

        }
    ]
}
        self.config_data = json.loads("{}".format(initial_config).replace("'",'"'))



    def add_new_blank_mapping(self):
        blank_mapping =   [{
            "description" : "description",
            "id" : 1,
            "sidebuttons" : {
                "01" : [],
                "02" : [],
                "03" : [],
                "04" : [],
                "05" : [],
                "06" : [],
                "07" : [],
                "08" : [],
                "09" : [],
                "10" : [],
                "11" : [],
                "12" : []
            },
            "frontbuttons" : {
                "BTN_EXTRA" : [],
                "BTN_SIDE"  : []
            }

        }]
        print self.config_data['mappings']
        print blank_mapping
        self.config_data['mappings'].extend(blank_mapping)


        
    def print_current_configuration(self):
        print(json.dumps(self.config_original_data, 
            indent=2, sort_keys=True))

    def print_target_configuration(self):
        print(json.dumps(self.config_data, indent = 2, sort_keys = True))

    def print_properties(self):
        print(json.dumps(self.config_data['properties'],
             indent = 2, sort_keys = True))

    def print_mapping(self, id):
        print(json.dumps(self.config_data['mappings'][id],
             indent = 2, sort_keys = True))


    def print_panel_configuration(self, map_id, panel):
        print(json.dumps(self.config_data['mappings'][map_id][panel],
             indent = 2, sort_keys = True))



    def print_button_mapping(self, map_id, panel, button):
        print(json.dumps(self.config_data['mappings'][map_id][panel][button], 
            indent = 2, sort_keys = True))

    def get_default_username(self):
        if 'user' in self.config_data['properties']:
            user = self.config_data['properties']['user']
        else:
            user = ""
        return user

    def set_username(self, user):
        self.config_data['properties']['user'] = user

    def get_device(self, panel):
        if panel in self.config_data['properties']['devices']:
            device = self.config_data['properties']['devices'][panel]
        else:
            device = ""
        return device

    def set_device(self, panel, device):
        self.config_data['properties']['devices'][panel] = device    


    def get_mapping_len(self):
        return len(self.config_data['mappings'])

    def delete_mapping(self, id):
        del self.config_data['mappings'][id]

    def list_mappings(self):
        id = 0
        for i in range(len(self.config_data['mappings'])):
            print (" [{:>02d}] : {}".format(i,self.config_data['mappings'][i]['description']))

    def delete_action(self,map_id, panel, button):
        self.config_data['mappings'][map_id][panel][button] = []

    def add_action(self, map_id, panel, button, action):
        self.config_data['mappings'][map_id][panel][button].extend(action)

    def get_mapping_description(self, map_id):
        return self.config_data['mappings'][map_id]['description']

    def set_mapping_description(self, map_id, description):
        self.config_data['mappings'][map_id]['description'] = description

    def save_config(self):
        with open(self.config_file, 'w') as outfile:
            json.dump(self.config_data, outfile, indent=4, sort_keys=True)






def print_menu(state):

    if state == 0:
        print """
=====================================================================
MAIN MENU
=====================================================================        
        1. show current configuration file
        2. show target configuration file
        3. show properties
        4. change default user
        5. change sidebuttons device
        6. change frontbuttons device            
        7. change mapping
        8. add new mappings
        9. delete mapping
        10: list mappings names
        99. save 
        0. exit 

        """
    elif state == 1:
        print """
=====================================================================
MAPPINGS MENU
=====================================================================        
        1. show mapping configuration
        2. change sidebuttons configuration
        3. change frontbuttons configuration
        4. change description
        0. up 

        """
    elif state == 2:
        print """
=====================================================================
SIDEBUTTONS MENU
=====================================================================        
        1. show sidebuttons configuration
        2. show button configuration
        3. list buttons available
        4. change button configuration 
        0. up 

        """
    elif state == 3:
        print """
=====================================================================
FRONTBUTTONS MENU
=====================================================================        
        1. show sidebuttons configuration
        2. show button configuration
        3. list buttons available
        4. change button configuration 
        0. up 

        """
    elif state == 4:
        print """
=====================================================================
ACTIONS MENU
=====================================================================        
        1. show current action
        2. reinitialize action
        3. add key action
        4. add click action
        5. add position action
        6. add run action
        7. add toggle action
        99. delete action 
        0. up 

        """
    elif state == 5:
        print """
=====================================================================
ACTIONS MENU
=====================================================================        
        1. show current actions set
        2. reinitialize actions set
        3. add key action
        4. add click action
        5. add position action
        6. add run action
        7. add toggle action
        99. delete action 
        0. up 

        """





def new_key_action():
    key_combination = raw_input("Enter key combination: ")
    action = { "action" : key_combination}
    return action


def isInt(str):
    try:
        int(str)
        return True
    except:
        return False





def main(args):
    config = NagaConfigurator(args[0])
    state = 0
    map_id = 0

    while True:
        print_menu(state)
        choice = raw_input("Select [0-9]: ")
        if state == 0:
            if choice == "0":
                return 1
            elif choice == "1":
                config.print_current_configuration()
                continue
            elif choice == "2":
                config.print_target_configuration()
                continue
            elif choice == "3":
                config.print_properties()
                continue
            elif choice == "4":
                user = config.get_default_username()
                print("Current user: {}".format(user))
                new_user = raw_input("New username: " )
                print("Username Selected : <{}>".format(new_user))
                yes_no = raw_input("Change username?[y/n]")
                if yes_no == "y":
                    config.set_username(new_user)
                continue
            elif choice == "5":
                device = config.get_device('sidebuttons')
                print("Current sidebuttons device: {}".format(device))
                new_device = raw_input("New device: ")
                print("Device Selected : <{}>".format(new_device))
                yes_no = raw_input("Change device?[y/n]")
                if yes_no == "y":
                    config.set_device('sidebuttons', new_device)
                continue
            elif choice == "6":
                device = config.get_device('frontbuttons')
                print("Current frontbuttons device: {}".format(device))
                new_device = raw_input("New device: ")
                print("Device Selected : <{}>".format(new_device))
                yes_no = raw_input("Change device?[y/n]")
                if yes_no == "y":
                    config.set_device('frontbuttons', new_device)
                continue

            elif choice == "7":
                nmaps = config.get_mapping_len()
                if nmaps == 1:
                    map_id = 0
                    state = 1
                else:
                    map_choice = raw_input("Select Map [0-{}]".format(nmaps - 1))
                    try:
                        tmp = int(map_choice)
                        if tmp >= nmaps or tmp < 0:
                            print("+++ERROR: {} out of range".format(tmp))
                        else:
                            map_id = tmp
                            state = 1
                             
                    except:
                        print("+++ ERROR: {} not a valid number".format(map_choice))
                continue
            elif choice == "8":
                config.add_new_blank_mapping()
                map_id = config.get_mapping_len()
                state = 0
                continue
            elif choice == "9":
                nmaps = config.get_mapping_len()
                del_map = raw_input("Select mapping to be deleted [0-{}]".format(nmaps))
                try:
                    tmp = int(del_map)
                    if tmp >= nmaps or tmp < 0:
                        print("+++ERROR: {} out of range".format(tmp))
                    else:
                        yes_no = raw_input("Are you sure to delete mapping {}? [y/n]".format(tmp))
                        if yes_no == y:
                            config.delete_mapping(tmp)
                            map_id = 0
                         
                except:
                    print("+++ ERROR: {} not a valid number".format(map_choice))
                continue

            elif choice == "10":
                config.list_mappings()
                continue

            elif choice == "99":
                config.save_config()
                return 1
        elif state == 1:
            if choice == "1":
                config.print_mapping(map_id)
                continue
            elif choice == "2":
                state = 2
                continue
            elif choice == "3":
                state = 3
                continue
            elif choice == "4":
                description = config.get_mapping_description(map_id)
                print("Current description: {}".format(description))
                new_desc = raw_input("New Description: ")
                yes_no = raw_input("Do you want to set description to '{}'?[y/n]".format(new_desc))
                if yes_no == 'y':
                    config.set_mapping_description(map_id, new_desc)
                continue

            elif choice == "0":
                state = 0
                continue
        elif state == 2:
            if choice == "0":
                state = 1
                continue
            elif choice == "1":
                config.print_panel_configuration(map_id,'sidebuttons')
                continue
            elif choice == "2":
                button_choice = raw_input("Select button [01-12]: ")
                try:
                    tmp = int(button_choice)
                    if tmp > 12 or tmp < 0:
                        print("+++ERROR: {} out of range".format(tmp))
                        continue
                    elif len(button_choice) != 2:
                        print("+++ERROR: button must have dd format")
                        continue
                except:
                    print("+++ERROR: invalid input -> {}".format(button_choice))
                    continue
                config.print_button_mapping(map_id,'sidebuttons',button_choice)
                continue
            elif choice == "3":
                print("Not defined")
                continue
            elif choice == "4":
                button_choice = raw_input("Select button [01-12]: ")
                try:
                    tmp = int(button_choice)
                    if tmp > 12 or tmp < 0:
                        print("+++ERROR: {} out of range".format(tmp))
                        continue
                    elif len(button_choice) != 2:
                        print("+++ERROR: button must have dd format")
                        continue
                except:
                    print("+++ERROR: invalid input -> {}".format(button_choice))
                    continue
                state = 4
                continue

        elif state == 3:
            if choice == "0":
                state = 1
                continue
            elif choice == "1":
                config.print_panel_configuration(map_id,'frontbuttons')
                continue
            elif choice == "2":
                print "[01] : BTN_EXTRA"
                print "[02] : BTN_SIDE"
                button_choice = raw_input("Select button [01-02]: ")
                try:
                    tmp = int(button_choice)
                    if tmp > 2 or tmp < 0:
                        print("+++ERROR: {} out of range".format(tmp))
                        continue
                    elif len(button_choice) != 2:
                        print("+++ERROR: button must have dd format")
                        continue
                    config.print_button_mapping(map_id,'frontbuttons',button_choice)
                except:
                    print("+++ERROR: invalid input -> {}".format(button_choice))
                    continue
                continue
            elif choice == "3":
                print("Not defined")
                continue
            elif choice == "4":
                print "[01] : BTN_EXTRA"
                print "[02] : BTN_SIDE"
                button_choice = raw_input("Select button [01-02]: ")
                try:
                    tmp = int(button_choice)
                    if tmp > 2 or tmp < 0:
                        print("+++ERROR: {} out of range".format(tmp))
                        continue
                    elif len(button_choice) != 2:
                        print("+++ERROR: button must have dd format")
                        continue
                except:
                    print("+++ERROR: invalid input -> {}".format(button_choice))
                    continue
                state = 5
                continue

        elif state == 4:
            if choice == "0":
                state = 2
                continue
            elif choice == "1":
                config.print_button_mapping(map_id,'sidebuttons',button_choice)
                continue
            elif choice == "2":
                config.delete_action(map_id, 'sidebuttons', button_choice)
                continue
            elif choice == "3":
                key_combination = raw_input("Enter key combination: ")
                action = [{ 
                    "type"   : "key",
                    "action" : key_combination
                }]
                config.add_action(map_id,'sidebuttons',button_choice, action)
                continue
            elif choice == "4":
                print "[1] : left"
                print "[2] : middle"
                print "[3] : right"                 
                click_choice = raw_input("Select button: ")
                try:
                    tmp = int(click_choice)
                except:
                    print("+++ERROR: invalid input -> {}".format(click_choice))
                    continue
                if tmp == 1:
                    click_action = 'left'
                elif tmp == 2:
                    click_action = 'middle'
                elif tmp == 3:
                    click_action = 'right'
                else:
                    print("+++ERROR: {} out of range".format(tmp))
                    continue

                action = [{ 
                    "type"   : "key",
                    "action" : click_action
                }]
                config.add_action(map_id,'sidebuttons',button_choice, action)
                continue
            elif choice == "5":
                x = raw_input("Enter X position: ")
                y = raw_input("Enter Y position: ")
                if isInt(x) and isInt(y):
                    action = [{
                        "type" : "position",
                        "x"    : x,
                        "y"    : y
                    }]
                    config.add_action(map_id,'sidebuttons',button_choice,action)
                else:
                    print("+++ERROR: position not valid")
                continue
            elif choice == "6":
                program = raw_input("Executable program with complete path: ")
                action = [{
                    "type" : "run",
                    "command" : program
                }]
                yes_no = raw_input("Do you want to set the user for this program? [y/n]: ")
                if yes_no == "y":
                    new_user = raw_input("username: ")
                    action[0]['user'] = new_user
                yes_no = raw_input("Does the program use parameters? [y/n]")
                if yes_no == "y":
                    parameters = []
                    while True:
                        new_param = raw_input("Enter parameter: ")
                        parameters.append(new_param)
                        yes_no = raw_input("Do you want to enter another parameter? [y/n]: ")
                        if yes_no != "y":
                            break
                    action[0]['params'] = parameters
                config.add_action(map_id, 'sidebuttons', button_choice, action)
            elif choice == "7":
                config.add_action(map_id,'sidebuttons', button_choice, [{ 'type' : 'toggle'}])
            elif choice == "99":
                print "not defined"
























if __name__ == "__main__":
    main(sys.argv[1:])