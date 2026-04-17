"""
nav2.launch.py  –  Nav2 + TB3 Gazebo component of the RMF ↔ Nav2 Route demo.

Wraps nav2_bringup/tb3_simulation_launch.py with:
  - nav2_params.yaml resolved from this package (no hardcoded ws path)
  - BT XML path injected at launch time via RewrittenYaml

Run on ROS_DOMAIN_ID=0 (default).

Usage:
  ros2 launch rmf_nav2_route_demo nav2.launch.py [headless:=True]
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from nav2_common.launch import RewrittenYaml


def generate_launch_description():
    demo_dir = get_package_share_directory('rmf_nav2_route_demo')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    bt_xml = os.path.join(
        demo_dir, 'config', 'navigate_on_route_graph_with_recovery.xml'
    )

    # Rewrite the placeholder BT path inside nav2_params.yaml at runtime
    params_file = RewrittenYaml(
        source_file=os.path.join(demo_dir, 'config', 'nav2_params.yaml'),
        param_rewrites={'default_nav_to_pose_bt_xml': bt_xml},
        convert_types=True,
    )

    # tb3_simulation_launch.py evaluates headless inside a PythonExpression,
    # so the value must be Python-cased ('True' / 'False'), not 'true'/'false'.
    headless_arg = DeclareLaunchArgument(
        'headless', default_value='False',
        description="Pass 'True' to run Gazebo without GUI",
    )

    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_dir, 'launch', 'tb3_simulation_launch.py')
        ),
        launch_arguments={
            'headless': LaunchConfiguration('headless'),
            'params_file': params_file,
        }.items(),
    )

    rmw_implementation = SetEnvironmentVariable(
        'RMW_IMPLEMENTATION', 'rmw_cyclonedds_cpp'
    )
    nav2_domain = SetEnvironmentVariable('ROS_DOMAIN_ID', '0')
    localhost_only = SetEnvironmentVariable('ROS_LOCALHOST_ONLY', '1')
    local_discovery = SetEnvironmentVariable('ROS_AUTOMATIC_DISCOVERY_RANGE', 'LOCALHOST')

    return LaunchDescription([
        rmw_implementation,
        nav2_domain,
        localhost_only,
        local_discovery,
        headless_arg,
        nav2_launch,
    ])
