from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    urdf_path = os.path.join(
        get_package_share_directory('exam_robot'),
        'urdf',
        'exam_robot.urdf'
    )

    with open(urdf_path, 'r') as infp:
        robot_description = infp.read()

    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description}]
    )

    # Наши узлы с параметрами (бонус 2)
    battery_node = Node(
        package='exam_robot',
        executable='battery_node',
        name='battery_node',
        output='screen',
        parameters=[{'discharge_rate': 1.0}]  # можно изменить
    )

    distance_sensor = Node(
        package='exam_robot',
        executable='distance_sensor',
        name='distance_sensor',
        output='screen'
    )

    status_display = Node(
        package='exam_robot',
        executable='status_display',
        name='status_display',
        output='screen'
    )

    robot_controller = Node(
        package='exam_robot',
        executable='robot_controller',
        name='robot_controller',
        output='screen',
        parameters=[{'max_speed': 0.3}]       # можно изменить
    )

    # Бонус 1: RViz с конфигурацией
    rviz_config = os.path.join(
        get_package_share_directory('exam_robot'),
        'rviz',
        'exam_robot.rviz'
    )
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config]
    )

    return LaunchDescription([
        robot_state_publisher,
        battery_node,
        distance_sensor,
        status_display,
        robot_controller,
        rviz_node
    ])