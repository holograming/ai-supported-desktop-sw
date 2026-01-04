# Project Scaffolding Spec

## Overview

프로젝트 스캐폴딩은 C++/QML 프로젝트의 표준 디렉토리 구조와 설정 파일을 생성합니다.
Modern CMake, vcpkg, 크로스 플랫폼 빌드를 지원합니다.

## Version

- Current: 1.0.0
- Last Updated: 2026-01-04

---

## Standard Directory Structure

```
project-root/
├── .claude/                    # Claude Code 설정
│   ├── agents/                 # 에이전트 정의
│   ├── skills/                 # 스킬 정의
│   ├── orchestrator/           # 워크플로우 오케스트레이터
│   ├── templates/              # 프로젝트 템플릿
│   ├── settings.json           # 설정
│   └── workflow.json           # 워크플로우 규칙
│
├── openspec/                   # OpenSpec 문서
│   ├── project.md              # 프로젝트 규칙
│   ├── specs/                  # 현재 스펙
│   ├── changes/                # 변경 제안
│   └── AGENTS.md               # AI 에이전트 지침
│
├── src/                        # 소스 코드
│   ├── core/                   # 핵심 비즈니스 로직
│   ├── ui/                     # QML UI 컴포넌트
│   ├── services/               # 서비스 레이어
│   ├── utils/                  # 유틸리티
│   └── main.cpp                # 진입점
│
├── include/                    # 공개 헤더
│   └── ${PROJECT}/             # 네임스페이스 디렉토리
│
├── tests/                      # 테스트
│   ├── unit/                   # 단위 테스트
│   └── integration/            # 통합 테스트
│
├── resources/                  # 리소스 파일
│   ├── qml/                    # QML 파일
│   ├── images/                 # 이미지
│   └── fonts/                  # 폰트
│
├── docs/                       # 문서
│
├── build/                      # 빌드 출력 (gitignore)
│   ├── windows-debug/
│   ├── windows-release/
│   ├── linux-debug/
│   └── ...
│
├── CMakeLists.txt              # 루트 CMake 설정
├── CMakePresets.json           # CMake 프리셋
├── vcpkg.json                  # vcpkg 의존성
└── .gitignore                  # Git 무시 패턴
```

---

## CMake Configuration

### CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.21)
project(${PROJECT_NAME} VERSION 0.1.0 LANGUAGES CXX)

# C++ Standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Qt Auto-tools
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# Find packages
find_package(Qt6 REQUIRED COMPONENTS Core Quick Widgets)

