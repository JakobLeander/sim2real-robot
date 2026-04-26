"""
Robot control interfaces for sim2real robot systems.

This module defines abstract interfaces for robot control systems,
providing a standardized way to interact with different robot implementations
in simulation and real-world environments.
"""

from abc import ABC, abstractmethod


class RobotControl(ABC):
    """
    Abstract base class for robot control interfaces.

    This interface defines the contract that all robot control implementations
    must follow. It provides methods for accessing robot state information
    such as orientation and position data.
    """

    @abstractmethod
    def get_pitch_angle(self) -> float:
        """
        Get the current pitch angle of the robot.

        Returns:
            float: The pitch angle in radians, where positive values indicate
                   forward tilt and negative values indicate backward tilt.
        """
        pass