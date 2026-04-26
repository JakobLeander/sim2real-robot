
from sim2real_robot.robot_control_gpio import RobotControlGPIO
from sim2real_robot.robot_control_sim import RobotControlSim


class RobotRunner:
    def __init__(self, backend: str = "gpio"):
        if backend == "gpio":
            self.robot_control = RobotControlGPIO()
        elif backend == "sim":
            self.robot_control = RobotControlSim()
        else:
            raise ValueError(f"Unknown backend: {backend}. Supported backends: 'gpio', 'sim'")

    def run(self):
        # Example of using the robot control interface to get pitch angle
        pitch_angle = self.robot_control.get_pitch_angle()
        print(f"Current pitch angle: {pitch_angle} degrees")

if __name__ == "__main__":
    runner = RobotRunner(backend="sim")  # Change to "sim" for simulation or "gpio" for real hardware
    runner.run()

