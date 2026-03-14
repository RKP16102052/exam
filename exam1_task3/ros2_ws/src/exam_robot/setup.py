from setuptools import find_packages, setup

package_name = 'exam_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/robot_system.launch.py']),
        ('share/' + package_name + '/urdf', ['urdf/exam_robot.urdf']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Student',
    maintainer_email='student@example.com',
    description='Exam robot package',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'battery_node = exam_robot.battery_node:main',
            'distance_sensor = exam_robot.distance_sensor:main',
            'robot_controller = exam_robot.robot_controller:main',
            'status_display = exam_robot.status_display:main',
        ],
    },
)
