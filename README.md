This program allows mapping buttons of razer naga classic mouse. The mapping will allow:
* Execution simple action:
** key or combination of key actions
** click action (left, middle and right mouse buttons)
** run a program (it may be run as any user defined in the system)
** move the mouse cursor
* Execute multiple simple actions in a defined order.
** This feature allows building macros

The main program is written in python, and it is based in the idea of Apocatarsis, which you may find in:
* https://www.reddit.com/r/razer/comments/37yc3y/tutorial_remapping_naga_side_keyboard_numpad_in/
* https://github.com/apocatarsis/Naga_KeypadMapper

It uses evdev package to handle mouse events.

# Mapping format

Mapping file is based in json format, which allows easy parsing and feature adding.

This is json example:
```
{
    "properties" : {
        "name" : "naga razer",
        "devices" : {
            "sidebuttons" : "/dev/input/by-id/usb-Razer_Razer_Naga-if01-event-kbd",
            "frontbuttons" : "/dev/input/event11"

        },
        "user" : "miguel"

    },
    "mappings" : [
        {
            "description" : "mapping for windows",
            "id" : 1,
            "sidebuttons" : {
                "KEY_1" : [
                    {
                        "type"   : "key",
                        "action" : "ctrl+Insert"
                    }
                ],
                "KEY_2" : [
                    {
                        "type"   : "key",
                        "action" : "shift+Insert"
                    }
                ],
                "KEY_3" : [
                    {
                        "type"   : "key",
                        "action" : "Alt"
                    },
                    {
                        "type"   : "key",
                        "action" : "4"
                    },
                    {
                        "type"   : "key",
                        "action" : "L"
                    }
                ],
                "KEY_4" : [
                    {
                        "type"   : "key",
                        "action" : "alt+4+L"
                    }
                ],
                "KEY_5" : [
                    {
                        "type"   : "click",
                        "button" : "right"
                    }
                ],
                "KEY_6" : [
                    {
                        "type"   : "position",
                        "x" : "200",
                        "y" : "1079"
                    }
                ],
                "KEY_7" : [
                    {
                        "type"   : "run",
                        "user"   : "satec",
                        "command" : "gnome-terminal",
                        "params" : [
                            "--geometry=40x40",
                            "--working-directory=/tmp"
                        ]
                    }
                ],
                "KEY_8" : [
                    {
                        "type"   : "run",
                        "user"   : "root",
                        "command" : "wireshark"
                    }
                ],
                "KEY_EQUAL" : [
                    {
                        "type"   : "toggle"
                    }
                ]
            }

        },
        {
            "description" : "mapping for visio",
            "id" : 1,
            "sidebuttons" : {
                "KEY_1" : [
                    {
                        "type"   : "key",
                        "action" : "ctrl+Insert"
                    }
                ],
                "KEY_2" : [
                    {
                        "type"   : "key",
                        "action" : "shift+Insert"
                    }
                ],
                "KEY_3" : [
                    {
                        "type"   : "key",
                        "action" : "Alt"
                    },
                    {
                        "type"   : "key",
                        "action" : "4"
                    },
                    {
                        "type"   : "key",
                        "action" : "L"
                    }
                ],
                "KEY_4" : [
                    {
                        "type"   : "key",
                        "action" : "alt+4+L"
                    }
                ],
                "KEY_EQUAL" : [
                    {
                        "type"   : "toggle"
                    }
                ]
            }

        }
    ]
}
```


## Mapping properties

* name: administrative name assigned to the mouse
* devices : path to devices assigned to the mouse
** sidebuttons : path to numeric sidebuttons. It is preferrable to use /dev/input/by-id/ symbolic links
** frontbuttons : path to extra buttons (these buttons are not implemented right now)
* user : user which will be used to run programs by default
* default_mapping : mapping which will be used when the program starts (note that first mapping is 0)


## Mappings

There may be as many mappings as you want. Each mapping may have the following attributes:

* description : it is an administrative name for the mapping (it will be used to notify the user which mapping is being used when there is a mapping toggle)
* id : an integer. It is not being used right now
* sidebuttons|frontbuttons: specific mapping of each button set. If a button is not mapped it will use the default action.

## Button mappings

Buttons must be named as defined in /usr/include/linux/input.h, because evdev takes the names from it (e.g: KEY_1, KEY_MINUS).

For each button mapping several actions may be taken. This allows to make macros.

### Key action

* type : 'key'
* action : key or keys combination. They must be defined to be interpreted by xdotool (X keysym) and are case sensitive

### click action

* type : 'key'
* button : {'left'|'middle'|'right'}

### position action

It moves mouse cursor to the specifed position. Coordinates center is in the left above corner.

* type : 'position'
* 'x' : x coordinate
* 'y' : y coordinate

### run action

It executes a program:

* type : 'run'
* user : this is an optional parameter. If used it specifies which user will be used to execute the program. If the user does not have X11 privileges the program will not work. (This parameter is used to run programs as root, like wireshark)
* command : name of the executable program
* params : Optional parameter. Ordered list of all parameters passed to the program


