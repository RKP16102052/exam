#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class RobotController(Node):
    def __init__(self):
        super().__init__('robot_controller')
        # Подписка на статус робота
        self.subscription = self.create_subscription(
            String, '/robot_status', self.status_callback, 10)
        # Публикатор команд скорости
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        # Таймер с частотой 10 Гц
        self.timer = self.create_timer(0.1, self.timer_callback)

        # Текущий статус (начальное значение)
        self.current_status = "ALL OK"
        self.previous_status = None

    def status_callback(self, msg):
        self.current_status = msg.data

    def timer_callback(self):
        # Формируем команду в зависимости от статуса
        twist = Twist()
        if self.current_status == "ALL OK":
            twist.linear.x = 0.3
            twist.angular.z = 0.0
        elif self.current_status == "WARNING: Low battery":
            twist.linear.x = 0.1
            twist.angular.z = 0.0
        elif self.current_status == "WARNING: Obstacle close":
            twist.linear.x = 0.0
            twist.angular.z = 0.5
        elif self.current_status == "CRITICAL":
            twist.linear.x = 0.0
            twist.angular.z = 0.0
        else:
            # Неизвестный статус — безопасная остановка
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            self.get_logger().warn(f'Unknown status received: {self.current_status}')

        # Публикуем команду
        self.publisher_.publish(twist)

        # Логируем изменение режима работы
        if self.current_status != self.previous_status:
            self.get_logger().info(f'Robot mode changed to: {self.current_status}')
            self.previous_status = self.current_status

def main(args=None):
    rclpy.init(args=args)
    node = RobotController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()