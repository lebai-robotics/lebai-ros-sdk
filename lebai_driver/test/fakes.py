from types import SimpleNamespace

from genpy import Duration, Time


class FakeRobot:
    def __init__(self, robot_ip='127.0.0.1', simulator=False):
        self.robot_ip = robot_ip
        self.simulator = simulator


class FakeRobotFactory:
    def __init__(self):
        self.calls = []

    def __call__(self, robot_ip, simulator=False):
        self.calls.append((robot_ip, simulator))
        return FakeRobot(robot_ip=robot_ip, simulator=simulator)


class FakeRospy:
    Duration = Duration

    def __init__(self):
        self.parameters = {}
        self.parameter_calls = []
        self.services = []
        self.publishers = []
        self.timers = []
        self.shutdown = False
        self.shutdown_callbacks = []
        self.logs = []
        self.stamp = Time(12, 34)
        self.Time = SimpleNamespace(now=lambda: self.stamp)

    def get_param(self, name, default):
        self.parameter_calls.append((name, default))
        return self.parameters.get(name, default)

    def Service(self, name, srv_type, handler):
        service = SimpleNamespace(name=name, srv_type=srv_type, handler=handler)
        self.services.append(service)
        return service

    def Publisher(self, name, msg_type, queue_size):
        publisher = SimpleNamespace(name=name, msg_type=msg_type, queue_size=queue_size)
        self.publishers.append(publisher)
        return publisher

    def Timer(self, duration, callback):
        timer = SimpleNamespace(duration=duration, callback=callback)
        self.timers.append(timer)
        return timer

    def is_shutdown(self):
        return self.shutdown

    def on_shutdown(self, callback):
        self.shutdown_callbacks.append(callback)

    def loginfo(self, *args, **kwargs):
        self.logs.append(('info', args, kwargs))

    def logerr(self, *args, **kwargs):
        self.logs.append(('error', args, kwargs))
