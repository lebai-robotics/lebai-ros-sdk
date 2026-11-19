"""ROS1 ActionServer lifecycle for independent goal workers."""

from concurrent.futures import Future
from contextlib import contextmanager
from threading import Event, Lock, Thread

from actionlib import ActionServer

from lebai_driver.sdk_gate import SdkAdmission


class _GoalCanceled(Exception):
    pass


class _Cancellation:
    def __init__(self):
        self.requested = Event()
        self.hook_result = Future()


class ActionBridge:
    def __init__(self, connection, action_name, server_factory, worker_factory, admission=None):
        self.connection = connection
        self._worker_factory = worker_factory or Thread
        self._admission = admission or SdkAdmission()
        self._state = Lock()
        self._cancellations = {}
        self.server = (server_factory or ActionServer)(
            action_name, self.action_type, self._goal, self._cancel, auto_start=False)
        self.server.start()

    def shutdown(self):
        self._admission.shutdown()

    @contextmanager
    def _admit_call(self, canceled=None):
        with self._admission.access() as admitted:
            if not admitted or (canceled is not None and canceled.is_set()):
                raise _GoalCanceled()
            yield

    def _goal(self, handle):
        goal = handle.get_goal()
        goal_id = handle.get_goal_id().id
        rejection = self._rejection(goal)
        cancellation = _Cancellation()
        with self._state:
            if self._admission.is_closed():
                rejection = self.result_type()
            if rejection is None:
                self._cancellations[goal_id] = cancellation

        # actionlib invokes callbacks under its own lock. Never invoke a handle
        # transition while holding the bridge lock.
        if rejection is not None:
            handle.set_rejected(rejection)
            return
        handle.set_accepted()
        try:
            worker = self._worker_factory(target=self._run, args=(handle, goal_id, goal, cancellation),
                                          daemon=True)
            worker.start()
        except Exception as exc:
            with self._state:
                self._cancellations.pop(goal_id, None)
            handle.set_aborted(self._error_result(exc))

    def _cancel(self, handle):
        goal_id = handle.get_goal_id().id
        with self._state:
            cancellation = self._cancellations.get(goal_id)
            if cancellation is None or self._admission.is_closed() or cancellation.requested.is_set():
                return
            cancellation.requested.set()
        try:
            self._on_cancel()
        except _GoalCanceled:
            pass  # Shutdown closed admission before the cancel hook entered.
        except Exception as exc:
            cancellation.hook_result.set_exception(exc)
            return
        cancellation.hook_result.set_result(None)

    def _run(self, handle, goal_id, goal, cancellation):
        result = self.result_type()
        try:
            if self._admission.is_closed() or cancellation.requested.is_set():
                raise _GoalCanceled()
            success = self._execute(goal, result, cancellation.requested)
        except _GoalCanceled:
            success = False
        except Exception as exc:
            result = self._error_result(exc)
            success = False

        with self._state:
            self._cancellations.pop(goal_id)
            shutting_down = self._admission.is_closed()
            cancel_requested = cancellation.requested.is_set()

        if cancel_requested and not shutting_down:
            try:
                cancellation.hook_result.result()
                self._on_cancel()
            except _GoalCanceled:
                pass
            except Exception as exc:
                handle.set_aborted(self._error_result(exc))
                return
        if shutting_down or cancel_requested:
            handle.set_canceled(result)
        elif success:
            handle.set_succeeded(result)
        else:
            handle.set_aborted(result)

    def _rejection(self, goal):
        return None

    def _on_cancel(self):
        pass
