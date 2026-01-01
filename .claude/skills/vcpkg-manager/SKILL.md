---
name: vcpkg
description: vcpkg manifest 모드를 사용한 C++ 의존성 관리. C++ 프로젝트에 vcpkg 설정, vcpkg.json으로 의존성 관리, CMake preset 통합, 바이너리 캐싱 설정, vcpkg 문제 해결 시 사용. Windows, Linux, macOS 지원.
---

# vcpkg 스킬

vcpkg manifest 모드와 CMake preset 통합을 사용한 C++ 의존성 관리.

## 빠른 시작

### 1. 프로젝트에 vcpkg 초기화

`assets/` 폴더의 템플릿을 프로젝트 루트에 복사:
- `vcpkg.json` - 의존성 manifest
- `vcpkg-configuration.json` - registry/baseline 설정
- `CMakePresets.json` - vcpkg 통합 CMake preset (기존 파일에 병합 가능)

### 2. Baseline 업데이트

최신 baseline 커밋 해시 가져오기:
```bash
git ls-remote https://github.com/microsoft/vcpkg.git HEAD
```

`vcpkg.json`과 `vcpkg-configuration.json` 두 파일의 `builtin-baseline` 값을 업데이트.

### 3. 의존성 추가

`vcpkg.json` 편집:
```json
{
  "dependencies": [
    "fmt",
    "spdlog",
    { "name": "qt6-base", "version>=": "6.6.0" },
    { "name": "gtest", "host": true }
  ]
}
```

### 4. 빌드

```bash
export VCPKG_ROOT=/path/to/vcpkg
cmake --preset linux-x64
cmake --build --preset linux-x64
```

## Manifest 모드 핵심

### vcpkg.json 구조

```json
{
  "name": "프로젝트명",
  "version": "1.0.0",
  "dependencies": [...],
  "overrides": [
    { "name": "openssl", "version": "3.1.0" }
  ],
  "features": {
    "tests": {
      "description": "테스트 빌드",
      "dependencies": ["gtest"]
    }
  },
  "builtin-baseline": "<커밋해시>"
}
```

### 의존성 지정 방식

| 문법 | 예시 | 설명 |
|------|------|------|
| 단순 | `"fmt"` | baseline 기준 최신 버전 |
| 버전 지정 | `{"name": "fmt", "version>=": "10.0.0"}` | 최소 버전 |
| 기능 선택 | `{"name": "curl", "features": ["ssl"]}` | 특정 기능 포함 |
| 플랫폼 한정 | `{"name": "pthread", "platform": "linux"}` | 특정 플랫폼만 |
| 호스트 전용 | `{"name": "protobuf", "host": true}` | 빌드 도구만 |

### 플랫폼 표현식

```json
{
  "name": "winapi",
  "platform": "windows"
},
{
  "name": "pthread", 
  "platform": "linux | osx"
},
{
  "name": "vulkan",
  "platform": "!uwp & !arm"
}
```

## CMake 통합

### 필수 환경변수

```bash
export VCPKG_ROOT=/path/to/vcpkg
```

### CMake 변수 (preset 또는 CMakeLists.txt)

```cmake
CMAKE_TOOLCHAIN_FILE = $ENV{VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake
VCPKG_MANIFEST_MODE = ON
VCPKG_TARGET_TRIPLET = x64-linux  # 또는 x64-windows, arm64-osx 등
```

### 패키지 사용법

```cmake
find_package(fmt CONFIG REQUIRED)
find_package(spdlog CONFIG REQUIRED)

target_link_libraries(myapp PRIVATE fmt::fmt spdlog::spdlog)
```

## 주요 Triplet

| 플랫폼 | Triplet | 링크 방식 |
|--------|---------|-----------|
| Linux x64 | `x64-linux` | 동적 |
| macOS Intel | `x64-osx` | 동적 |
| macOS ARM | `arm64-osx` | 동적 |
| Windows x64 | `x64-windows` | 동적 |
| Windows x64 | `x64-windows-static` | 정적 |
| Windows x64 | `x64-windows-static-md` | 정적 라이브러리, 동적 CRT |

## 바이너리 캐싱

재컴파일 방지를 위한 캐싱 설정. 상세 설정은 `references/binary-caching.md` 참고.

### 빠른 설정

```bash
# 로컬 캐시 (기본값, 자동)
# ~/.cache/vcpkg/archives (Linux/macOS)
# %LOCALAPPDATA%\vcpkg\archives (Windows)

# GitHub Actions
export VCPKG_BINARY_SOURCES="clear;x-gha,readwrite"

# 커스텀 파일시스템 캐시
export VCPKG_BINARY_SOURCES="clear;files,/shared/vcpkg-cache,readwrite"
```

## 문제 해결

### 흔한 문제

**패키지 설치 후 찾을 수 없음:**
```cmake
# CONFIG 모드 확인
find_package(PackageName CONFIG REQUIRED)
```

**버전 충돌:**
```json
// vcpkg.json에서 overrides 사용
"overrides": [
  { "name": "package", "version": "x.y.z" }
]
```

**클린 빌드 강제:**
```bash
rm -rf build/
rm -rf vcpkg_installed/
cmake --preset <preset>
```

### 유용한 명령어

```bash
# 설치된 패키지 목록
vcpkg list

# 패키지 검색
vcpkg search <키워드>

# 패키지 정보 확인
vcpkg info <패키지>

# 업데이트 확인
vcpkg update

# manifest 검증
vcpkg format-manifest vcpkg.json
```
