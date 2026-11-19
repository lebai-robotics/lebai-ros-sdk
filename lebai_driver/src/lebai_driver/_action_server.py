"""ROS1 ActionServer lifecycle for independent goal workers."""

from threading import Event, Lock, Thread

from actionlib import ActionServer


class _GoalCanceled(Exception):
    pass


class ActionBridge:
    def __init__(self, connection, action_name, server_factory, worker_factory):
        self.connection = connection
        self._worker_factory = worker_factory or Thread
        self._shutdown = Event()
        self._lock = Lock()
        self._cancel_events = {}
        self.server = (server_factory or ActionServer)(
            action_name, self.action_type, self._goal, self._cancel, auto_start=False)
        self.server.start()

    def shutdown(self):
        with self._lock:
            self._shutdown.set()

    def _goal(self, handle):
        goal = handle.get_goal()
        goal_id = handle.get_goal_id().id
        rejection = self._rejection(goal)
        canceled = Event()
        with self._lock:
            if self._shutdown.is_set():
                rejection = self.result_type()
            if rejection is None:
                self._cancel_events[goal_id] = canceled

        # actionlib invokes callbacks under its own lock. Never invoke a handle
        # transition while holding the bridge lock.
        if rejection is not None:
            handle.set_rejected(rejection)
            return
        handle.set_accepted()
        try:
            worker = self._worker_factory(target=self._run, args=(handle, goal_id, goal, canceled),
                                          daemon=True)
            worker.start()
        except Exception as exc:
            with self._lock:
                self._cancel_events.pop(goal_id, None)
            handle.set_aborted(self._error_result(exc))

    def _cancel(self, handle):
        goal_id = handle.get_goal_id().id
        with self._lock:
            canceled = self._cancel_events.get(goal_id)
            if canceled is None or self._shutdown.is_set():
                return
            canceled.set()
        self._on_cancel()

    def _run(self, handle, goal_id, goal, canceled):
        def check_active():
            if self._shutdown.is_set() or canceled.is_set():
                raise _GoalCanceled()

        result = self.result_type()
        try:
            check_active()
            success = self._execute(goal, result, check_active)
        except _GoalCanceled:
            success = False
        except Exception as exc:
            result = self._error_result(exc)
            success = False

        with self._lock:
            self._cancel_events.pop(goal_id)
            shutting_down = self._shutdown.is_set()
            cancel_requested = canceled.is_set()

        if cancel_requested and not shutting_down:
            try:
                self._on_cancel()
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
