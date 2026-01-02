---
name: vcpkg-manager
description: "vcpkg dependency management - installation, binary caching, triplet configuration, and C++ project setup"
---

# vcpkg Manager Skill

## 1. vcpkg Installation (Submodule Method)

### Why Submodule?
- **Consistent version across team**: Everyone uses the same vcpkg commit
- **Reproducible builds**: Same dependencies, same versions everywhere
- **Avoids global installation bloat**: vcpkg stays within project scope
- **Easy CI/CD integration**: Git automatically clones submodule

### Installation Steps

#### Windows (PowerShell)
```powershell
# Add vcpkg as submodule
git submodule add https://github.com/microsoft/vcpkg.git external/vcpkg
cd external/vcpkg

# Pin to a stable version
git checkout 2024.11.16

# Return to project root
cd ../..

# Update submodule reference
git submodule update --init --recursive

# Bootstrap vcpkg
.\external\vcpkg\bootstrap-vcpkg.bat

# Verify installation
.\external\vcpkg\vcpkg --version
```

#### Linux (Bash)
```bash
# Add vcpkg as submodule
git submodule add https://github.com/microsoft/vcpkg.git external/vcpkg
cd external/vcpkg

# Pin to a stable version
git checkout 2024.11.16

# Return to project root
cd ../..

# Update submodule reference
git submodule update --init --recursive

# Bootstrap vcpkg
./external/vcpkg/bootstrap-vcpkg.sh

# Verify installation
./external/vcpkg/vcpkg --version
```

#### macOS (Bash)
```bash
# Add vcpkg as submodule
git submodule add https://github.com/microsoft/vcpkg.git external/vcpkg
cd external/vcpkg

# Pin to a stable version
git checkout 2024.11.16

# Return to project root
cd ../..

# Update submodule reference
git submodule update --init --recursive

# Bootstrap vcpkg
./external/vcpkg/bootstrap-vcpkg.sh

# Install required system dependencies
brew install pkg-config

# Verify installation
./external/vcpkg/vcpkg --version
```

---

## 2. Binary Caching Configuration

### Why Binary Caching?
Binary caching dramatically speeds up builds by reusing pre-compiled dependencies instead of rebuilding from source every time.

### Local Binary Cache Setup

#### Windows
```powershell
# Set environment variable for local binary cache
$env:VCPKG_BINARY_SOURCES = "clear;files,$env:LOCALAPPDATA\vcpkg\archives,readwrite"

# Make it permanent (Administrator required)
[Environment]::SetEnvironmentVariable("VCPKG_BINARY_SOURCES", "clear;files,$env:LOCALAPPDATA\vcpkg\archives,readwrite", [EnvironmentVariableTarget]::User)

# Verify
echo $env:VCPKG_BINARY_SOURCES
```

#### Linux
```bash
# Set environment variable for local binary cache
export VCPKG_BINARY_SOURCES="clear;files,$HOME/.vcpkg/archives,readwrite"

# Make it permanent (add to ~/.bashrc or ~/.zshrc)
echo 'export VCPKG_BINARY_SOURCES="clear;files,$HOME/.vcpkg/archives,readwrite"' >> ~/.bashrc

# Verify
echo $VCPKG_BINARY_SOURCES
```

#### macOS
```bash
# Set environment variable for local binary cache
export VCPKG_BINARY_SOURCES="clear;files,$HOME/.vcpkg/archives,readwrite"

# Make it permanent (add to ~/.zshrc or ~/.bash_profile)
echo 'export VCPKG_BINARY_SOURCES="clear;files,$HOME/.vcpkg/archives,readwrite"' >> ~/.zshrc

# Verify
echo $VCPKG_BINARY_SOURCES
```

### GitHub Actions Binary Cache

In your `.github/workflows/*.yml` files, add the following environment variable:

```yaml
env:
  VCPKG_BINARY_SOURCES: "clear;x-gha,readwrite"
```

This uses GitHub's built-in cache backend for faster CI builds. GitHub Actions will automatically:
- Cache compiled packages
- Restore them in subsequent workflow runs
- Share cache across jobs in the same workflow

### Binary Cache Configuration File

Create `.vcpkg/vcpkg-configuration.json` (optional, for advanced control):

```json
{
  "default-registry": {
    "kind": "git",
    "repository": "https://github.com/microsoft/vcpkg",
    "baseline": "a42af01b72c28a8e1d7b48107b33e4f286a55ef6"
  },
  "registries": []
}
```

---

## 3. Triplet Configuration

Triplets define the target platform, architecture, and linking strategy for dependencies.

