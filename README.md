# ROS 2 Vision-Based Hand Teleoperation

A ROS 2 project that enables **vision-based teleoperation** of a robotic manipulator using only a webcam and MediaPipe hand tracking.

The goal is to control the end-effector of a Franka Panda robot arm using natural hand motions without requiring a motion capture suit or specialized hardware.

---

## Features

- Webcam-based hand tracking using MediaPipe
- ROS 2 Python nodes
- Custom ROS 2 messages (`HandLandmarks`)
- Gesture detection (pinch, open hand)
- Pose mapping from camera space to robot workspace
- MoveIt 2 integration for Franka Panda *(work in progress)*

---

## Project Architecture

```text
Webcam
   │
   ▼
Hand Tracking Node
(OpenCV + MediaPipe)
   │
   ▼
/hand/landmarks
(Custom ROS 2 Message)
   │
   ▼
Gesture Detector
   │
   ├── /hand/pinch
   └── /hand/gesture
   │
   ▼
Pose Mapper
   │
   ▼
/teleop/target_pose
   │
   ▼
MoveIt 2
   │
   ▼
Franka Panda Robot
```

---

## Current Progress

- ✅ ROS 2 workspace setup
- ✅ Webcam node
- ✅ MediaPipe hand tracking
- ✅ Custom ROS 2 interface package
- ✅ Landmark publisher
- ✅ Gesture detector
- ✅ Pose mapper
- 🚧 MoveIt 2 teleoperation
- ⏳ Gripper control
- ⏳ Motion smoothing
- ⏳ Safety constraints

---

## Technologies Used

- ROS 2 Humble
- Python
- OpenCV
- MediaPipe
- MoveIt 2
- RViz2

---

## Repository Structure

```text
hand_teleop/
├── hand_teleop/
│   ├── webcam_node.py
│   ├── hand_tracking_node.py
│   ├── gesture_detector_node.py
│   ├── pose_mapper_node.py
│   └── moveit_teleop_node.py
├── package.xml
├── setup.py
└── README.md
```

---

## Future Work

- Continuous MoveIt teleoperation
- Palm orientation estimation
- Gripper control using pinch gestures
- Motion smoothing
- Workspace constraints
- Launch files
- Support for real robot hardware

---

## Author

**Pranav**
