---
name: modern-cmake
description: "Modern CMake practices - vcpkg integration, presets, Ninja generator, cross-platform configuration"
---

# Modern CMake Skill

## 1. CMake Best Practices for vcpkg Integration

### Project Structure Template

```
project-root/
├── CMakeLists.txt              # Root CMake configuration
├── CMakePresets.json           # Build presets (6 configurations)
├── vcpkg.json                  # Dependency manifest
├── external/
│   └── vcpkg/                  # vcpkg submodule
├── src/
│   ├── CMakeLists.txt          # Source CMake
│   └── main.cpp
├── tests/
│   ├── CMakeLists.txt          # Test CMake
│   └── test_*.cpp
├── .gitignore
└── build/                      # Build output (gitignored)
```

### Root CMakeLists.txt Template

```cmake
cmake_minimum_required(VERSION 3.21)

# CRITICAL: Must be BEFORE project() declaration
set(CMAKE_TOOLCHAIN_FILE
    "${CMAKE_CURRENT_SOURCE_DIR}/external/vcpkg/scripts/buildsystems/vcpkg.cmake"
    CACHE STRING "Vcpkg toolchain file")

project(MyProject
    VERSION 1.0.0
    LANGUAGES CXX
    DESCRIPTION "Modern C++ project with vcpkg"
)

# C++ Standard Configuration
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Output Directories
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib")
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib")

# Compilation Options
option(BUILD_TESTING "Build tests" ON)
option(BUILD_SHARED_LIBS "Build shared libraries" OFF)

# Find Packages (vcpkg handles dependency resolution)
find_package(fmt CONFIG REQUIRED)
find_package(spdlog CONFIG REQUIRED)
if(BUILD_TESTING)
    find_package(Catch2 CONFIG REQUIRED)
endif()

# Add Subdirectories
add_subdirectory(src)

if(BUILD_TESTING)
    enable_testing()
    add_subdirectory(tests)
endif()
```

### Modern CMake Principles

#### ✅ DO: Use Target-Based Design

```cmake
# Add executable/library
add_executable(my_app src/main.cpp)

# Configure compilation settings PER TARGET
target_compile_features(my_app PUBLIC cxx_std_20)
target_compile_options(my_app PRIVATE /W4)  # MSVC warning level

# Link libraries to target
target_link_libraries(my_app PRIVATE fmt::fmt spdlog::spdlog)

# Include directories are target-specific
target_include_directories(my_app PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)
```

#### ❌ DON'T: Use Global Settings

```cmake
# BAD - affects all targets globally
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_FLAGS "/W4")

# This makes it hard to manage multiple targets with different settings
```

#### Using Generator Expressions

```cmake
# Conditional compilation based on configuration
target_compile_options(my_app PRIVATE
    $<$<CONFIG:Debug>:-g -O0>
    $<$<CONFIG:Release>:-O3>
)

# Compiler-specific flags
target_compile_options(my_app PRIVATE
    $<$<CXX_COMPILER_ID:MSVC>:/W4>
    $<$<CXX_COMPILER_ID:GNU,Clang>:-Wall -Wextra>
)
```

---

## 2. CMakePresets.json Usage

### Why CMakePresets.json?

- **Standardization**: Same build configuration across all team members
- **Cross-platform**: Single file works on Windows/Linux/macOS
- **IDE support**: VS Code, CLion, Visual Studio all read presets
- **Reproducibility**: Ensures consistent builds in CI/CD
- **User customization**: CMakeUserPresets.json for personal overrides (gitignored)

### Complete CMakePresets.json Template

This template provides 6 build configurations (3 platforms × 2 build types):