### Standard Triplets

#### x64-windows (Windows 64-bit, Dynamic Linking)
Used for standard Windows applications with dynamic dependencies.
```cmake
# In CMakePresets.json
"cacheVariables": {
  "VCPKG_TARGET_TRIPLET": "x64-windows"
}
```

Key settings:
- Architecture: x64
- CRT Linkage: dynamic (shares Windows C runtime)
- Library Linkage: dynamic (DLL imports)

#### x64-windows-static (Windows 64-bit, Static Linking)
Used for self-contained applications.
```cmake
# In CMakePresets.json
"cacheVariables": {
  "VCPKG_TARGET_TRIPLET": "x64-windows-static"
}
```

Key settings:
- Architecture: x64
- CRT Linkage: static
- Library Linkage: static

#### x64-linux (Linux 64-bit)
Used for Linux applications.
```cmake
# In CMakePresets.json
"cacheVariables": {
  "VCPKG_TARGET_TRIPLET": "x64-linux"
}
```

Key settings:
- Architecture: x64
- Uses gcc/clang toolchain
- Dynamic linking by default

#### x64-osx (macOS 64-bit)
Used for macOS applications.
```cmake
# In CMakePresets.json
"cacheVariables": {
  "VCPKG_TARGET_TRIPLET": "x64-osx"
}
```

Key settings:
- Architecture: x64
- Uses Apple Clang
- Dynamic linking by default

### Custom Triplets

Create custom triplets in `external/vcpkg/triplets/community/`.

#### Example: x64-windows-static-md.cmake
```cmake
# Custom triplet for Windows with static library linkage but dynamic CRT
set(VCPKG_TARGET_ARCHITECTURE x64)
set(VCPKG_CRT_LINKAGE dynamic)
set(VCPKG_LIBRARY_LINKAGE static)
```

Use in CMakePresets.json:
```cmake
"cacheVariables": {
  "VCPKG_TARGET_TRIPLET": "x64-windows-static-md"
}
```

#### Example: x64-linux-musl.cmake
For Alpine Linux with musl libc:
```cmake
set(VCPKG_TARGET_ARCHITECTURE x64)
set(VCPKG_CMAKE_SYSTEM_NAME Linux)
set(VCPKG_LIBRARY_LINKAGE static)
```

---

## 4. Dependency Management with vcpkg.json

### Manifest Mode Best Practices

Manifest mode (`vcpkg.json`) is the recommended approach. It provides:
- Reproducible dependency resolution
- Version control of dependencies
- Per-project isolation

#### Basic vcpkg.json Template
```json
{
  "name": "my-cpp-project",
  "version": "1.0.0",
  "description": "A modern C++ project with vcpkg",
  "dependencies": [
    "fmt",
    "spdlog",
    "catch2"
  ],
  "builtin-baseline": "a42af01b72c28a8e1d7b48107b33e4f286a55ef6"
}
```

#### Advanced vcpkg.json with Version Constraints
```json
{
  "name": "my-cpp-project",
  "version": "1.0.0",
  "dependencies": [
    {
      "name": "fmt",
      "version>=": "10.0.0"
    },
    {
      "name": "spdlog",
      "version>=": "1.11.0"
    },
    {
      "name": "qt6",
      "platform": "windows"
    },
    {
      "name": "catch2",
      "features": ["shared"]
    }
  ],
  "builtin-baseline": "a42af01b72c28a8e1d7b48107b33e4f286a55ef6"
}
```

### Finding the Latest Baseline

To find the latest vcpkg baseline commit:

```bash
# Check remote repository for latest commit
curl https://api.github.com/repos/microsoft/vcpkg/commits | jq '.[0].sha'

# Or visit: https://github.com/microsoft/vcpkg/commits/master
```

---

## 5. Common vcpkg Commands

### Installation
```bash
# Install all dependencies (creates vcpkg_installed/)
vcpkg install --triplet x64-windows

# Install specific version
vcpkg install fmt:x64-windows

# Install with features
vcpkg install spdlog[fmt-support]:x64-windows
```

### Search and Discovery
```bash
# Search for packages
vcpkg search fmt

# Get package details
vcpkg info fmt

# List installed packages
vcpkg list
```

### Maintenance
```bash
# Update vcpkg itself
git -C external/vcpkg pull origin master
git -C external/vcpkg checkout 2024.11.16

# Remove outdated packages
vcpkg remove --outdated --recurse

# Clear build cache
rm -rf vcpkg_installed/  # On Linux/macOS
rmdir /s vcpkg_installed  # On Windows
```

---

## 6. SCRIPT SECTION: Creating C++ Project with vcpkg

