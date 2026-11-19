# Lebai Noetic driver

Start the driver from a sourced Catkin workspace. Replace the example IP with the controller address.

```bash
roslaunch lebai_driver driver.launch robot_ip:=192.168.1.104
```

Add `simulator:=true` to connect to a running simulator. Driver services and status topics use the `/lebai` namespace by default. The two action names default to the absolute paths `/lebai_trajectory_controller` and `/lebai_gripper_controller/gripper_cmd`.

- [Launch parameters and companion nodes](../docs/quickstart.rst)
- [Status topics](../docs/interfaces/topics.rst)
- [Services](../docs/interfaces/services.rst)
- [Actions, concurrency limits, and migration](../docs/architecture.rst)
