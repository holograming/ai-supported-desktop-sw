---
name: project-scaffolding
description: "C++/QML 프로젝트 스캐폴딩 - 표준 디렉토리 구조, 빌드 설정, OpenSpec 초기화"
---

# Project Scaffolding Skill

## Overview

새로운 C++/QML 프로젝트를 표준 구조로 생성하는 스킬입니다.

## Usage

```bash
# 스킬 호출 (task-manager가 담당)
/scaffold-project {project-name}
```

## Standard Structure

`.claude/templates/project-structure.md` 참조

## Scaffolding Steps

### Step 1: Create Directory Structure

```bash
mkdir -p {project-name}/{src,qml,tests,external,docs}
mkdir -p {project-name}/.claude/{agents,skills,templates,orchestrator}
mkdir -p {project-name}/openspec/{specs,changes}
mkdir -p {project-name}/.github/workflows
```

### Step 2: Initialize CMake

**CMakeLists.txt**
```cmake
cmake_minimum_required(VERSION 3.21)
project({project-name} VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Qt6
find_package(Qt6 REQUIRED COMPONENTS Core Quick Widgets)
qt_standard_project_setup()

# Sources
add_subdirectory(src)

# Tests
enable_testing()
add_subdirectory(tests)
```

**CMakePresets.json**
```json
{
  "version": 6,
  "configurePresets": [
    {
      "name": "base",
      "hidden": true,
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/${presetName}",
      "toolchainFile": "${sourceDir}/external/vcpkg/scripts/buildsystems/vcpkg.cmake"
    },
    {
      "name": "windows-debug",
      "inherits": "base",
      "displayName": "Windows Debug",
      "condition": { "type": "equals", "lhs": "${hostSystemName}", "rhs": "Windows" },
      "cacheVariables": { "CMAKE_BUILD_TYPE": "Debug" }
    },
    {
      "name": "windows-release",
      "inherits": "base",
      "displayName": "Windows Release",
      "condition": { "type": "equals", "lhs": "${hostSystemName}", "rhs": "Windows" },
      "cacheVariables": { "CMAKE_BUILD_TYPE": "Release" }
    },
    {
      "name": "linux-debug",
      "inherits": "base",
      "displayName": "Linux Debug",
      "condition": { "type": "equals", "lhs": "${hostSystemName}", "rhs": "Linux" },
      "cacheVariables": { "CMAKE_BUILD_TYPE": "Debug" }
    },
    {
      "name": "linux-release",
      "inherits": "base",
      "displayName": "Linux Release",
      "condition": { "type": "equals", "lhs": "${hostSystemName}", "rhs": "Linux" },
      "cacheVariables": { "CMAKE_BUILD_TYPE": "Release" }
    },
    {
      "name": "macos-debug",
      "inherits": "base",
      "displayName": "macOS Debug",
      "condition": { "type": "equals", "lhs": "${hostSystemName}", "rhs": "Darwin" },
      "cacheVariables": { "CMAKE_BUILD_TYPE": "Debug" }
    },
    {
      "name": "macos-release",
      "inherits": "base",
      "displayName": "macOS Release",
      "condition": { "type": "equals", "lhs": "${hostSystemName}", "rhs": "Darwin" },
      "cacheVariables": { "CMAKE_BUILD_TYPE": "Release" }
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

### Step 3: Initialize vcpkg

**vcpkg.json**
```json
{
  "name": "{project-name}",
  "version": "0.1.0",
  "dependencies": [
    "qt6",
    "fmt",
    "spdlog",
    "catch2"
  ]
}
```

```bash
# Add vcpkg submodule
git submodule add https://github.com/microsoft/vcpkg.git external/vcpkg
./external/vcpkg/bootstrap-vcpkg.sh
```

### Step 4: Initialize OpenSpec

```bash
# Create required files
touch openspec/project.md
touch openspec/AGENTS.md
```

**openspec/project.md** - project.md 템플릿 복사
**openspec/AGENTS.md** - AGENTS.md 템플릿 복사

### Step 5: Create CLAUDE.md

```markdown
<!-- OPENSPEC:START -->
# OpenSpec Instructions
...
<!-- OPENSPEC:END -->

# Project Name

## Tech Stack
- C++17
- Qt6/QML
- CMake 3.21+
- vcpkg
```

### Step 6: Initialize Git

```bash
git init
git add .
git commit -m "chore: initial project scaffold"
```

### Step 7: Verify Build

```bash
# Configure
cmake --preset {platform}-debug

# Build
cmake --build --preset {platform}-debug

# Test
ctest --preset {platform}-debug
```

## Build Folder Convention

**CRITICAL**: 모든 빌드 출력은 `build/${presetName}/` 경로 사용

| Preset | Build Directory |
|--------|-----------------|
| windows-debug | `build/windows-debug/` |
| windows-release | `build/windows-release/` |
| linux-debug | `build/linux-debug/` |
| linux-release | `build/linux-release/` |
| macos-debug | `build/macos-debug/` |
| macos-release | `build/macos-release/` |

## Validation

스캐폴딩 완료 후 검증:
- [ ] CMake configure 성공
- [ ] 빌드 성공
- [ ] 테스트 실행 성공
- [ ] .gitignore에 build/ 포함
- [ ] vcpkg 서브모듈 정상 작동
