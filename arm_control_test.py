import rospy
from kinematics import ik_transform
from armpi_pro import bus_servo_control
from hiwonder_servo_msgs.msg import MultiRawIdPosDur, RawIdPosDur

def main():
    rospy.init_node('servo_control_test', anonymous=True)

    # Set shutdown procedure
    def shutdown(signum, frame):
        rospy.loginfo('shutdown')
        rospy.signal_shutdown('shutdown')

    # On recieving SIGINT (like a KeyboardInterrupt) call shutdown()
    signal.signal(signal.SIGINT, shutdown) 

    # The publisher for raw input servo control
    joints_pub = rospy.Publisher(
        '/servo_controllers/port_id_1/multi_id_pos_dur', 
        MultiRawIdPosDur, queue_size=1)

    # Wait a moment for changes to take effect
    rospy.sleep(0.3)

    # Solve inverse kinematics to get ranges for each servo
    ik = ik_transform.ArmIK()
    target = ik.set Pitch Ranges((0.0, 0.15, 0.07), -90, -180, 0)
    servo_data = target[1]

    # Only servos 3-6 are set because 1 and 2 only control the rotation and grasping of the claw
    bus_servo_control.set_servos(joints_pub, 1, 
        ((3, servo_data['servo3']),
         (4, servo_data['servo4']),
         (5, servo_data['servo5']),
         (6, servo_data['servo6'])))

    # Wait until movement is done (1 second, as set in set_servos)
    rospy.sleep(1)

if __name__ == '__main__':
    main()
