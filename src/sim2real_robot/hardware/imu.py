"""
IMU (Inertial Measurement Unit) interface for BNO055 sensor.

This module provides an interface to the BNO055 9-DOF IMU sensor via UART.
"""

import serial
import time
import struct


class IMU:
    """IMU class to interface with the BNO055 sensor via UART."""

    def __init__(self, port="/dev/serial0", baudrate=115200):
        """Initialize the IMU with the given UART port."""
        self.available = False
        try:
            self.ser = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=0.1
            )
            time.sleep(0.7)
            
            self.ser.reset_input_buffer()
            self._initialize()
            self.available = True
        except Exception as e:
            print(f"Warning: Could not initialize BNO055 IMU: {e}")
            self.available = False

    def _write(self, reg, value):
        """Write a register to the BNO055."""
        if not self.available:
            return
        packet = bytes([0xAA, 0x00, reg, 0x01, value])
        self.ser.write(packet)
        self.ser.flush()
        time.sleep(0.002)

    def _read(self, reg, length):
        """Read registers from the BNO055."""
        if not self.available:
            return None
        self.ser.write(bytes([0xAA, 0x01, reg, length]))
        self.ser.flush()
        time.sleep(0.002)

        header = self.ser.read(2)

        if len(header) != 2 or header[0] != 0xBB:
            print("[ERR]   Invalid header")
            return None

        reported_length = header[1]
        if reported_length != length:
            print(f"[WARN]   Response length {reported_length} != requested {length}")

        data = self.ser.read(reported_length)

        if len(data) != reported_length:
            print("[ERR]   Incomplete data")
            return None

        return data

    def _initialize(self):
        """Initialize the BNO055 sensor in NDOF mode."""
        # Switching to CONFIGMODE
        self._write(0x3D, 0x00)
        time.sleep(0.02)

        # Setting power mode NORMAL
        self._write(0x3E, 0x00)

        # Clearing SYS_TRIGGER
        self._write(0x3F, 0x00)

        #Selecting PAGE 0
        self._write(0x07, 0x00)

        # Apply remap
        self._write(0x41, 0x06)   # X=Z, Y=Y, Z=X
        self._write(0x42, 0x02)   # Flip Y

        # Switching to NDOF mode
        self._write(0x3D, 0x0C)
        time.sleep(1.0)

    def get_euler(self):
        """Get the current Euler angles (heading, roll, pitch) from the IMU in degrees."""
        if not self.available:
            return None

        try:
            data = self._read(0x1A, 6)
            if data is not None:
                heading, roll, pitch = struct.unpack("<hhh", data)
                scale = 1.0 / 16.0
                return heading * scale, roll * scale, pitch * scale
        except Exception as e:
            print(f"Warning: Could not read Euler angles from IMU: {e}")
        return None

    def get_pitch_angle(self):
        """Get the current pitch angle from the IMU."""
        if not self.available:
            return 0.0

        try:
            euler = self.get_euler()
            if euler is not None:
                return euler[1]  # euler[1] corresponds to pitch
        except Exception as e:
            print(f"Warning: Could not read pitch angle from IMU: {e}")
        return 0.0

    def get_angular_velocity(self):
        """Get the current angular velocity (gyroscope data) from the IMU in deg/s."""
        if not self.available:
            return None

        try:
            data = self._read(0x14, 6)
            if data is not None:
                gyr_x, gyr_y, gyr_z = struct.unpack("<hhh", data)
                scale = 1.0 / 16.0  # BNO055 gyroscope scale factor
                return gyr_x * scale, gyr_y * scale, gyr_z * scale
        except Exception as e:
            print(f"Warning: Could not read angular velocity from IMU: {e}")
        return None

    def get_pitch_angular_velocity(self):
        """Get the current pitch angular velocity from the IMU in deg/s."""
        if not self.available:
            return 0.0

        try:
            angular_velocity = self.get_angular_velocity()
            if angular_velocity is not None:
                return angular_velocity[1]  # gyr_x corresponds to pitch rate
        except Exception as e:
            print(f"Warning: Could not read pitch angular velocity from IMU: {e}")
        return 0.0

    def get_calibration_status(self):
        """Get the calibration status of the IMU."""
        if not self.available:
            return None

        try:
            data = self._read(0x35, 1)
            if data is not None:
                calib = data[0]
                acc = calib & 0x03  # bits 0-1
                mag = (calib >> 2) & 0x03  # bits 2-3
                gyr = (calib >> 4) & 0x03  # bits 4-5
                sys = (calib >> 6) & 0x03  # bits 6-7
                return acc, mag, gyr, sys
        except Exception as e:
            print(f"Warning: Could not read calibration status from IMU: {e}")
        return None


if __name__ == "__main__":
    # Initialize the IMU sensor
    imu = IMU()

    if not imu.available:
        print("[ERR] IMU not available. Exiting.")
        exit(1)

    # Check calibration status
    calib = imu.get_calibration_status()
    if calib is not None:
        acc_calib, mag_calib, gyr_calib, sys_calib = calib
        print(f"[DBG] Calibration status: Acc={acc_calib}, Mag={mag_calib}, Gyr={gyr_calib}, Sys={sys_calib}")
    else:
        print("[ERR] Failed to read calibration status")

    # Main loop: read and print Euler angles and angular velocity
    print("[DBG] Starting Euler and angular velocity read loop...")
    try:
        while True:
            pitch = imu.get_pitch_angle()
            pitch_angular_velocity = imu.get_pitch_angular_velocity()
            if pitch is not None and pitch_angular_velocity is not None:
                print(f"Pitch: Angle={pitch:+07.2f}°, AngularVel={pitch_angular_velocity:+07.2f}°/s")
            else:
                print("[ERR] Failed to read pitch data")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n[DBG] Exiting...")

