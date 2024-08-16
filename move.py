import time
from chassis_control import *

def main():
    chassis = Chassis()

    chassis.set_velocity(-50, 90, 0)
    time.sleep(1)

    chassis.stop()

if __name__ == '__main__':
    main()

