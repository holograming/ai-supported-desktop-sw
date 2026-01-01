cmake_minimum_required(VERSION 3.25)

project(toss-pos VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

# Qt 패키지 찾기
find_package(Qt6 6.5 REQUIRED COMPONENTS
    Core
    Gui
    Quick
    QuickControls2
    Sql
)

qt_standard_project_setup(REQUIRES 6.5)

# 실행 파일 정의
qt_add_executable(${PROJECT_NAME}
    main.cpp
    src/database/db_manager.h
    src/database/db_manager.cpp
    src/types/product.h
    src/types/order.h
)

# TossTheme 싱글톤 등록
set_source_files_properties(qml/theme/TossTheme.qml
    PROPERTIES QT_QML_SINGLETON_TYPE TRUE
)

# QML 모듈 정의
qt_add_qml_module(${PROJECT_NAME}
    URI TossPos
    VERSION 1.0
    QML_FILES
        qml/Main.qml
        qml/theme/TossTheme.qml
        qml/pages/OrderPage.qml
        qml/pages/PaymentPage.qml
        qml/pages/ReportPage.qml
        qml/components/TossButton.qml
        qml/components/TossCard.qml
        qml/components/ProductCard.qml
        qml/components/CategoryBar.qml
        qml/components/OrderPanel.qml
        qml/components/OrderItemRow.qml
    SOURCES
        src/models/category_model.h src/models/category_model.cpp
        src/models/product_model.h src/models/product_model.cpp
        src/models/order_model.h src/models/order_model.cpp
        src/services/order_service.h src/services/order_service.cpp
        src/services/report_service.h src/services/report_service.cpp
    RESOURCES
        resources/sample_data.sql
    NO_RESOURCE_TARGET_PATH
)

# Qt 라이브러리 링크
target_link_libraries(${PROJECT_NAME} PRIVATE
    Qt6::Core
    Qt6::Gui
    Qt6::Quick
    Qt6::QuickControls2
    Qt6::Sql
)

# Include 경로 설정
target_include_directories(${PROJECT_NAME} PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/src
    ${CMAKE_CURRENT_SOURCE_DIR}/src/models
    ${CMAKE_CURRENT_SOURCE_DIR}/src/services
    ${CMAKE_CURRENT_SOURCE_DIR}/src/database
    ${CMAKE_CURRENT_SOURCE_DIR}/src/types
)

# macOS 번들 설정
if(APPLE)
    set_target_properties(${PROJECT_NAME} PROPERTIES
        MACOSX_BUNDLE TRUE
        MACOSX_BUNDLE_GUI_IDENTIFIER com.tossplace.pos
        MACOSX_BUNDLE_BUNDLE_VERSION ${PROJECT_VERSION}
        MACOSX_BUNDLE_SHORT_VERSION_STRING ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}
    )
endif()

# Windows 설정
if(WIN32)
    set_target_properties(${PROJECT_NAME} PROPERTIES
        WIN32_EXECUTABLE TRUE
    )
endif()

# 설치 설정
include(GNUInstallDirs)
install(TARGETS ${PROJECT_NAME}
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
