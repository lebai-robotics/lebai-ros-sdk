from types import SimpleNamespace
from unittest.mock import Mock

from actionlib_msgs.msg import GoalID
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


class ActionHarness:
    """Capture ActionServer callbacks and defer each worker until its test runs it."""

    def __init__(self):
        self.jobs = []
        self.start_count = 0

    def server_factory(self, name, ActionSpec, goal_cb, cancel_cb, auto_start):
        assert auto_start is False
        self.name = name
        self.action_type = ActionSpec
        self.goal_cb = goal_cb
        self.cancel_cb = cancel_cb
        return self

    def start(self):
        self.start_count += 1

    def worker_factory(self, target, args, daemon):
        return SimpleNamespace(start=lambda: self.jobs.append(lambda: target(*args)))

    def submit(self, goal, goal_id='g1'):
        handle = self.handle(goal, goal_id)
        self.goal_cb(handle)
        return handle

    @staticmethod
    def handle(goal, goal_id):
        handle = Mock(spec=['get_goal', 'get_goal_id', 'set_accepted', 'set_rejected',
                            'set_aborted', 'set_succeeded', 'set_canceled'])
        handle.get_goal.return_value = goal
        handle.get_goal_id.return_value = GoalID(id=goal_id)
        return handle


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
