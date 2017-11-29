project(glfw-examples)
cmake_minimum_required(VERSION 2.8.12)

include_directories(${glfw_INCLUDE_DIRS} "${CMAKE_SOURCE_DIR}/deps")

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

if (MATH_LIBRARY)
    link_libraries("${MATH_LIBRARY}")
endif()

if (MSVC)
    add_definitions(-D_CRT_SECURE_NO_WARNINGS)
endif()

if (GLFW_USE_OSMESA)
    add_definitions(-DUSE_NATIVE_OSMESA)
endif()

if (WIN32)
    set(ICON glfw.rc)
elseif (APPLE)
    set(ICON glfw.icns)
    set_source_files_properties(glfw.icns PROPERTIES
        MACOSX_PACKAGE_LOCATION "Resources")
endif()

set(GLAD "${CMAKE_SOURCE_DIR}/deps/glad/glad.h"
         "${CMAKE_SOURCE_DIR}/deps/glad.c")
set(GETOPT "${CMAKE_SOURCE_DIR}/deps/getopt.h"
           "${CMAKE_SOURCE_DIR}/deps/getopt.c")
set(TINYCTHREAD "${CMAKE_SOURCE_DIR}/deps/tinycthread.h"
                "${CMAKE_SOURCE_DIR}/deps/tinycthread.c")

add_executable(boing WIN32 MACOSX_BUNDLE boing.c ${ICON} ${GLAD})
add_executable(gears WIN32 MACOSX_BUNDLE gears.c ${ICON} ${GLAD})
add_executable(heightmap WIN32 MACOSX_BUNDLE heightmap.c ${ICON} ${GLAD})
add_executable(particles WIN32 MACOSX_BUNDLE particles.c ${ICON} ${TINYCTHREAD} ${GETOPT} ${GLAD})
add_executable(simple WIN32 MACOSX_BUNDLE simple.c ${ICON} ${GLAD})
add_executable(splitview WIN32 MACOSX_BUNDLE splitview.c ${ICON} ${GLAD})
add_executable(wave WIN32 MACOSX_BUNDLE wave.c ${ICON} ${GLAD})

target_link_libraries(boing ${CONAN_LIBS})
target_link_libraries(gears ${CONAN_LIBS})
target_link_libraries(heightmap ${CONAN_LIBS})
target_link_libraries(simple ${CONAN_LIBS})
target_link_libraries(splitview ${CONAN_LIBS})
target_link_libraries(wave ${CONAN_LIBS})
target_link_libraries(particles ${CMAKE_THREAD_LIBS_INIT} ${CONAN_LIBS})
if (RT_LIBRARY)
    target_link_libraries(particles "${RT_LIBRARY}")
endif()

set(WINDOWS_BINARIES boing gears heightmap particles simple splitview wave)

set_target_properties(${WINDOWS_BINARIES} ${CONSOLE_BINARIES} PROPERTIES
                      FOLDER "GLFW3/Examples")

if (MSVC)
    # Tell MSVC to use main instead of WinMain for Windows subsystem executables
    set_target_properties(${WINDOWS_BINARIES} PROPERTIES
                          LINK_FLAGS "/ENTRY:mainCRTStartup")
endif()

if (APPLE)
    set_target_properties(boing PROPERTIES MACOSX_BUNDLE_BUNDLE_NAME "Boing")
    set_target_properties(gears PROPERTIES MACOSX_BUNDLE_BUNDLE_NAME "Gears")
    set_target_properties(heightmap PROPERTIES MACOSX_BUNDLE_BUNDLE_NAME "Heightmap")
    set_target_properties(particles PROPERTIES MACOSX_BUNDLE_BUNDLE_NAME "Particles")
    set_target_properties(simple PROPERTIES MACOSX_BUNDLE_BUNDLE_NAME "Simple")
    set_target_properties(splitview PROPERTIES MACOSX_BUNDLE_BUNDLE_NAME "SplitView")
    set_target_properties(wave PROPERTIES MACOSX_BUNDLE_BUNDLE_NAME "Wave")

    set_target_properties(${WINDOWS_BINARIES} PROPERTIES
                          RESOURCE glfw.icns
                          MACOSX_BUNDLE_SHORT_VERSION_STRING ${GLFW_VERSION}
                          MACOSX_BUNDLE_LONG_VERSION_STRING ${GLFW_VERSION_FULL}
                          MACOSX_BUNDLE_ICON_FILE glfw.icns
                          MACOSX_BUNDLE_INFO_PLIST "${CMAKE_SOURCE_DIR}/CMake/MacOSXBundleInfo.plist.in")
endif()