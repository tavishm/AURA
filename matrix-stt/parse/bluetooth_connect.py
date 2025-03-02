import os
import subprocess
from evdev import InputDevice


def connect_bt():
    while True:
        subprocess.check_output(
            'bash ' + os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 'bluetooth_connect.sh'
            ), shell=True
        )
        try:
            bldevice = InputDevice('/dev/input/event0')
        except FileNotFoundError:
            continue
        except PermissionError:
            return 'success'
        break


if __name__ == '__main__':
    connect_bt()
