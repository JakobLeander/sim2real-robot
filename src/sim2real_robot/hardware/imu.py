"""
IMU (Inertial Measurement Unit) interface for BNO055 sensor.

This module provides an interface to the Adafruit BNO055 9-DOF IMU sensor,
which includes an accelerometer, gyroscope, and magnetometer.
"""

import adafruit_bno055
import board
import busio

class IMU:
    """
    IMU class to interface with the BNO055 sensor.

    This class provides methods to read orientation and motion data from the
    BNO055 sensor, which can be used for robot control and navigation.
    """

    def __init__(self):
        """
        Initialize the IMU with the given I2C interface.

        Args:
            i2c: An instance of an I2C interface (e.g., from board.I2C()).
        """
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            self.imu = adafruit_bno055.BNO055_I2C(i2c)
            self.available = True
            print("BNO055 IMU initialized successfully")
        except Exception as e:
            print(f"Warning: Could not initialize BNO055 IMU: {e}")
            self.imu = None
            self.available = False

    def get_pitch_angle(self) -> float:
        """
        Get the current pitch angle from the IMU.

        Returns:
            float: The pitch angle in degrees, where positive values indicate
                   forward tilt and negative values indicate backward tilt.
        """
        if not self.available or self.imu is None:
            return 0.0

        try:
            euler = self.imu.euler
            if euler is not None:
                return euler[1]  # euler[1] corresponds to pitch
            else:
                return 0.0
        except Exception as e:
            print(f"Warning: Could not read pitch angle from IMU: {e}")
            return 0.0

if __name__ == "__main__":
    # test blinka
    print("Board ID:", board.board_id)
    
    print("Testing IMU...")
    try:
        imu = IMU()
        if imu.available:
            pitch = imu.get_pitch_angle()
            print(f"IMU test successful! Current pitch angle: {pitch:.2f} degrees")
        else:
            print("IMU hardware not available or not connected")
    except Exception as e:
        print(f"Error during IMU test: {e}")