```json
{
  "version": 6,
  "vendor": {
    "example.com/ExampleProject": {
      "autoFormat": true
    }
  },
  "cmakeMinimumRequired": {
    "major": 3,
    "minor": 21,
    "patch": 0
  },
  "configurePresets": [
    {
      "name": "base",
      "description": "Base configuration shared by all presets",
      "hidden": true,
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/${presetName}",
      "cacheVariables": {
        "CMAKE_TOOLCHAIN_FILE": "${sourceDir}/external/vcpkg/scripts/buildsystems/vcpkg.cmake",
        "CMAKE_EXPORT_COMPILE_COMMANDS": "ON"
      },
      "warnings": {
        "dev": true,
        "deprecated": true
      }
    },
    {
      "name": "windows-base",
      "description": "Windows base configuration",
      "hidden": true,
      "inherits": "base",
      "condition": {
        "type": "equals",
        "lhs": "${hostSystemName}",
        "rhs": "Windows"
      },
      "cacheVariables": {
        "VCPKG_TARGET_TRIPLET": "x64-windows"
      }
    },
    {
      "name": "linux-base",
      "description": "Linux base configuration",
      "hidden": true,
      "inherits": "base",
      "condition": {
        "type": "equals",
        "lhs": "${hostSystemName}",
        "rhs": "Linux"
      },
      "cacheVariables": {
        "VCPKG_TARGET_TRIPLET": "x64-linux"
      }
    },
    {
      "name": "macos-base",
      "description": "macOS base configuration",
      "hidden": true,
      "inherits": "base",
      "condition": {
        "type": "equals",
        "lhs": "${hostSystemName}",
        "rhs": "Darwin"
      },
      "cacheVariables": {
        "VCPKG_TARGET_TRIPLET": "x64-osx"
      }
    },
    {
      "name": "windows-debug",
      "displayName": "Windows Debug",
      "description": "Windows build with debug symbols",
      "inherits": "windows-base",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Debug"
      }
    },
    {
      "name": "windows-release",
      "displayName": "Windows Release",
      "description": "Windows optimized release build",
      "inherits": "windows-base",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release"
      }
    },
    {
      "name": "linux-debug",
      "displayName": "Linux Debug",
      "description": "Linux build with debug symbols",
      "inherits": "linux-base",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Debug"
      }
    },
    {
      "name": "linux-release",
      "displayName": "Linux Release",
      "description": "Linux optimized release build",
      "inherits": "linux-base",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release"
      }
    },
    {
      "name": "osx-debug",
      "displayName": "macOS Debug",
      "description": "macOS build with debug symbols",
      "inherits": "macos-base",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Debug"
      }
    },
    {
      "name": "osx-release",
      "displayName": "macOS Release",
      "description": "macOS optimized release build",
      "inherits": "macos-base",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release"
      }
    }
  ],
  "buildPresets": [
    {
      "name": "windows-debug",
      "configurePreset": "windows-debug",
      "configuration": "Debug",
      "jobs": 0,
      "targets": ["all"]
    },
    {
      "name": "windows-release",
      "configurePreset": "windows-release",
      "configuration": "Release",
      "jobs": 0,
      "targets": ["all"]
    },
    {
      "name": "linux-debug",
      "configurePreset": "linux-debug",
      "configuration": "Debug",
      "jobs": 0,
      "targets": ["all"]
    },
    {
      "name": "linux-release",
      "configurePreset": "linux-release",
      "configuration": "Release",
      "jobs": 0,
      "targets": ["all"]
    },
    {
      "name": "osx-debug",
      "configurePreset": "osx-debug",
      "configuration": "Debug",
      "jobs": 0,
      "targets": ["all"]
    },
    {
      "name": "osx-release",
      "configurePreset": "osx-release",
      "configuration": "Release",
      "jobs": 0,
      "targets": ["all"]
    }
  ],
  "testPresets": [
    {
      "name": "windows-debug",
      "configurePreset": "windows-debug",
      "output": {
        "outputOnFailure": true
      }
    },
    {
      "name": "linux-debug",
      "configurePreset": "linux-debug",
      "output": {
        "outputOnFailure": true
      }
    },
    {
      "name": "osx-debug",
      "configurePreset": "osx-debug",
      "output": {
        "outputOnFailure": true
      }
    }
  ]
}
```

### Preset Inheritance Hierarchy

```
base (hidden - shared by all)
├── windows-base (hidden - Windows-specific)
│   ├── windows-debug (final - user-facing)
│   └── windows-release (final - user-facing)
├── linux-base (hidden - Linux-specific)
│   ├── linux-debug (final - user-facing)
│   └── linux-release (final - user-facing)
└── macos-base (hidden - macOS-specific)
    ├── osx-debug (final - user-facing)
    └── osx-release (final - user-facing)
```

