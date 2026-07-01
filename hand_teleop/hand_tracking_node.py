#!/usr/bin/env python3

import cv2
import mediapipe as mp
import rclpy
from rclpy.node import Node

from hand_teleop_interfaces.msg import HandLandmarks


class HandTrackingNode(Node):
    def __init__(self):
        super().__init__("hand_tracking_node")

        self.landmark_pub = self.create_publisher(
            HandLandmarks,
            "/hand/landmarks",
            10
        )

        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            self.get_logger().error("Could not open webcam")
            return

        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
        )

        self.timer = self.create_timer(0.03, self.process_frame)

        self.get_logger().info("Hand tracking node started")
        self.get_logger().info("Publishing landmarks on /hand/landmarks")

    def process_frame(self):
        ret, frame = self.cap.read()

        if not ret:
            self.get_logger().error("Could not read frame")
            return

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                )

                msg = HandLandmarks()
                msg.header.stamp = self.get_clock().now().to_msg()
                msg.header.frame_id = "camera"

                for landmark in hand_landmarks.landmark:
                    msg.x.append(float(landmark.x))
                    msg.y.append(float(landmark.y))
                    msg.z.append(float(landmark.z))

                self.landmark_pub.publish(msg)

                wrist = hand_landmarks.landmark[0]
                index_tip = hand_landmarks.landmark[8]
                thumb_tip = hand_landmarks.landmark[4]

                self.get_logger().info(
                    f"Wrist: x={wrist.x:.2f}, y={wrist.y:.2f}, z={wrist.z:.2f} | "
                    f"Index: x={index_tip.x:.2f}, y={index_tip.y:.2f}, z={index_tip.z:.2f} | "
                    f"Thumb: x={thumb_tip.x:.2f}, y={thumb_tip.y:.2f}, z={thumb_tip.z:.2f}"
                )

        cv2.imshow("ROS 2 Hand Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            self.get_logger().info("Q pressed, shutting down")
            rclpy.shutdown()

    def destroy_node(self):
        if hasattr(self, "cap"):
            self.cap.release()

        if hasattr(self, "hands"):
            self.hands.close()

        cv2.destroyAllWindows()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = HandTrackingNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()


if __name__ == "__main__":
    main()
