from setuptools import find_packages, setup

package_name = 'hand_teleop'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='pranav.infinite@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={

        'console_scripts': [

            'webcam_node = hand_teleop.webcam_node:main',
            'hand_tracking_node = hand_teleop.hand_tracking_node:main',
            'gesture_detector_node = hand_teleop.gesture_detector_node:main',
            'pose_mapper_node = hand_teleop.pose_mapper_node:main',
            'moveit_teleop_node = hand_teleop.moveit_teleop_node:main',
            'gripper_control_node = hand_teleop.gripper_control_node:main',
            'target_selector_node = hand_teleop.target_selector_node:main',
        ],
    },
)
