#####################################
cmake_minimum_required (VERSION 2.8)
project (shades)
set(raspicam_DIR "/usr/local/lib/cmake")
find_package(raspicam REQUIRED)
add_executable (shades shades.cpp)
target_link_libraries (shades ${raspicam_LIBS})
#####################################
