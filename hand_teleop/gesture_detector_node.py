#!/usr/bin/env python3

import math
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, String

from hand_teleop_interfaces.msg import HandLandmarks


class GestureDetectorNode(Node):
    def __init__(self):
        super().__init__("gesture_detector_node")

        self.landmark_sub = self.create_subscription(
            HandLandmarks,
            "/hand/landmarks",
            self.landmarks_callback,
            10
        )

        self.pinch_pub = self.create_publisher(Bool, "/hand/pinch", 10)
        self.gesture_pub = self.create_publisher(String, "/hand/gesture", 10)

        self.pinch_threshold = 0.05

        self.get_logger().info("Gesture detector node started")
        self.get_logger().info("Subscribing to /hand/landmarks")

    def landmarks_callback(self, msg):
        if len(msg.x) != 21 or len(msg.y) != 21 or len(msg.z) != 21:
            self.get_logger().warn("Invalid landmark message")
            return

        thumb_tip = 4
        index_tip = 8
        wrist = 0

        dx = msg.x[thumb_tip] - msg.x[index_tip]
        dy = msg.y[thumb_tip] - msg.y[index_tip]
        dz = msg.z[thumb_tip] - msg.z[index_tip]

        pinch_distance = math.sqrt(dx * dx + dy * dy + dz * dz)
        is_pinching = pinch_distance < self.pinch_threshold

        pinch_msg = Bool()
        pinch_msg.data = is_pinching
        self.pinch_pub.publish(pinch_msg)

        gesture_msg = String()

        if is_pinching:
            gesture_msg.data = "pinch"
        else:
            gesture_msg.data = "open"

        self.gesture_pub.publish(gesture_msg)

        self.get_logger().info(
            f"Gesture: {gesture_msg.data} | "
            f"Pinch distance: {pinch_distance:.3f} | "
            f"Wrist: x={msg.x[wrist]:.2f}, y={msg.y[wrist]:.2f}, z={msg.z[wrist]:.2f}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = GestureDetectorNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()


if __name__ == "__main__":
    main()
