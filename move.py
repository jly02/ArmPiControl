import time
from chassis_control import *

def main():
    v_s = [-10, 10, 10, -10]

    chassis = Chassis()

    """
    direction = 0
    for i in range(9):
        theta = direction + i * 45
        chassis.set_velocity((10, theta), 0)
        time.sleep(1)
    """

    chassis.set_velocity((-50, 90), 0)
    time.sleep(1)

    chassis.stop()

if __name__ == '__main__':
    main()

