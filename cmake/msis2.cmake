include(FetchContent)
include(CheckFortranCompilerFlag)

FetchContent_Declare(msis2proj
URL https://map.nrl.navy.mil/map/pub/nrl/NRLMSIS/NRLMSIS2.0/NRLMSIS2.0.zip
URL_HASH SHA1=fa817dfee637ec2298a6ec882345d13d0b087a85
UPDATE_DISCONNECTED true
)

FetchContent_MakeAvailable(msis2proj)

set(_s ${msis2proj_SOURCE_DIR})  # convenience

add_library(msis2 ${_s}/alt2gph.F90 ${_s}/msis_constants.F90 ${_s}/msis_init.F90 ${_s}/msis_gfn.F90 ${_s}/msis_tfn.F90 ${_s}/msis_dfn.F90 ${_s}/msis_calc.F90 ${_s}/msis_gtd8d.F90)
if(CMAKE_Fortran_COMPILER_ID STREQUAL GNU)
  # msis_calc:bspline has argument mismatch on nodes variable
  target_compile_options(msis2 PRIVATE -std=legacy)
endif()
