# Lebai ROS Noetic SDK 文档

驱动 2.0.0 面向 Ubuntu 20.04 上的 ROS Noetic，需要 Python 3.8 和
`pylebai>=2.0.8,<3`，不支持 Python 2。本次升级包含不兼容变更。驱动通过
`lebai_interfaces` 提供服务和状态，并为 LM3 提供带内置夹爪和仅机械臂两种
MoveIt 1 配置。

- [安装 SDK 并构建 Catkin 工作空间](docs/install.rst)
- [快速开始](docs/quickstart.rst)
- [节点和参数](docs/architecture.rst)
- [话题](docs/interfaces/topics.rst)
- [服务](docs/interfaces/services.rst)
- [为 LM3 配置 MoveIt 1](docs/moveit.rst)
- [运行 Python 示例](docs/examples.rst)

在仓库根目录构建 HTML 文档。

```bash
python3 -m pip install --user -r docs/requirements.txt
./scripts/build-docs.sh
```

构建完成后，在浏览器中打开 `site/index.html`。
