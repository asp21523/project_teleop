#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from std_msgs.msg import Bool
from control_msgs.action import GripperCommand


class GripperControlNode(Node):
    def __init__(self):
        super().__init__("gripper_control_node")

        self.last_pinch = None
        self.goal_active = False

        self.sub = self.create_subscription(
            Bool,
            "/hand/pinch",
            self.pinch_callback,
            10
        )

        self.client = ActionClient(
            self,
            GripperCommand,
            "/panda_hand_controller/gripper_cmd"
        )

        self.get_logger().info("Gripper control node started")

    def pinch_callback(self, msg):
        if msg.data == self.last_pinch:
            return

        if self.goal_active:
            return

        self.last_pinch = msg.data

        if msg.data:
            self.send_gripper_goal(0.0, 10.0)   # close
        else:
            self.send_gripper_goal(0.08, 10.0)  # open

    def send_gripper_goal(self, position, effort):
        if not self.client.wait_for_server(timeout_sec=1.0):
            self.get_logger().warn("Gripper action server not available")
            return

        goal = GripperCommand.Goal()
        goal.command.position = position
        goal.command.max_effort = effort

        self.goal_active = True
        self.get_logger().info(f"Sending gripper goal: position={position}")

        future = self.client.send_goal_async(goal)
        future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().warn("Gripper goal rejected")
            self.goal_active = False
            return

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def result_callback(self, future):
        self.get_logger().info("Gripper movement done")
        self.goal_active = False


def main(args=None):
    rclpy.init(args=args)
    node = GripperControlNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()


if __name__ == "__main__":
    main()
