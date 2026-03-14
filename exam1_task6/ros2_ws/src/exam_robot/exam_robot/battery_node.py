#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class BatteryNode(Node):
    def __init__(self):
        super().__init__('battery_node')
        # Издатель для топика /battery_level
        self.publisher_ = self.create_publisher(Float32, '/battery_level', 10)
        # Таймер с частотой 1 Гц
        self.timer = self.create_timer(1.0, self.timer_callback)
        # Начальный заряд
        self.level = 100
        # Множество уже залогированных порогов (чтобы не повторяться)
        self.logged_thresholds = set()

    def timer_callback(self):
        # Публикуем текущий уровень заряда
        msg = Float32()
        msg.data = float(self.level)
        self.publisher_.publish(msg)

        # Логирование при достижении нового порога (90%, 80%, ..., 0%)
        if self.level % 10 == 0 and self.level < 100 and self.level not in self.logged_thresholds:
            self.get_logger().info(f'Battery: {self.level}%')
            self.logged_thresholds.add(self.level)

        # Разряд: уменьшаем заряд, но не ниже 0
        if self.level > 0:
            self.level -= 1

def main(args=None):
    rclpy.init(args=args)
    node = BatteryNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()