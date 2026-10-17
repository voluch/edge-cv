cmake_minimum_required(VERSION 3.16)
project(ecv_common VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_library(ecv_common
  src_cpp/types.cpp
  src_cpp/geometry.cpp
  src_cpp/bench.cpp
)
add_library(ecv::common ALIAS ecv_common)
target_include_directories(ecv_common PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)
target_compile_options(ecv_common PRIVATE -Wall -Wextra)

# Only build tests when this is the top-level project (not via add_subdirectory)
if(CMAKE_SOURCE_DIR STREQUAL CMAKE_CURRENT_SOURCE_DIR)
  enable_testing()
  add_executable(test_common tests_cpp/test_common.cpp)
  target_link_libraries(test_common PRIVATE ecv_common)
  add_test(NAME common COMMAND test_common)
endif()
