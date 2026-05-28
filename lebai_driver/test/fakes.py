class FakeRobot:
    def __init__(self, robot_ip='127.0.0.1', simulator=False):
        self.robot_ip = robot_ip
        self.simulator = simulator
        self.calls = []

    def start_sys(self):
        self.calls.append(('start_sys', (), {}))


class FakeRobotFactory:
    def __init__(self):
        self.calls = []

    def __call__(self, robot_ip, simulator=False):
        self.calls.append((robot_ip, simulator))
        return FakeRobot(robot_ip=robot_ip, simulator=simulator)


class FakeDiscovery:
    def __init__(self, controllers=None):
        self.controllers = controllers or []
        self.calls = []

    def resolve(self):
        self.calls.append(('resolve', (), {}))
        return self.controllers


class FakeStandaloneGripper:
    def __init__(self):
        self.calls = []

    def move(self, position):
        self.calls.append(('move', (position,), {}))