### CMakeUserPresets.json (User Customization)

Create `CMakeUserPresets.json` (gitignored) for personal overrides:

```json
{
  "version": 6,
  "configurePresets": [
    {
      "name": "dev",
      "inherits": "windows-debug",
      "cacheVariables": {
        "MY_CUSTOM_PATH": "C:/my/custom/path",
        "ENABLE_COVERAGE": "ON"
      }
    }
  ]
}
```

---

## 3. Ninja Generator Configuration

### Why Ninja?

| Feature | Ninja | MSBuild |
|---------|-------|---------|
| Speed | ⚡ Fast (parallel) | 🐢 Slower |
| Cross-platform | ✅ Yes (all OSes) | ❌ Windows only |
| Complexity | 📝 Simple | 📚 Complex |
| IDE integration | ⚠️ Limited | ✅ Native |
| Command-line | ✅ Excellent | 🟡 Good |

**Recommendation**: Use Ninja for most projects. It's faster, simpler, and works everywhere.

### Installation

#### Windows (via vcpkg - recommended)
```powershell
# Option 1: Via vcpkg
vcpkg install ninja:x64-windows

# Option 2: Via winget
winget install Ninja-build.Ninja

# Option 3: Via Chocolatey
choco install ninja

# Verify
ninja --version
```

#### Linux
```bash
# Ubuntu/Debian
sudo apt install ninja-build

# Fedora/RHEL
sudo dnf install ninja

# Arch Linux
sudo pacman -S ninja

# Verify
ninja --version
```

#### macOS
```bash
brew install ninja

# Verify
ninja --version
```

### Integration with CMakePresets.json

Already configured in the template above:
```json
{
  "name": "base",
  "generator": "Ninja",
  "binaryDir": "${sourceDir}/build/${presetName}"
}
```

### Manual Usage (without presets)

```bash
# Configure
cmake -G Ninja -S . -B build

# Build (with parallelization)
cmake --build build --parallel

# Build specific target
cmake --build build --target my_app

# Build with verbose output
cmake --build build --verbose
```

---

## 4. Cross-Platform Build Configuration

### Platform Detection in CMake

```cmake
if(WIN32)
    # Windows-specific settings
    target_compile_definitions(my_app PRIVATE PLATFORM_WINDOWS)
    if(MSVC)
        target_compile_options(my_app PRIVATE /W4 /permissive-)
    endif()

elseif(UNIX AND NOT APPLE)
    # Linux-specific settings
    target_compile_definitions(my_app PRIVATE PLATFORM_LINUX)
    target_compile_options(my_app PRIVATE -Wall -Wextra -Wpedantic)

elseif(APPLE)
    # macOS-specific settings
    target_compile_definitions(my_app PRIVATE PLATFORM_MACOS)
    target_compile_options(my_app PRIVATE -Wall -Wextra)

    # macOS-specific frameworks
    target_link_libraries(my_app PRIVATE
        "-framework CoreFoundation"
        "-framework AppKit"
    )
endif()
```

### Compiler-Specific Settings

```cmake
# MSVC (Microsoft Visual C++) - Windows
if(MSVC)
    target_compile_options(my_app PRIVATE
        /W4           # Warning level 4
        /WX           # Warnings as errors
        /permissive-  # Standards conformance
        /std:c++latest
    )
endif()

# GCC and Clang (Linux/macOS)
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(my_app PRIVATE
        -Wall         # All warnings
        -Wextra       # Extra warnings
        -Wpedantic    # Pedantic mode
        -Werror       # Warnings as errors
        -fPIC         # Position independent code
    )

    # For C++20 concepts
    if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
        target_compile_options(my_app PRIVATE -fconcepts)
    endif()
endif()
```

### vcpkg Triplet Selection

Handled automatically in CMakePresets.json based on platform detection:

```json
{
  "condition": {
    "type": "equals",
    "lhs": "${hostSystemName}",
    "rhs": "Windows"
  },
  "cacheVariables": {
    "VCPKG_TARGET_TRIPLET": "x64-windows"
  }
}
```

Manual override:
```bash
cmake --preset windows-debug -DVCPKG_TARGET_TRIPLET=x64-windows-static
```