# Source files
file(GLOB_RECURSE SOURCES src/*.cpp)
file(GLOB_RECURSE HEADERS include/${PROJECT_NAME}/*.h src/*.h)
file(GLOB_RECURSE QML_FILES resources/qml/*.qml)

# Executable
qt_add_executable(${PROJECT_NAME}
    ${SOURCES}
    ${HEADERS}
)

# QML Module
qt_add_qml_module(${PROJECT_NAME}
    URI ${PROJECT_NAME}
    VERSION 1.0
    QML_FILES ${QML_FILES}
)

# Link libraries
target_link_libraries(${PROJECT_NAME} PRIVATE
    Qt6::Core
    Qt6::Quick
    Qt6::Widgets
)

# Include directories
target_include_directories(${PROJECT_NAME} PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)

# Tests
if(BUILD_TESTING)
    enable_testing()
    add_subdirectory(tests)
endif()
```

---

## CMake Presets

### CMakePresets.json

```json
{
  "version": 6,
  "cmakeMinimumRequired": { "major": 3, "minor": 21, "patch": 0 },
  "configurePresets": [
    {
      "name": "base",
      "hidden": true,
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/${presetName}",
      "cacheVariables": {
        "CMAKE_TOOLCHAIN_FILE": {
          "type": "FILEPATH",
          "value": "$env{VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake"
        }
      }
    },
    {
      "name": "windows-debug",
      "inherits": "base",
      "displayName": "Windows Debug",
      "condition": { "type": "equals", "lhs": "${hostSystemName}", "rhs": "Windows" },
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Debug",
        "VCPKG_TARGET_TRIPLET": "x64-windows"
      }
    },
    {
      "name": "windows-release",
      "inherits": "base",
      "displayName": "Windows Release",
      "condition": { "type": "equals", "lhs": "${hostSystemName}", "rhs": "Windows" },
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release",
        "VCPKG_TARGET_TRIPLET": "x64-windows"
      }
    },
    {
      "name": "linux-debug",
      "inherits": "base",
      "displayName": "Linux Debug",
      "condition": { "type": "equals", "lhs": "${hostSystemName}", "rhs": "Linux" },
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Debug",
        "VCPKG_TARGET_TRIPLET": "x64-linux"
      }
    },
    {
      "name": "linux-release",
      "inherits": "base",
      "displayName": "Linux Release",
      "condition": { "type": "equals", "lhs": "${hostSystemName}", "rhs": "Linux" },
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release",
        "VCPKG_TARGET_TRIPLET": "x64-linux"
      }
    },
    {
      "name": "macos-debug",
      "inherits": "base",
      "displayName": "macOS Debug",
      "condition": { "type": "equals", "lhs": "${hostSystemName}", "rhs": "Darwin" },
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Debug",
        "VCPKG_TARGET_TRIPLET": "x64-osx"
      }
    },
    {
      "name": "macos-release",
      "inherits": "base",
      "displayName": "macOS Release",
      "condition": { "type": "equals", "lhs": "${hostSystemName}", "rhs": "Darwin" },
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release",
        "VCPKG_TARGET_TRIPLET": "x64-osx"
      }
    }
  ],
  "buildPresets": [
    { "name": "windows-debug", "configurePreset": "windows-debug" },
    { "name": "windows-release", "configurePreset": "windows-release" },
    { "name": "linux-debug", "configurePreset": "linux-debug" },
    { "name": "linux-release", "configurePreset": "linux-release" },
    { "name": "macos-debug", "configurePreset": "macos-debug" },
    { "name": "macos-release", "configurePreset": "macos-release" }
  ],
  "testPresets": [
    { "name": "windows-debug", "configurePreset": "windows-debug" },
    { "name": "linux-debug", "configurePreset": "linux-debug" },
    { "name": "macos-debug", "configurePreset": "macos-debug" }
  ]
}
```

---

## vcpkg Configuration

### vcpkg.json

```json
{
  "name": "project-name",
  "version-string": "0.1.0",
  "dependencies": [
    {
      "name": "qtbase",
      "default-features": false,
      "features": ["widgets", "gui", "concurrent"]
    },
    "qtdeclarative",
    "qtquickcontrols2"
  ],
  "builtin-baseline": "latest"
}
```

---

## Build Folder Convention

### Critical Rule

모든 빌드 출력은 반드시 `build/${presetName}/` 경로를 사용:

```
build/
├── windows-debug/
├── windows-release/
├── linux-debug/
├── linux-release/
├── macos-debug/
└── macos-release/
```

### Forbidden Patterns

```
✗ build/Debug/          # 플랫폼 정보 없음
✗ out/build/            # 비표준 경로
✗ cmake-build-debug/    # IDE 특정 경로
✗ build-windows/        # 빌드 타입 없음
```

---

## .gitignore

```gitignore
# Build
build/
out/
cmake-build-*/

# IDE
.vs/
.vscode/
.idea/
*.user

# Compiled
*.o
*.obj
*.exe
*.dll
*.so
*.dylib

# Qt
moc_*.cpp
ui_*.h
qrc_*.cpp
*.qmlc
*.jsc

# vcpkg
vcpkg_installed/

# OS
.DS_Store
Thumbs.db

# Worktrees
.worktrees/
```

---

## Scaffolding Command

### Usage

```bash
/project:scaffold --name MyApp --type desktop
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| --name | 프로젝트 이름 | Required |
| --type | 프로젝트 타입 (desktop, library) | desktop |
| --qt-version | Qt 버전 | 6 |
| --no-tests | 테스트 디렉토리 생략 | false |

### Generated Files

1. `CMakeLists.txt`
2. `CMakePresets.json`
3. `vcpkg.json`
4. `.gitignore`
5. `src/main.cpp`
6. `resources/qml/Main.qml`

---

## Related Skills

- `vcpkg-manager` - 의존성 관리
- `modern-cmake` - CMake 설정
- `qml-desktop-ui` - QML UI 개발

---

## Related Specs

- [Orchestration](../orchestration/spec.md)
