import math
import smbus2

ENCODER_ADDRESS = 0x34

class MotorController:
    def __init__(self, i2c_port, motor_type=3):
        self.i2c_port = i2c_port
        with smbus2.SMBus(self.i2c_port) as bus:
            bus.write_i2c_block_data(ENCODER_ADDRESS, 20, [motor_type, ])

    def set_speed(self, speed, motor_id=None, offset=0):
        with smbus2.SMBus(self.i2c_port) as bus:
            try:
                if motor_id is None:
                    bus.write_i2c_block_data(ENCODER_ADDRESS,
                                             51 + offset, speed)
                elif 0 < motor_id <= 4:
                    bus.write_i2c_block_data(ENCODER_ADDRESS,
                                             50 + motor_id, [speed, ])
                else:
                    raise ValueError("Invalid motor id")

            except Exception as e:
                print(e)

class Chassis:
    def __init__(self, a=110, b=97.5, wheel_diam=96.5, pulse_per_cyc=44*178):
        self.a = a
        self.b = b
        self.wheel_diam = wheel_diam
        self.pulse_per_cyc = pulse_per_cyc
        self.mc = MotorController(1)

    def convert_to_pulse(self, speed):
        """
        Converts speed from mm/s to pulse/10ms

        :param speed:
        :return:
        """
        return speed / (math.pi * self.wheel_diam) * self.pulse_per_cyc * 0.01

    def set_velocity(self, lin_vel, dir, angular_velocity):
        """
        Set velocity by polar coordinates

        :param linear_velocity: the linear velocity in mm/s, tuple of mag and dir
        :param angular_velocity: the angular velocity in rad/s
        :return:
        """
        r, theta = lin_vel, dir
        theta = math.radians(theta) # convert to radians

        # compute x, y, and peripheral velocity
        v_x = -r * math.cos(theta) 
        v_y = -r * math.sin(theta)
        v_p = -angular_velocity * (self.a + self.b)

        # compute the wheel velocities (mm/s)
        v_1 = v_y - v_x + v_p 
        v_2 = v_y + v_x - v_p
        v_3 = v_y - v_x - v_p
        v_4 = v_y + v_x + v_p

        # gather velocities in correct motor order
        v_s = [v_1, -v_4, -v_2, v_3]

        # set wheel speeds
        self.mc.set_speed([int(self.convert_to_pulse(v)) for v in v_s])

    def stop(self):
        """
        Stop all of the motors from moving

        :return:
        """
        self.mc.set_speed([0, 0, 0, 0])
