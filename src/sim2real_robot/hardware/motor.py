"""
Stepper Motor interface for controlling a stepper motor.

This module provides an interface to control a stepper motor via UART.
# Tested with motor SM-42BYG011-25 from Mercury using a DRV8825 stepper driver.
"""

import serial
import time
import struct
import threading
import RPi.GPIO as GPIO
import time
import sys
import math

from spikes.run_motor import DEGREES_PER_STEP

# Degrees per step for motor is 1.8 degree
# With microstepping 1/4 this is the RAD value
RAD_PER_STEP = 0.00785

# Max speed in rad/second
MAX_SPEED = 20.0


class StepperMotor:
    """Stepper Motor class to interface with the stepper motor."""

    def __init__(self, step_pin, dir_pin, enable_pin):
        """Initialize the Stepper Motor with the given GPIO pins."""
        self._step_pin = step_pin
        self._dir_pin = dir_pin
        self._enable_pin = enable_pin

        self._thread = None
        self._running = False
        
        # setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._step_pin, GPIO.OUT)
        GPIO.setup(self._dir_pin, GPIO.OUT)
        GPIO.setup(self._enable_pin, GPIO.OUT)
        
        # Initialize pins
        GPIO.output(self._step_pin, GPIO.LOW)
        GPIO.output(self._dir_pin, GPIO.LOW)
        GPIO.output(self._enable_pin, GPIO.HIGH) #turned off
        
        self._direction = 1  # 1 for forward, -1 for backward

        # Delay between steps.
        # Because each step requires pulling pin high and low, the total step period is 2 * step_delay. So step_delay is half the step period.
        self._step_delay = 0.0

    # ==================== PUBLIC API ====================

    def start(self):
        """Start the motor"""
        if self._running:
            print("[WARN] IMU thread already running")
            return
        
        self._running = True
        GPIO.output(self._enable_pin, GPIO.LOW)  # Enable the motor
        self._thread = threading.Thread(target=self._run_motor, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop the motor."""
        if not self._running:
            return
        
        GPIO.output(self._enable_pin, GPIO.HIGH)  # Disable the motor
        self._running = False
        if self._thread is not None:
            self._thread.join(timeout=1.0)

    def set_speed(self, speed_rad_per_sec):
        """Set the motor speed in radians per second."""
        #clamp speed to max
        clamped_speed = max(-MAX_SPEED, min(speed_rad_per_sec, MAX_SPEED))

        if clamped_speed < 0:
            self._direction = -1
            clamped_speed = -clamped_speed
        else:
            self._direction = 1
       
        GPIO.output(self._dir_pin, GPIO.HIGH if self._direction == 1 else GPIO.LOW)

        if clamped_speed > 0:
            step_frequency = clamped_speed / RAD_PER_STEP  # steps per second
            self._step_delay = 0.5 / step_frequency  # delay for half the step period
        else:
            self._step_delay = 0.0

    # ==================== PRIVATE IMPLEMENTATION ====================
    def _run_motor(self):
        """Background thread that continuously send stepper signals."""
        next_step = time.perf_counter()

        while self._running:
            now = time.perf_counter()    

            if self._step_delay > 0 and now >= next_step:
                # Send step pulse - high for step_delay, then low for step_delay
                GPIO.output(self._step_pin, GPIO.HIGH)
                time.sleep(self._step_delay)
                GPIO.output(self._step_pin, GPIO.LOW)
                time.sleep(self._step_delay)

                next_step += 2 * self._step_delay  # Schedule next step

            # Sleep a bit to avoid busy waiting, but not too long to maintain responsiveness
            time.sleep(0.001)

def main():
    """Main function for testing the stepper motor."""

    STEP_PIN = 17
    DIR_PIN = 27
    ENABLE_PIN = 22

    motor = StepperMotor(STEP_PIN, DIR_PIN, ENABLE_PIN)

    motor.start()
    motor.set_speed(5.0)  # Set speed to 5 rad/s
    time.sleep(10)
    motor.set_speed(-5.0)  # Set speed to 5 rad/s
    time.sleep(10)
    motor.stop()

if __name__ == "__main__":
    main()