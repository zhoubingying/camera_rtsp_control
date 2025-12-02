cmake_minimum_required(VERSION 3.10)
project(camera_rtsp_subscribe)

# 设置C++标准
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 查找OpenCV包
find_package(OpenCV REQUIRED)

# 添加可执行文件
add_executable(${PROJECT_NAME} src/main.cpp)

# 链接OpenCV库
target_link_libraries(${PROJECT_NAME} PRIVATE ${OpenCV_LIBS})

# 设置包含目录
target_include_directories(${PROJECT_NAME} PRIVATE ${OpenCV_INCLUDE_DIRS})

# 复制配置文件到构建目录
file(COPY ${CMAKE_SOURCE_DIR}/config_files DESTINATION ${CMAKE_BINARY_DIR}) 