class RobotConnection:
    def __init__(self, robot_ip, simulator=False, robot_factory=None):
        if not robot_ip:
            raise ValueError('robot_ip is required')

        self.robot_ip = robot_ip
        self.simulator = simulator
        self._robot_factory = robot_factory or _default_robot_factory
        self._robot = None

    @property
    def robot(self):
        if self._robot is None:
            self._robot = self._robot_factory(self.robot_ip, simulator=self.simulator)
        return self._robot


def _default_robot_factory(robot_ip, simulator=False):
    import pylebai

    return pylebai.Robot(robot_ip, simulator=simulator)
