# Lebai ROS Noetic SDK 文档

[查看 Noetic 在线文档](https://lebai-robotics.github.io/lebai-ros-sdk/noetic/)

驱动 2.0.0 面向 Ubuntu 20.04 上的 ROS Noetic，需要 Python 3.8 和
`pylebai>=2.0.8,<3`，不支持 Python 2。本次升级包含不兼容变更。驱动通过
`lebai_interfaces` 提供服务和状态，并为 LM3 提供带内置夹爪和仅机械臂两种
MoveIt 1 配置。

- [安装 SDK 并构建 Catkin 工作空间](https://lebai-robotics.github.io/lebai-ros-sdk/noetic/install.html)
- [快速开始](https://lebai-robotics.github.io/lebai-ros-sdk/noetic/quickstart.html)
- [节点和参数](https://lebai-robotics.github.io/lebai-ros-sdk/noetic/architecture.html)
- [话题](https://lebai-robotics.github.io/lebai-ros-sdk/noetic/interfaces/topics.html)
- [服务](https://lebai-robotics.github.io/lebai-ros-sdk/noetic/interfaces/services.html)
- [为 LM3 配置 MoveIt 1](https://lebai-robotics.github.io/lebai-ros-sdk/noetic/moveit.html)
- [运行 Python 示例](https://lebai-robotics.github.io/lebai-ros-sdk/noetic/examples.html)

在仓库根目录构建 HTML 文档。

```bash
python3 -m pip install --user -r docs/requirements.txt
./scripts/build-docs.sh
```

构建完成后，在浏览器中打开 `site/index.html`。