### Project Directory Structure Template
```
my-cpp-project/
├── external/
│   └── vcpkg/              (git submodule)
├── src/
│   ├── main.cpp
│   └── CMakeLists.txt
├── tests/
│   ├── test_*.cpp
│   └── CMakeLists.txt
├── CMakeLists.txt          (root CMake)
├── CMakePresets.json       (build presets)
├── vcpkg.json              (dependencies)
├── .gitignore
└── .gitmodules
```

### Automated Project Setup - Windows (PowerShell)

Save as `setup-project.ps1`:

```powershell
param(
    [string]$ProjectName = "MyCppProject",
    [string]$VcpkgVersion = "2024.11.16"
)

Write-Host "Setting up $ProjectName..." -ForegroundColor Green

# 1. Create directory structure
$dirs = @("src", "tests", "external")
foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

# 2. Initialize git
git init

# 3. Setup vcpkg submodule
Write-Host "Adding vcpkg as submodule..." -ForegroundColor Cyan
git submodule add https://github.com/microsoft/vcpkg.git external/vcpkg
Push-Location external/vcpkg
git checkout $VcpkgVersion
Pop-Location
git submodule update --init --recursive

# 4. Bootstrap vcpkg
Write-Host "Bootstrapping vcpkg..." -ForegroundColor Cyan
.\external\vcpkg\bootstrap-vcpkg.bat

# 5. Create vcpkg.json
@"
{
  "name": "$($ProjectName.ToLower())",
  "version": "1.0.0",
  "description": "Modern C++ project",
  "dependencies": [
    "fmt",
    "spdlog",
    "catch2"
  ],
  "builtin-baseline": "a42af01b72c28a8e1d7b48107b33e4f286a55ef6"
}
"@ | Out-File -Encoding UTF8 vcpkg.json

# 6. Create root CMakeLists.txt
@"
cmake_minimum_required(VERSION 3.21)

set(CMAKE_TOOLCHAIN_FILE `${CMAKE_CURRENT_SOURCE_DIR}/external/vcpkg/scripts/buildsystems/vcpkg.cmake
  CACHE STRING "Vcpkg toolchain file")

project($ProjectName VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY `${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY `${CMAKE_BINARY_DIR}/lib)

find_package(fmt CONFIG REQUIRED)
find_package(spdlog CONFIG REQUIRED)
find_package(Catch2 CONFIG REQUIRED)

add_subdirectory(src)

enable_testing()
add_subdirectory(tests)
"@ | Out-File -Encoding UTF8 CMakeLists.txt

# 7. Create src/CMakeLists.txt
@"
add_executable(my_app main.cpp)
target_link_libraries(my_app PRIVATE fmt::fmt spdlog::spdlog)
"@ | Out-File -Encoding UTF8 src/CMakeLists.txt

# 8. Create src/main.cpp
@"
#include <fmt/core.h>
#include <spdlog/spdlog.h>

int main() {
    spdlog::info("Welcome to $ProjectName!");
    fmt::print("Modern C++ with vcpkg and CMake\n");
    return 0;
}
"@ | Out-File -Encoding UTF8 src/main.cpp

# 9. Create tests/CMakeLists.txt
@"
add_executable(tests test_main.cpp)
target_link_libraries(tests PRIVATE Catch2::Catch2WithMain)
add_test(NAME tests COMMAND tests)
"@ | Out-File -Encoding UTF8 tests/CMakeLists.txt

# 10. Create tests/test_main.cpp
@"
#include <catch2/catch_test_macros.hpp>

TEST_CASE("Basic test", "[basic]") {
    REQUIRE(1 + 1 == 2);
}
"@ | Out-File -Encoding UTF8 tests/test_main.cpp

# 11. Create .gitignore
@"
# Build directories
build/
cmake-build-*/

# IDE files
.vscode/
.vs/
.idea/
*.user

# Generated files
vcpkg_installed/
CMakeUserPresets.json
compile_commands.json

# OS
.DS_Store
Thumbs.db
"@ | Out-File -Encoding UTF8 .gitignore

Write-Host "Project setup complete!" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. cd $ProjectName"
Write-Host "2. Get CMakePresets.json from modern-cmake skill"
Write-Host "3. cmake --preset windows-debug"
Write-Host "4. cmake --build --preset windows-debug"
```

Run with:
```powershell
.\setup-project.ps1 -ProjectName "MyApp" -VcpkgVersion "2024.11.16"
```

### Automated Project Setup - Linux/macOS (Bash)

Save as `setup-project.sh`:

```bash
#!/bin/bash

