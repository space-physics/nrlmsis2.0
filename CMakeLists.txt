cmake_minimum_required(VERSION 3.15)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "release or debug")
endif()

project(MSIS2
  LANGUAGES Fortran
  DESCRIPTION "Build and use MSIS 2.0 from CMake projects"
  HOMEPAGE_URL https://map.nrl.navy.mil/map/pub/nrl/NRLMSIS/NRLMSIS2.0/)

include(CTest)

include(cmake/msis2.cmake)


# if(BUILD_TESTING)
#   add_subdirectory(tests)
# endif()
