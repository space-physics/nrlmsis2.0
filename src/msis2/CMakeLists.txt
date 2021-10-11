cmake_minimum_required(VERSION 3.15...3.21)

project(MSIS2
  LANGUAGES Fortran
  DESCRIPTION "Build and use MSIS 2.0 from Python"
  HOMEPAGE_URL https://map.nrl.navy.mil/map/pub/nrl/NRLMSIS/NRLMSIS2.0/
)

set(FETCHCONTENT_UPDATES_DISCONNECTED_MSIS2 true)

include(cmake/msis2.cmake)

add_executable(msis2driver msis2driver.f90)
target_link_libraries(msis2driver PRIVATE msis2)
set_target_properties(msis2driver PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR})

# MSIS 2.0 exe needs this parm file
if(NOT EXISTS ${PROJECT_SOURCE_DIR}/msis20.parm)
  file(COPY ${msis2proj_SOURCE_DIR}/msis20.parm DESTINATION ${PROJECT_SOURCE_DIR})
endif()