PROJECT_NAME="${1:-MyCppProject}"
VCPKG_VERSION="${2:-2024.11.16}"

echo "Setting up $PROJECT_NAME..."

# 1. Create directory structure
mkdir -p src tests external

# 2. Initialize git
git init

# 3. Setup vcpkg submodule
echo "Adding vcpkg as submodule..."
git submodule add https://github.com/microsoft/vcpkg.git external/vcpkg
cd external/vcpkg
git checkout $VCPKG_VERSION
cd ../..
git submodule update --init --recursive

# 4. Bootstrap vcpkg
echo "Bootstrapping vcpkg..."
./external/vcpkg/bootstrap-vcpkg.sh

# 5. Create vcpkg.json
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

# 6. Create root CMakeLists.txt
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
cat > src/CMakeLists.txt << 'EOF'
add_executable(my_app main.cpp)
target_link_libraries(my_app PRIVATE fmt::fmt spdlog::spdlog)
EOF

# 8. Create src/main.cpp
cat > src/main.cpp << 'EOF'
#include <fmt/core.h>
#include <spdlog/spdlog.h>

int main() {
    spdlog::info("Welcome to MyCppProject!");
    fmt::print("Modern C++ with vcpkg and CMake\n");
    return 0;
}
EOF

# 9. Create tests/CMakeLists.txt
cat > tests/CMakeLists.txt << 'EOF'
add_executable(tests test_main.cpp)
target_link_libraries(tests PRIVATE Catch2::Catch2WithMain)
add_test(NAME tests COMMAND tests)
EOF

# 10. Create tests/test_main.cpp
cat > tests/test_main.cpp << 'EOF'
#include <catch2/catch_test_macros.hpp>

TEST_CASE("Basic test", "[basic]") {
    REQUIRE(1 + 1 == 2);
}
EOF

# 11. Create .gitignore
cat > .gitignore << 'EOF'
# Build directories
build/
cmake-build-*/

# IDE files
.vscode/
.vs/
.idea/
*.user

# Generated files
vcpkg_installed/
CMakeUserPresets.json
compile_commands.json

# OS
.DS_Store
Thumbs.db
EOF

echo "Project setup complete!"
echo "Next steps:"
echo "1. Get CMakePresets.json from modern-cmake skill"
echo "2. cmake --preset linux-debug (or osx-debug)"
echo "3. cmake --build --preset linux-debug"
```

Run with:
```bash
chmod +x setup-project.sh
./setup-project.sh "MyApp" "2024.11.16"
```

---

## 7. Troubleshooting Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| vcpkg command not found | Not in PATH | Use full path: `./external/vcpkg/vcpkg` (Linux/macOS) or `.\external\vcpkg\vcpkg.exe` (Windows) |
| Hash mismatch error | Cached binary corrupted | Clear cache: `rm -rf ~/.vcpkg/archives` or `%LOCALAPPDATA%\vcpkg\archives` |
| Port install fails | Network issue or missing port | Check internet connection, update vcpkg: `git -C external/vcpkg pull` |
| Triplet not found | Wrong triplet name | Check available triplets: `vcpkg list --available` |
| CMake can't find packages | Toolchain file not set | Ensure `CMAKE_TOOLCHAIN_FILE` points to `external/vcpkg/scripts/buildsystems/vcpkg.cmake` |
| vcpkg.json not found | Wrong working directory | Run from project root where `vcpkg.json` exists |
| Permission denied | Windows UAC or file lock | Close IDE/build tools, run as Administrator if needed |

---

## 8. Best Practices

1. **Pin vcpkg version**: Always use specific commit/tag in submodule, not `master`
2. **Use manifest mode**: Always create `vcpkg.json` for new projects
3. **Enable binary caching**: Set `VCPKG_BINARY_SOURCES` environment variable
4. **Commit dependency files**: Add `vcpkg.json` and `external/.gitmodules` to git
5. **Ignore generated files**: Add `vcpkg_installed/` to `.gitignore`
6. **Update periodically**: Monthly updates to get latest port versions and bug fixes
7. **Test on all platforms**: vcpkg works best with consistent CMake presets

---

## References

- [vcpkg Official Documentation](https://vcpkg.io/)
- [Manifest Mode Documentation](https://learn.microsoft.com/en-us/vcpkg/users/manifests)
- [Binary Caching Guide](https://learn.microsoft.com/en-us/vcpkg/users/binarycaching)
- [lukka/run-vcpkg GitHub Action](https://github.com/lukka/run-vcpkg)
- [Available Ports](https://vcpkg.io/packages)
