#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class BatteryNode(Node):
    def __init__(self):
        super().__init__('battery_node')
        # Параметр скорости разряда (%/сек)
        self.declare_parameter('discharge_rate', 1.0)
        self.discharge_rate = self.get_parameter('discharge_rate').value

        self.publisher_ = self.create_publisher(Float32, '/battery_level', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.level = 100.0
        self.logged_thresholds = set()

    def timer_callback(self):
        msg = Float32()
        msg.data = float(self.level)
        self.publisher_.publish(msg)

        if self.level % 10 == 0 and self.level < 100 and self.level not in self.logged_thresholds:
            self.get_logger().info(f'Battery: {self.level}%')
            self.logged_thresholds.add(self.level)

        if self.level > 0:
            self.level -= self.discharge_rate

def main(args=None):
    rclpy.init(args=args)
    node = BatteryNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()