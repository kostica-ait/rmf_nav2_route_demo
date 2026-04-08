cmake_minimum_required(VERSION 3.8)
project(rmf_nav2_route_demo)

find_package(ament_cmake REQUIRED)

install(DIRECTORY
  config
  launch
  DESTINATION share/${PROJECT_NAME}/
)

ament_package()
