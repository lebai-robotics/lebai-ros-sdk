# Lebai ROS SDK

> **在线文档入口：**
> <https://lebai-robotics.github.io/lebai-ros-sdk/>

本仓库提供 Lebai 机器人在 ROS/ROS2 下使用的驱动、示例、机器人模型和文档。

`main` 分支只作为项目入口和 GitHub Pages 文档发布分支使用，不用于构建机器人
驱动。请根据你的 Ubuntu 和 ROS 发行版选择对应分支。

## 当前 ROS2 分支

| ROS 发行版 | Ubuntu | 代码分支 | 获取代码 |
| --- | --- | --- | --- |
| ROS2 Humble | Ubuntu 22.04 | `humble-dev` | `git clone --branch humble-dev https://github.com/lebai-robotics/lebai-ros-sdk.git` |
| ROS2 Jazzy | Ubuntu 24.04 | `jazzy-dev` | `git clone --branch jazzy-dev https://github.com/lebai-robotics/lebai-ros-sdk.git` |
| ROS2 Lyrical | Ubuntu 26.04 | `lyrical-dev` | `git clone --branch lyrical-dev https://github.com/lebai-robotics/lebai-ros-sdk.git` |

## 历史分支

以下分支保留给已有用户参考，不再作为当前开发目标：

| ROS 发行版 | 代码分支 |
| --- | --- |
| ROS Noetic | `noetic-dev` |
| ROS2 Galactic | `galactic-dev` |
| ROS Melodic | `melodic-dev` |

## 文档发布

GitHub Pages 由 `main` 分支统一发布。发布流程会构建中文 Sphinx 首页，使用
Read the Docs 主题，然后分别检出当前 ROS2 分支并构建各自的 Sphinx 文档，最后
把合并后的站点发布到 `gh-pages` 分支：

```text
/              文档入口和分支选择页
/humble/       从 humble-dev 构建的文档
/jazzy/        从 jazzy-dev 构建的文档
/lyrical/      从 lyrical-dev 构建的文档
/noetic/       历史文档入口
/galactic/     历史文档入口
/melodic/      历史文档入口
```

各发行版分支会运行自己的 CI，用于验证代码、测试和本地文档构建；它们不直接发布
GitHub Pages。
