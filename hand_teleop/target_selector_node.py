#!/usr/bin/env python3

import math
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from hand_teleop_interfaces.msg import HandLandmarks


class TargetSelectorNode(Node):
    def __init__(self):
        super().__init__("target_selector_node")

        self.sub = self.create_subscription(
            HandLandmarks,
            "/hand/landmarks",
            self.landmarks_callback,
            10
        )

        self.pose_pub = self.create_publisher(
            PoseStamped,
            "/teleop/target_pose",
            10
        )

        self.last_index = None
        self.stable_start_time = None
        self.target_sent = False

        self.stability_threshold = 0.015
        self.hold_time = 1.5

        self.get_logger().info("Target selector started")
        self.get_logger().info("Hold index finger steady to send one target pose")

    def distance_3d(self, a, b):
        return math.sqrt(
            (a[0] - b[0]) ** 2 +
            (a[1] - b[1]) ** 2 +
            (a[2] - b[2]) ** 2
        )

    def landmarks_callback(self, msg):
        if self.target_sent:
            return

        if len(msg.x) != 21 or len(msg.y) != 21 or len(msg.z) != 21:
            return

        index_tip = 8

        current_index = (
            msg.x[index_tip],
            msg.y[index_tip],
            msg.z[index_tip],
        )

        now = self.get_clock().now()

        if self.last_index is None:
            self.last_index = current_index
            self.stable_start_time = now
            return

        movement = self.distance_3d(current_index, self.last_index)

        if movement < self.stability_threshold:
            elapsed = (now - self.stable_start_time).nanoseconds / 1e9

            self.get_logger().info(
                f"Index stable: {elapsed:.2f}s / {self.hold_time:.2f}s"
            )

            if elapsed >= self.hold_time:
                self.publish_target(current_index)
                self.target_sent = True
                self.get_logger().info("Target sent. Arm is now frozen.")
        else:
            self.stable_start_time = now
            self.last_index = current_index

    def publish_target(self, index):
        hand_x, hand_y, hand_z = index

        target = PoseStamped()
        target.header.stamp = self.get_clock().now().to_msg()
        target.header.frame_id = "panda_link0"

        # Index fingertip camera coordinates -> Panda workspace
        target.pose.position.x = 0.4 + (0.5 - hand_y) * 0.5
        target.pose.position.y = (0.5 - hand_x) * 0.5
        target.pose.position.z = 0.4 + (-hand_z) * 1.5

        target.pose.orientation.x = 1.0
        target.pose.orientation.y = 0.0
        target.pose.orientation.z = 0.0
        target.pose.orientation.w = 0.0

        self.pose_pub.publish(target)

        self.get_logger().info(
            f"Published one target pose: "
            f"x={target.pose.position.x:.2f}, "
            f"y={target.pose.position.y:.2f}, "
            f"z={target.pose.position.z:.2f}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = TargetSelectorNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()


if __name__ == "__main__":
    main()
