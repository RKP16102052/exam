#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32

class StatusDisplay(Node):
    def __init__(self):
        super().__init__('status_display')
        # Публикатор статуса с частотой 2 Гц
        self.publisher_ = self.create_publisher(String, '/robot_status', 10)
        self.timer = self.create_timer(0.5, self.timer_callback)  # 2 Hz

        # Подписка на топики батареи и расстояния
        self.battery_sub = self.create_subscription(Float32, '/battery_level', self.battery_callback, 10)
        self.distance_sub = self.create_subscription(Float32, '/distance', self.distance_callback, 10)

        # Хранение последних полученных значений
        self.battery = 100.0
        self.distance = 3.0
        self.last_status = ""  # для отслеживания изменений статуса

    def battery_callback(self, msg):
        self.battery = msg.data

    def distance_callback(self, msg):
        self.distance = msg.data

    def timer_callback(self):
        # Определение статуса по приоритету (CRITICAL → WARNING → ALL OK)
        if self.battery < 10.0 or self.distance < 0.7:
            status = "CRITICAL"
        elif self.battery < 20.0:
            status = "WARNING: Low battery"
        elif self.distance < 1.0:
            status = "WARNING: Obstacle close"
        else:
            status = "ALL OK"

        # Публикация статуса
        msg = String()
        msg.data = status
        self.publisher_.publish(msg)

        # Логирование при изменении статуса
        if status != self.last_status:
            self.get_logger().info(f'Status changed to: {status}')
            self.last_status = status

def main(args=None):
    rclpy.init(args=args)
    node = StatusDisplay()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()