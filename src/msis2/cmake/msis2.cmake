include(FetchContent)
include(CheckFortranCompilerFlag)

FetchContent_Declare(msis2proj
URL https://map.nrl.navy.mil/map/pub/nrl/NRLMSIS/NRLMSIS2.0/NRLMSIS2.0.zip
URL_HASH SHA256=bcaf1d0e233dd7a5547b2f0a00c7a83dffa4338475848f696a3a3de253c3c987
)

FetchContent_MakeAvailable(msis2proj)

set(_s ${msis2proj_SOURCE_DIR})  # convenience

add_library(msis2 ${_s}/alt2gph.F90 ${_s}/msis_constants.F90 ${_s}/msis_init.F90 ${_s}/msis_gfn.F90 ${_s}/msis_tfn.F90 ${_s}/msis_dfn.F90 ${_s}/msis_calc.F90 ${_s}/msis_gtd8d.F90)
set_target_properties(msis2 PROPERTIES Fortran_MODULE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/include)
target_include_directories(msis2 INTERFACE ${CMAKE_CURRENT_BINARY_DIR}/include)
if(CMAKE_Fortran_COMPILER_ID STREQUAL GNU)
  # msis_calc:bspline has argument mismatch on nodes variable
  target_compile_options(msis2 PRIVATE -std=legacy)
endif()

if(BUILD_TESTING)
  add_executable(msis2test ${msis2proj_SOURCE_DIR}/msis2.0_test.F90)
  target_link_libraries(msis2test PRIVATE msis2)

  add_test(NAME MSIS2
    COMMAND $<TARGET_FILE:msis2test>
    WORKING_DIRECTORY ${msis2proj_SOURCE_DIR})
endif()
