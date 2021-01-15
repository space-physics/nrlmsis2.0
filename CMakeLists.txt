cmake_minimum_required(VERSION 3.15)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "release or debug")
endif()

project(MSIS2 LANGUAGES Fortran)

include(CTest)

include(src/msis2/cmake/msis2.cmake)
