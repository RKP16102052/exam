#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist

class DistanceSensor(Node):
    def __init__(self):
        super().__init__('distance_sensor')
        # Публикатор для /distance
        self.publisher_ = self.create_publisher(Float32, '/distance', 10)
        # Подписка на /cmd_vel
        self.subscription = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_callback, 10)
        # Таймер с частотой 5 Гц (период 0.2 с)
        self.timer = self.create_timer(0.2, self.timer_callback)
        # Начальные значения
        self.current_speed = 0.0          # линейная скорость по X
        self.distance = 3.0                # начальная дистанция

    def cmd_callback(self, msg):
        # Сохраняем текущую команду скорости
        self.current_speed = msg.linear.x

    def timer_callback(self):
        # Обновляем расстояние в зависимости от скорости
        if self.current_speed == 0.0:
            # Стоим – расстояние равно 3.0 м
            self.distance = 3.0
        elif self.current_speed > 0.0:
            # Движение вперёд – уменьшаем на 0.2 м, но не менее 0.5 м
            self.distance = max(0.5, self.distance - 0.2)
        else:  # self.current_speed < 0.0
            # Движение назад – увеличиваем на 0.2 м, но не более 3.0 м
            self.distance = min(3.0, self.distance + 0.2)

        # Публикуем текущее расстояние
        msg = Float32()
        msg.data = self.distance
        self.publisher_.publish(msg)

        # Логирование для отладки (можно оставить, но необязательно)
        # self.get_logger().info(f'Distance: {self.distance:.2f} m')

def main(args=None):
    rclpy.init(args=args)
    node = DistanceSensor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()