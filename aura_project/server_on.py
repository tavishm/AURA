import os
import threading
t1 = threading.Thread(target = os.system, args=('python3.7 display_server.py',))
t2 = threading.Thread(target = os.system, args=('python3.7 motor_receiver_server.py',))
t1.start()
t2.start()

