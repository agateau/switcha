find_package(KDE3 REQUIRED)
include_directories(
	${KDE3_INCLUDE_DIR}
	${QT_INCLUDE_DIR}
	${CMAKE_BINARY_DIR})
link_directories(${KDE3_LIB_DIR})

set(switcha_SRCS
	main.cpp
	window.cpp)

kde3_automoc(${switcha_SRCS})

add_executable(switcha ${switcha_SRCS})
target_link_libraries(switcha ${QT_AND_KDECORE_LIBS} kdeui kio)
