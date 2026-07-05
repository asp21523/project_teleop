# Vision-Based Teleoperation of a Franka Panda Robot using ROS 2

A ROS 2 project that enables **vision-based teleoperation** of a **Franka Panda robotic manipulator** using only a webcam and MediaPipe hand tracking.

The objective is to control the robot without requiring expensive motion-capture systems or specialized gloves. Human hand movements are interpreted through computer vision, converted into robot commands, and executed using MoveIt 2.

---


# Demo

![Vision-Based Teleoperation Demo](media/gif1_teleop.gif)
# Features

- Webcam-based hand tracking using MediaPipe
- ROS 2 Humble Python implementation
- Custom ROS 2 interface package (`HandLandmarks`)
- Real-time 21-point hand landmark detection
- Gesture detection (Pinch / Open Hand)
- Target pose selection using the index fingertip
- One-shot robot positioning using MoveIt 2
- Franka Panda simulation in RViz2
- Gripper control using pinch gestures
- Modular ROS 2 node architecture

---

# System Architecture

```text
                         Webcam
                            │
                            ▼
                 OpenCV + MediaPipe
                            │
                            ▼
                 hand_tracking_node
                            │
                  /hand/landmarks
                            │
             ┌──────────────┴──────────────┐
             ▼                             ▼
    target_selector_node          gesture_detector_node
             │                             │
             ▼                             ▼
    /teleop/target_pose             /hand/pinch
             │                             │
             ▼                             ▼
    moveit_teleop_node         gripper_control_node
             │                             │
             └──────────────┬──────────────┘
                            ▼
                   Franka Panda Robot
```

---

# Teleoperation Workflow

1. Capture the user's hand using a webcam.
2. Detect 21 hand landmarks using MediaPipe.
3. Publish landmarks as a custom ROS 2 message.
4. Hold the index fingertip steady to select a robot target.
5. Move the Panda arm to the selected position using MoveIt 2.
6. Freeze the robot arm after reaching the target.
7. Control the gripper using pinch and release gestures.

---

# Repository Structure

```text
hand_teleop/
├── hand_teleop/
│   ├── webcam_node.py
│   ├── hand_tracking_node.py
│   ├── gesture_detector_node.py
│   ├── pose_mapper_node.py
│   ├── target_selector_node.py
│   ├── moveit_teleop_node.py
│   └── gripper_control_node.py
│
├── package.xml
├── setup.py
├── setup.cfg
├── LICENSE
└── README.md
```

---

# ROS 2 Nodes

| Node | Description |
|------|-------------|
| `hand_tracking_node` | Detects hand landmarks using MediaPipe and publishes them as a custom ROS 2 message. |
| `gesture_detector_node` | Detects pinch and open-hand gestures from the landmarks. |
| `target_selector_node` | Waits until the index fingertip is stable before publishing a target pose. |
| `moveit_teleop_node` | Sends a single target pose to MoveIt and freezes the robot after reaching it. |
| `gripper_control_node` | Controls the Panda gripper using pinch gestures. |
| `pose_mapper_node` | Converts camera coordinates into robot workspace coordinates (continuous teleoperation prototype). |

---

# Topics

| Topic | Type | Description |
|------|------|-------------|
| `/hand/landmarks` | `HandLandmarks` | 21 detected hand landmarks |
| `/hand/pinch` | `std_msgs/Bool` | Pinch detected |
| `/hand/gesture` | `std_msgs/String` | Current hand gesture |
| `/teleop/target_pose` | `geometry_msgs/PoseStamped` | Robot target pose |

---

# Technologies Used

- ROS 2 Humble
- Python
- OpenCV
- MediaPipe
- MoveIt 2
- RViz2

---

# Current Progress

- ✅ ROS 2 workspace setup
- ✅ Webcam integration
- ✅ MediaPipe hand tracking
- ✅ Custom ROS 2 interfaces
- ✅ Real-time landmark publishing
- ✅ Gesture detection
- ✅ Target pose selection
- ✅ Franka Panda MoveIt integration
- ✅ Robot positioning
- ✅ Gripper control using pinch gestures
- 🚧 Palm orientation estimation
- 🚧 Continuous Cartesian teleoperation
- 🚧 Motion smoothing
- 🚧 Workspace constraints
- 🚧 Real robot support

---

# Future Work

- Continuous Cartesian teleoperation
- Palm orientation estimation
- Full 6-DoF end-effector control
- Dynamic retargeting algorithms
- Motion filtering and smoothing
- Workspace safety constraints
- Launch files
- Real Franka Panda hardware support
- Multi-hand support
- Gesture-based mode switching

---

# Demo

🚧 Demo video coming soon.

Planned demonstration:

- Hand detection using a webcam
- Target selection using the index fingertip
- Robot arm moving to the selected position
- Pinch gesture closing the gripper
- Open hand opening the gripper

---

# Author

**Pranav**

Robotics | ROS 2 | Computer Vision | Manipulation | Teleoperation
