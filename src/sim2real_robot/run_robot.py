
from sim2real_robot.robot_control_gpio import RobotControlGPIO
from sim2real_robot.robot_control_sim import RobotControlSim
import time


class RobotRunner:
    CONTROL_RATE_HZ = 100
    DT = 1/CONTROL_RATE_HZ

    def __init__(self, backend: str = "gpio"):
        if backend == "gpio":
            self.robot_control = RobotControlGPIO()
        elif backend == "sim":
            self.robot_control = RobotControlSim()
        else:
            raise ValueError(f"Unknown backend: {backend}. Supported backends: 'gpio', 'sim'")

    def write_debug(self, text: str):
        print(text, flush=True, end="\r")

    def update(self):
        # TODO: Update robot state and control logic here
        pass


    def run(self):
        fps_count = 0
        fps_time_start = time.time()
        fps_elapsed = 0.0
        next_time = time.perf_counter()

        try:
            self.robot_control.start_robot()

            while True:
                now = time.perf_counter()

                if now>=next_time:
                    self.update()  # Update robot state

                    fps_count += 1
                    fps_elapsed = time.time() - fps_time_start
                    if fps_elapsed >= 1.0:
                        fps = fps_count / fps_elapsed
                        self.write_debug(f"Control loop FPS: {fps:.1f} Hz")
                        fps_count = 0
                        fps_time_start = time.time()

                    next_time += self.DT
                time.sleep(0.001)                
                
                


        finally:
            self.robot_control.stop_robot()
            print("\nRobot stopped. Exiting.")

if __name__ == "__main__":
    runner = RobotRunner(backend="sim")  # Change to "sim" for simulation or "gpio" for real hardware
    runner.run()