---

## 5. SCRIPT SECTION: Complete Project Setup

### Windows Automated Setup - setup-project.ps1

```powershell
<#
.SYNOPSIS
    Automated C++ project setup with CMake, vcpkg, and Ninja
.PARAMETER ProjectName
    Name of the project to create
.PARAMETER VcpkgVersion
    vcpkg version to use (default: 2024.11.16)
#>

param(
    [string]$ProjectName = "MyCppProject",
    [string]$VcpkgVersion = "2024.11.16"
)

Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  C++ Project Setup with CMake & vcpkg  ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check prerequisites
Write-Host "✓ Checking prerequisites..." -ForegroundColor Yellow

$MissingTools = @()
if (-not (Get-Command cmake -ErrorAction SilentlyContinue)) { $MissingTools += "cmake" }
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { $MissingTools += "git" }
if (-not (Get-Command ninja -ErrorAction SilentlyContinue)) { $MissingTools += "ninja" }

if ($MissingTools.Count -gt 0) {
    Write-Host "✗ Missing tools: $($MissingTools -join ', ')" -ForegroundColor Red
    Write-Host "  Install them and try again." -ForegroundColor Red
    exit 1
}

Write-Host "✓ All prerequisites found!" -ForegroundColor Green
Write-Host ""

# Get CMakePresets.json from user
Write-Host "⚠ Important: You need CMakePresets.json to complete setup" -ForegroundColor Yellow
Write-Host "  Get it from the modern-cmake skill documentation" -ForegroundColor Yellow
Write-Host ""
$ReadyWithPresets = Read-Host "Ready to proceed? (y/n)"
if ($ReadyWithPresets -ne 'y') { exit 0 }

# 1. Create directory structure
Write-Host "📁 Creating directory structure..." -ForegroundColor Cyan
$dirs = @("src", "tests", "include", "external", "build")
foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

# 2. Initialize git
Write-Host "🔧 Initializing git repository..." -ForegroundColor Cyan
git init
git config user.email "developer@example.com"
git config user.name "Developer"

# 3. Setup vcpkg submodule
Write-Host "📦 Adding vcpkg as submodule (v$VcpkgVersion)..." -ForegroundColor Cyan
git submodule add https://github.com/microsoft/vcpkg.git external/vcpkg
Push-Location external/vcpkg
git checkout $VcpkgVersion
Pop-Location
git submodule update --init --recursive

# 4. Bootstrap vcpkg
Write-Host "⚙ Bootstrapping vcpkg..." -ForegroundColor Cyan
.\external\vcpkg\bootstrap-vcpkg.bat
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ vcpkg bootstrap failed!" -ForegroundColor Red
    exit 1
}

# 5. Create vcpkg.json
Write-Host "📄 Creating vcpkg.json..." -ForegroundColor Cyan
$vcpkgJson = @{
    name = $ProjectName.ToLower()
    version = "1.0.0"
    description = "Modern C++ project"
    dependencies = @("fmt", "spdlog", "catch2")
    "builtin-baseline" = "a42af01b72c28a8e1d7b48107b33e4f286a55ef6"
} | ConvertTo-Json -Depth 10
$vcpkgJson | Out-File -Encoding UTF8 vcpkg.json

# 6. Create CMakeLists.txt
Write-Host "📄 Creating CMakeLists.txt..." -ForegroundColor Cyan
@"
cmake_minimum_required(VERSION 3.21)

set(CMAKE_TOOLCHAIN_FILE
    "`${CMAKE_CURRENT_SOURCE_DIR}/external/vcpkg/scripts/buildsystems/vcpkg.cmake"
    CACHE STRING "Vcpkg toolchain file")

