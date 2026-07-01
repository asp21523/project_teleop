#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped

from hand_teleop_interfaces.msg import HandLandmarks


class PoseMapperNode(Node):
    def __init__(self):
        super().__init__("pose_mapper_node")

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

        self.get_logger().info("Pose mapper node started")

    def landmarks_callback(self, msg):
        if len(msg.x) != 21:
            return

        wrist = 0

        hand_x = msg.x[wrist]
        hand_y = msg.y[wrist]
        hand_z = msg.z[wrist]

        target = PoseStamped()
        target.header.stamp = self.get_clock().now().to_msg()
        target.header.frame_id = "base_link"

        # Camera normalized coordinates → robot workspace
        target.pose.position.x = 0.4 + (0.5 - hand_y) * 0.5
        target.pose.position.y = (0.5 - hand_x) * 0.5
        target.pose.position.z = 0.4 + (-hand_z) * 1.5

        target.pose.orientation.x = 0.0
        target.pose.orientation.y = 0.0
        target.pose.orientation.z = 0.0
        target.pose.orientation.w = 1.0

        self.pose_pub.publish(target)

        self.get_logger().info(
            f"Target pose: x={target.pose.position.x:.2f}, "
            f"y={target.pose.position.y:.2f}, "
            f"z={target.pose.position.z:.2f}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = PoseMapperNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()


if __name__ == "__main__":
    main()
