from lebai_driver.sdk_gate import SdkAdmission


class RosNodeAdapter:
    def __init__(self, rospy_module=None):
        if rospy_module is None:
            import rospy as rospy_module

        self._rospy = rospy_module
        self.admission = SdkAdmission(lambda: self._rospy.is_shutdown_requested() or self._rospy.is_shutdown())
        self.on_shutdown(self.admission.shutdown)

    def parameter(self, name, default):
        return self._rospy.get_param(f'~{name}', default)

    def create_service(self, srv_type, name, callback):
        def handle_request(request):
            response = srv_type._response_class()
            callback(request, response)
            return response

        return self._rospy.Service(name, srv_type, handle_request)

    def create_publisher(self, msg_type, name, queue_size=10):
        return self._rospy.Publisher(name, msg_type, queue_size=queue_size)

    def create_timer(self, period, callback):
        def handle_timer(_event):
            with self.admission.access() as admitted:
                if admitted:
                    callback()

        return self._rospy.Timer(self._rospy.Duration.from_sec(period), handle_timer)

    def now(self):
        return self._rospy.Time.now()

    def loginfo(self, *args, **kwargs):
        self._rospy.loginfo(*args, **kwargs)

    def logerr(self, *args, **kwargs):
        self._rospy.logerr(*args, **kwargs)

    def on_shutdown(self, callback):
        self._rospy.on_shutdown(callback)