project($ProjectName VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "`${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "`${CMAKE_BINARY_DIR}/lib)

find_package(fmt CONFIG REQUIRED)
find_package(spdlog CONFIG REQUIRED)
find_package(Catch2 CONFIG REQUIRED)

add_subdirectory(src)
enable_testing()
add_subdirectory(tests)
"@ | Out-File -Encoding UTF8 CMakeLists.txt

# 7. Create subdirectory CMakeLists
Write-Host "📄 Creating src/CMakeLists.txt..." -ForegroundColor Cyan
@"
add_executable(my_app main.cpp)
target_link_libraries(my_app PRIVATE fmt::fmt spdlog::spdlog)
"@ | Out-File -Encoding UTF8 src/CMakeLists.txt

# 8. Create source files
Write-Host "📄 Creating src/main.cpp..." -ForegroundColor Cyan
@"
#include <fmt/core.h>
#include <spdlog/spdlog.h>

int main() {
    spdlog::info("Welcome to $ProjectName!");
    fmt::print("Modern C++ with vcpkg and CMake\n");
    return 0;
}
"@ | Out-File -Encoding UTF8 src/main.cpp

# 9. Create tests
Write-Host "📄 Creating test files..." -ForegroundColor Cyan
@"
add_executable(tests test_main.cpp)
target_link_libraries(tests PRIVATE Catch2::Catch2WithMain)
add_test(NAME tests COMMAND tests)
"@ | Out-File -Encoding UTF8 tests/CMakeLists.txt

@"
#include <catch2/catch_test_macros.hpp>

TEST_CASE("Basic arithmetic", "[basic]") {
    REQUIRE(2 + 2 == 4);
}
"@ | Out-File -Encoding UTF8 tests/test_main.cpp

# 10. Create .gitignore
Write-Host "📄 Creating .gitignore..." -ForegroundColor Cyan
@"
# Build
build/
cmake-build-*/

# IDE
.vscode/
.vs/
.idea/
*.user

# vcpkg
vcpkg_installed/
CMakeUserPresets.json

# Generated
compile_commands.json
"@ | Out-File -Encoding UTF8 .gitignore

# 11. Create CMakePresets.json
Write-Host "📄 Downloading CMakePresets.json..." -ForegroundColor Cyan
Write-Host "  ⚠ MANUAL STEP: Copy CMakePresets.json from modern-cmake skill" -ForegroundColor Yellow

# 12. Initial git commit
Write-Host "📝 Creating initial git commit..." -ForegroundColor Cyan
git add .gitignore vcpkg.json CMakeLists.txt "src/" "tests/" ".gitmodules"
git commit -m "Initial project setup with CMake and vcpkg"

Write-Host ""
Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║     Setup Complete!                    ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "  1. Copy CMakePresets.json from modern-cmake skill documentation" -ForegroundColor White
Write-Host "  2. cmake --preset windows-debug" -ForegroundColor White
Write-Host "  3. cmake --build --preset windows-debug" -ForegroundColor White
Write-Host ""
```

Save as `setup-project.ps1` and run:
```powershell
.\setup-project.ps1 -ProjectName "MyApp"
```

### Linux/macOS Automated Setup - setup-project.sh

```bash
#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

PROJECT_NAME="${1:-MyCppProject}"
VCPKG_VERSION="${2:-2024.11.16}"

echo -e "${CYAN}╔════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  C++ Project Setup with CMake & vcpkg  ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════╝${NC}"
echo ""

# Check prerequisites
echo -e "${YELLOW}✓ Checking prerequisites...${NC}"
MISSING_TOOLS=()
command -v cmake &> /dev/null || MISSING_TOOLS+=("cmake")
command -v git &> /dev/null || MISSING_TOOLS+=("git")
command -v ninja &> /dev/null || MISSING_TOOLS+=("ninja")

if [ ${#MISSING_TOOLS[@]} -gt 0 ]; then
    echo -e "${RED}✗ Missing tools: ${MISSING_TOOLS[*]}${NC}"
    echo -e "${RED}  Install them and try again.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ All prerequisites found!${NC}"
echo ""

# 1. Create directory structure
echo -e "${CYAN}📁 Creating directory structure...${NC}"
mkdir -p src tests include external build

# 2. Initialize git
echo -e "${CYAN}🔧 Initializing git repository...${NC}"
git init
git config user.email "developer@example.com"
git config user.name "Developer"

# 3. Setup vcpkg submodule
echo -e "${CYAN}📦 Adding vcpkg as submodule (v$VCPKG_VERSION)...${NC}"
git submodule add https://github.com/microsoft/vcpkg.git external/vcpkg
(cd external/vcpkg && git checkout $VCPKG_VERSION)
git submodule update --init --recursive

# 4. Bootstrap vcpkg
echo -e "${CYAN}⚙ Bootstrapping vcpkg...${NC}"
./external/vcpkg/bootstrap-vcpkg.sh
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ vcpkg bootstrap failed!${NC}"
    exit 1
fi

# 5. Create vcpkg.json
echo -e "${CYAN}📄 Creating vcpkg.json...${NC}"
cat > vcpkg.json << 'EOF'
{
  "name": "$(echo $PROJECT_NAME | tr '[:upper:]' '[:lower:]')",
  "version": "1.0.0",
  "description": "Modern C++ project",
  "dependencies": [
    "fmt",
    "spdlog",
    "catch2"
  ],
  "builtin-baseline": "a42af01b72c28a8e1d7b48107b33e4f286a55ef6"
}
EOF

# 6. Create CMakeLists.txt
echo -e "${CYAN}📄 Creating CMakeLists.txt...${NC}"
cat > CMakeLists.txt << 'EOF'
cmake_minimum_required(VERSION 3.21)

set(CMAKE_TOOLCHAIN_FILE ${CMAKE_CURRENT_SOURCE_DIR}/external/vcpkg/scripts/buildsystems/vcpkg.cmake
  CACHE STRING "Vcpkg toolchain file")

project(MyCppProject VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

find_package(fmt CONFIG REQUIRED)
find_package(spdlog CONFIG REQUIRED)
find_package(Catch2 CONFIG REQUIRED)

add_subdirectory(src)
enable_testing()
add_subdirectory(tests)
EOF

# 7. Create src/CMakeLists.txt
echo -e "${CYAN}📄 Creating src/CMakeLists.txt...${NC}"
cat > src/CMakeLists.txt << 'EOF'
add_executable(my_app main.cpp)
target_link_libraries(my_app PRIVATE fmt::fmt spdlog::spdlog)
EOF

# 8. Create src/main.cpp
echo -e "${CYAN}📄 Creating src/main.cpp...${NC}"
cat > src/main.cpp << 'EOF'
#include <fmt/core.h>
#include <spdlog/spdlog.h>

int main() {
    spdlog::info("Welcome to MyCppProject!");
    fmt::print("Modern C++ with vcpkg and CMake\n");
    return 0;
}
EOF

# 9. Create tests
echo -e "${CYAN}📄 Creating test files...${NC}"
cat > tests/CMakeLists.txt << 'EOF'
add_executable(tests test_main.cpp)
target_link_libraries(tests PRIVATE Catch2::Catch2WithMain)
add_test(NAME tests COMMAND tests)
EOF

cat > tests/test_main.cpp << 'EOF'
#include <catch2/catch_test_macros.hpp>

TEST_CASE("Basic arithmetic", "[basic]") {
    REQUIRE(2 + 2 == 4);
}
EOF

# 10. Create .gitignore
echo -e "${CYAN}📄 Creating .gitignore...${NC}"
cat > .gitignore << 'EOF'
# Build
build/
cmake-build-*/

# IDE
.vscode/
.vs/
.idea/
*.user

# vcpkg
vcpkg_installed/
CMakeUserPresets.json

# Generated
compile_commands.json
EOF

# 11. Initial git commit
echo -e "${CYAN}📝 Creating initial git commit...${NC}"
git add .gitignore vcpkg.json CMakeLists.txt src/ tests/ .gitmodules 2>/dev/null
git commit -m "Initial project setup with CMake and vcpkg"

echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     Setup Complete!                    ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}📋 Next steps:${NC}"
echo "  1. Copy CMakePresets.json from modern-cmake skill documentation"
echo "  2. cmake --preset linux-debug  # or osx-debug"
echo "  3. cmake --build --preset linux-debug"
echo ""
```

Save as `setup-project.sh` and run:
```bash
chmod +x setup-project.sh
./setup-project.sh "MyApp" "2024.11.16"
```

---

## 6. Build Commands Reference

### Using CMakePresets.json (Recommended)

```bash
# List available presets
cmake --list-presets

# Configure (automatic platform detection)
cmake --preset windows-debug
cmake --preset linux-release
cmake --preset osx-debug

# Build
cmake --build --preset windows-debug
cmake --build --preset linux-debug --parallel 8

# Run tests
ctest --preset windows-debug --output-on-failure

# Verbose output
cmake --build --preset windows-debug -- --verbose
```

### Manual Configuration (without presets)

```bash
# Configure with Ninja
cmake -G Ninja -S . -B build \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_TOOLCHAIN_FILE=external/vcpkg/scripts/buildsystems/vcpkg.cmake \
  -DVCPKG_TARGET_TRIPLET=x64-windows

# Build
cmake --build build --parallel 8

# Install (if configured)
cmake --install build --prefix /usr/local
```

### Clean Builds

```bash
# Remove build directory
rm -rf build/  # Linux/macOS
rmdir /s build  # Windows

# Clean specific preset
cmake --build --preset windows-debug --target clean
```

---

## 7. Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Ninja not found | Not installed | Install ninja via package manager or winget |
| Preset "X" not found | Typo or wrong platform | Run `cmake --list-presets` to see available presets |
| CMAKE_TOOLCHAIN_FILE not found | Wrong path | Verify path in CMakeLists.txt and CMakePresets.json |
| VCPKG_TARGET_TRIPLET mismatch | Platform detection failed | Manually set triplet: `cmake --preset windows-debug -DVCPKG_TARGET_TRIPLET=x64-windows` |
| Build type mismatch | Debug/Release mismatch | Ensure preset build type matches CMake build type |
| Permission denied | File access issue | Check file permissions, run as admin if needed |
| Module not found | vcpkg not initialized | Run `git submodule update --init --recursive` |

---

## 8. Build Folder Convention (CRITICAL)

모든 빌드 출력은 **반드시** `build/${presetName}/` 경로를 사용해야 합니다.

### 규칙

```
build/
├── windows-debug/      # Windows Debug 빌드
│   ├── bin/            # 실행 파일
│   └── lib/            # 라이브러리
├── windows-release/    # Windows Release 빌드
├── linux-debug/        # Linux Debug 빌드
├── linux-release/      # Linux Release 빌드
├── macos-debug/        # macOS Debug 빌드
└── macos-release/      # macOS Release 빌드
```

### CMakePresets.json 필수 설정

```json
{
  "name": "base",
  "hidden": true,
  "binaryDir": "${sourceDir}/build/${presetName}"  // ← 필수
}
```

### CMakeLists.txt 출력 디렉토리

```cmake
# 빌드 출력 경로 (CMAKE_BINARY_DIR은 binaryDir와 동일)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib")
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib")
```

### 금지 패턴

다음 경로는 사용하지 마세요:
- ❌ `out/build/`
- ❌ `cmake-build-*/`
- ❌ `Debug/`, `Release/` (루트 레벨)
- ❌ `x64/`, `x86/`

### .gitignore

```gitignore
# Build output (all presets)
build/
out/

# vcpkg
vcpkg_installed/
```

---

## 9. Best Practices Summary

1. **Always use CMakePresets.json** - Ensures consistency across team
2. **Use Ninja generator** - Fastest, simplest, most portable
3. **Use target-based CMake** - Easier to manage, more flexible
4. **Pin vcpkg version** - Same submodule commit everywhere
5. **Set CMAKE_TOOLCHAIN_FILE before project()** - Critical for vcpkg
6. **Enable compile_commands.json** - Better IDE support
7. **Gitignore build/**, **CMakeUserPresets.json**, **vcpkg_installed/**
8. **Test on all platforms** - Windows, Linux, macOS
9. **Use generator expressions** - For platform-specific settings
10. **Document your presets** - Add displayName and description
11. **Build folder convention** - Use `build/${presetName}/` path (Section 8)

---

## References

- [CMakePresets.json Official Documentation](https://cmake.org/cmake/help/latest/manual/cmake-presets.7.html)
- [CMake Modern Best Practices](https://gist.github.com/mbinna/c61dbb39bca0e4fb7d1f73b0d66a4fd1)
- [lukka/CppCMakeVcpkgTemplate](https://github.com/lukka/CppCMakeVcpkgTemplate)
- [Ninja Build System](https://ninja-build.org/)
- [CMake Official Site](https://cmake.org/)
