from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Определяем путь к URDF-файлу внутри пакета
    urdf_path = os.path.join(
        get_package_share_directory('exam_robot'),
        'urdf',
        'exam_robot.urdf'
    )

    # Читаем содержимое URDF для передачи в параметр robot_description
    with open(urdf_path, 'r') as urdf_file:
        robot_description_content = urdf_file.read()

    return LaunchDescription([
        # Узел robot_state_publisher, публикующий TF из URDF
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description_content}]
        ),

        # Узлы из пакета exam_robot
        Node(
            package='exam_robot',
            executable='battery_node',
            name='battery_node',
            output='screen'
        ),
        Node(
            package='exam_robot',
            executable='distance_sensor',
            name='distance_sensor',
            output='screen'
        ),
        Node(
            package='exam_robot',
            executable='status_display',
            name='status_display',
            output='screen'
        ),
        Node(
            package='exam_robot',
            executable='robot_controller',
            name='robot_controller',
            output='screen'
        ),
    ])