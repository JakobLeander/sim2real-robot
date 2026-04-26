from .robot_control_interfaces import RobotControl
from .hardware.imu import IMU

class RobotControlGPIO(RobotControl):
    def __init__(self):
        super().__init__()

        self.imu = IMU()  # Initialize the IMU sensor

    def get_pitch_angle(self) -> float:
        # Implement GPIO-based method to read pitch angle
        # Placeholder implementation
        pitch_angle = self.imu.get_pitch_angle()  # Get pitch angle from IMU
        return pitch_angle


    