#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from geometry_msgs.msg import PoseStamped
from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import (
    Constraints,
    PositionConstraint,
    OrientationConstraint,
    BoundingVolume,
)
from shape_msgs.msg import SolidPrimitive


class MoveItTeleopNode(Node):
    def __init__(self):
        super().__init__("moveit_teleop_node")

        self.latest_pose = None
        self.goal_active = False

        self.sub = self.create_subscription(
            PoseStamped,
            "/teleop/target_pose",
            self.pose_callback,
            10,
        )

        self.client = ActionClient(self, MoveGroup, "/move_action")

        self.timer = self.create_timer(2.0, self.send_goal_timer)

        self.get_logger().info("MoveIt teleop node started")
        self.get_logger().info("Waiting for /move_action...")

    def pose_callback(self, msg):
        self.latest_pose = msg

    def send_goal_timer(self):
        if self.latest_pose is None:
            return

        if self.goal_active:
            return

        if not self.client.wait_for_server(timeout_sec=0.1):
            self.get_logger().warn("MoveIt action server not available yet")
            return

        pose = self.latest_pose

        goal = MoveGroup.Goal()
        goal.request.group_name = "panda_arm"
        goal.request.num_planning_attempts = 5
        goal.request.allowed_planning_time = 2.0
        goal.request.max_velocity_scaling_factor = 0.2
        goal.request.max_acceleration_scaling_factor = 0.2

        constraints = Constraints()

        position_constraint = PositionConstraint()
        position_constraint.header.frame_id = "panda_link0"
        position_constraint.link_name = "panda_hand"
        position_constraint.weight = 1.0

        box = SolidPrimitive()
        box.type = SolidPrimitive.BOX
        box.dimensions = [0.02, 0.02, 0.02]

        volume = BoundingVolume()
        volume.primitives.append(box)
        volume.primitive_poses.append(pose.pose)

        position_constraint.constraint_region = volume
        constraints.position_constraints.append(position_constraint)

        orientation_constraint = OrientationConstraint()
        orientation_constraint.header.frame_id = "panda_link0"
        orientation_constraint.link_name = "panda_hand"
        orientation_constraint.orientation = pose.pose.orientation
        orientation_constraint.absolute_x_axis_tolerance = 3.14
        orientation_constraint.absolute_y_axis_tolerance = 3.14
        orientation_constraint.absolute_z_axis_tolerance = 3.14
        orientation_constraint.weight = 0.1

        constraints.orientation_constraints.append(orientation_constraint)

        goal.request.goal_constraints.append(constraints)

        self.goal_active = True
        self.get_logger().info(
            f"Sending goal: x={pose.pose.position.x:.2f}, "
            f"y={pose.pose.position.y:.2f}, "
            f"z={pose.pose.position.z:.2f}"
        )

        future = self.client.send_goal_async(goal)
        future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().warn("Goal rejected")
            self.goal_active = False
            return

        self.get_logger().info("Goal accepted")
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f"MoveIt result error code: {result.error_code.val}")
        self.goal_active = False


def main(args=None):
    rclpy.init(args=args)
    node = MoveItTeleopNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()


if __name__ == "__main__":
    main()
