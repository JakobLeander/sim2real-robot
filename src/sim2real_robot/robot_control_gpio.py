from .robot_control_interfaces import RobotControl
from .hardware.imu import IMU
from .hardware.motor import StepperMotor


class RobotControlGPIO(RobotControl):
    def __init__(self):
        super().__init__()

        self._imu = IMU()  # Initialize the IMU sensor
        self._left_motor = StepperMotor(step_pin=17, dir_pin=27, enable_pin=22, reverse_direction=False)  # Initialize left motor
        self._right_motor = StepperMotor(step_pin=23, dir_pin=24, enable_pin=25, reverse_direction=True)  # Initialize right motor


    def get_pitch_angle(self) -> float:
        # Implement GPIO-based method to read pitch angle
        # Placeholder implementation
        pitch_angle = self._imu.pitch_angle  # Get pitch angle from IMU
        return pitch_angle

    def start_robot(self):
        # Implement GPIO-based method to start the robot
        self._imu.start()  # Start IMU reading thread
        self._left_motor.start()  # Start left motor
        self._right_motor.start()  # Start right motor

    def stop_robot(self):
        # Implement GPIO-based method to stop the robot
        self._imu.stop()  # Stop IMU reading thread
        self._left_motor.stop()  # Stop left motor
        self._right_motor.stop()  # Stop right motor

