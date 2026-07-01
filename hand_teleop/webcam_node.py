#!/usr/bin/env python3

import cv2
import rclpy
from rclpy.node import Node


class WebcamNode(Node):
    def __init__(self):
        super().__init__("webcam_node")

        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            self.get_logger().error("Could not open webcam")
            return

        self.get_logger().info("Webcam opened successfully")
        self.timer = self.create_timer(0.03, self.read_frame)

    def read_frame(self):
        ret, frame = self.cap.read()

        if not ret:
            self.get_logger().error("Could not read frame")
            return

        cv2.imshow("ROS 2 Webcam Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            self.get_logger().info("Q pressed, shutting down")
            rclpy.shutdown()

    def destroy_node(self):
        if hasattr(self, "cap"):
            self.cap.release()
        cv2.destroyAllWindows()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = WebcamNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()


if __name__ == "__main__":
    main()
