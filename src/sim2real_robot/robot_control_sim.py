from sim2real_robot.robot_control_interfaces import RobotControl


class RobotControlSim(RobotControl):
    def __init__(self):
        super().__init__()

    def get_pitch_angle(self) -> float:
        return 0.0  # Placeholder for simulated pitch angle


    