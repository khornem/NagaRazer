This program allows mapping buttons of razer naga classic mouse. The mapping will allow:
* Execution simple action:
** key or combination of key actions
** click action (left, middle and right mouse buttons)
** run a program (it may be run as any user defined in the system)
** move the mouse cursor
* Execute multiple simple actions in a defined order.
** This feature allows building macros

Sidebutton actions are overrided by the program, but extra buttons in front of the button are not. These buttons will execute default action plus the programmed action (I was not able to grab only those buttons and not normal buttons)

The main program is written in python, and it is based in the idea and program of Apocatarsis, which you may find in:
* https://www.reddit.com/r/razer/comments/37yc3y/tutorial_remapping_naga_side_keyboard_numpad_in/
* https://github.com/apocatarsis/Naga_KeypadMapper

It uses evdev package to handle mouse events.


# Installation instructions

The following packages must be installed:
* python-dev
* python package evdev
* xdotool
* libudev-dev

The following files are used:
* <code>/usr/local/bin/NagaConfigurator.py</code>  
* <code>/usr/local/bin/naga_razer.py</code> : this code must be modified to change default user 
* <code>/usr/local/bin/udev-naga.sh.py</code>  : this code must be modified to change default user
* <code>/etc/udev/rules.d/40-mouse-razer.rules</code>  
* <code>$HOME/.config/NagaRazer/naga_config.json</code>  : this code must be modified to change default user

A simple installation script has been programmed to make all these action, including changing default username (miguel) to the local username. 

```
sudo ./install.sh <username>
```



# Configuration file format

Mapping file is based in json format, which allows easy parsing and feature adding.

Mapping file must be named <code>naga_config.json</code> and the default file location should be <code>$HOME/.config/NagaRazer</code>

This is a configuration file example:
```json
{
  "properties": {
    "name": "naga razer",
    "devices": {
      "sidebuttons": "/dev/input/by-id/usb-Razer_Razer_Naga-if01-event-kbd",
      "frontbuttons": "/dev/input/by-id/usb-Razer_Razer_Naga-event-mouse"
    },
    "user": "miguel"
  },
  "mappings": [
    {
      "description": "mapping for Linux",
      "id": 1,
      "sidebuttons": {
        "01": [
          {
            "type": "key",
            "action": "ctrl+Super_L+Left"
          }
        ],
        "02": [
          {
            "type": "key",
            "action": "shift+Insert"
          }
        ],
        "03": [
          {
            "type": "key",
            "action": "ctrl+Super_L+Right"
          }
        ],
        "04": [
          {
            "type": "key",
            "action": "Shift_L+ctrl+Alt_L+Left"
          }
        ],
        "06": [
          {
            "type": "key",
            "action": "Shift_L+ctrl+Alt_L+Right"
          }
        ],
        "07": [
          {
            "type": "run",
            "command": "gnome-terminal",
            "params": [
              "--geometry=100x40"
            ]
          }
        ],
        "09": [
          {
            "type": "run",
            "user": "root",
            "command": "wireshark"
          }
        ],
        "12": [
          {
            "type": "toggle"
          }
        ]
      },
      "frontbuttons": {
        "BTN_EXTRA": [
          {
            "type": "run",
            "command": "gnome-terminal",
            "params": [
              "--geometry=100x40"
            ]
          }
        ],
        "BTN_SIDE": []
      }
    },
    {
      "description": "mapping for visio",
      "id": 1,
      "sidebuttons": {
        "01": [
          {
            "type": "key",
            "action": "ctrl+Insert"
          }
        ],
        "02": [
          {
            "type": "key",
            "action": "shift+Insert"
          }
        ],
        "03": [
          {
            "type": "key",
            "action": "Alt"
          },
          {
            "type": "key",
            "action": "4"
          },
          {
            "type": "key",
            "action": "L"
          }
        ],
        "04": [
          {
            "type": "key",
            "action": "alt+4+L"
          }
        ],
        "12": [
          {
            "type": "toggle"
          }
        ]
      }
    }
  ]
}
```


## Mapping properties

* **name**: administrative name assigned to the mouse
* **devices** : path to devices assigned to the mouse
 * **sidebuttons** : path to numeric sidebuttons. It is preferrable to use <code>/dev/input/by-id/</code> symbolic links
 * **frontbuttons** : path to extra buttons (these buttons are not implemented right now)
* **user** : user which will be used to run programs by default
* **default_mapping** : mapping which will be used when the program starts (note that first mapping is 0)


## Mappings

There may be as many mappings as you want. Each mapping may have the following attributes:

* **description** : it is an administrative name for the mapping (it will be used to notify the user which mapping is being used when there is a mapping toggle)
* **id** : an integer. It is not being used right now
* **sidebuttons|frontbuttons**: specific mapping of each button set. If a button is not mapped it will use the default action.

## Button mappings

Buttons are defined after the number they are labelled with.
* **sidebuttons** are labelled from 01 to 12 (I used dd notation to ease sorting)
* **frontbuttons** are labelled after names defined in <code>/usr/include/linux/input.h</code>
 * BTN_EXTRA
 * BTN_SIDE

For each button mapping several actions may be taken, so macros may be built.

### Key action

* **type** : 'key'
* **action** : key or keys combination. They must be defined to be interpreted by xdotool (X keysym) and are case sensitive

### click action

* **type** : 'click'
* **button** : {'left'|'middle'|'right'}

### position action

It moves mouse cursor to the specifed position. Coordinates center is in the left above corner.

* **type** : 'position'
* **'x'** : x coordinate
* **'y'** : y coordinate

### run action

It executes a program:

* **type** : 'run'
* **user** : this is an optional parameter. If used it specifies which user will be used to execute the program. If the user does not have X11 privileges the program will not work. (This parameter is used to run programs as root, like wireshark)
* **command** : name of the executable program
* **params** : Optional parameter. Ordered list of all parameters passed to the program

### Toggle action

It changes button mappings to the next one in a round robin fashion.


# PENDING ACTIONS

## udev rule
I have not been able to make udev rule work properly. It is executed five times. I have tried several configuration found on the web but none of them worked.

As a workaround I have used this [solution](http://stackoverflow.com/questions/19937584/udev-rule-runs-bash-script-multiple-times).

## NagaConfigurator.py

This script is very limited and does not allow complex actions like inserting actions in the middle of a macro.

Code should be modularized. 

## naga_razer.py

Although sidebuttons perform only configured action, extra buttons perform both default action and new configured one.

The script grabs side buttons device, so all events are managed by it. However, if script grabs front buttons device then it will have to handle regular mouse buttons, and it is not a good option. I have not found another way to override extra button mapping with this script.

## Macro recorder

It is in my mind to make a simple macro recorder, but it is not a priority right now.
