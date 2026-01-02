# TossPlace POS - 크로스 플랫폼 빌드 가이드

이 문서는 Windows, macOS에서 TossPlace POS 앱을 빌드하는 방법을 설명합니다.

## 📋 목차

1. [Quick Start](#quick-start)
2. [시스템 요구사항](#시스템-요구사항)
3. [상세 설정 (Windows)](#상세-설정-windows)
4. [상세 설정 (macOS)](#상세-설정-macos)
5. [빌드 명령어](#빌드-명령어)
6. [개발자 가이드](#개발자-가이드)
7. [문제 해결](#문제-해결)

---

## Quick Start

### Windows

```bash
# 1. 개발 환경 설정 (처음 한 번만)
.\build-scripts\setup-dev.bat

# 2. 새 명령 프롬프트 열기 (또는 기존 프롬프트 재시작)

# 3. 프로젝트 디렉토리로 이동
cd toss-pos

# 4. 빌드
cmake --preset windows-x64
cmake --build --preset windows-release

# 5. 실행
.\build\windows-x64\toss-pos.exe
```

### macOS Intel

```bash
# 1. 개발 환경 설정 (처음 한 번만)
./build-scripts/setup-dev.sh

# 2. 셸 설정 재로드
source ~/.bashrc  # 또는 ~/.zshrc

# 3. 프로젝트 디렉토리로 이동
cd toss-pos

# 4. 빌드
cmake --preset macos-x64
cmake --build --preset macos-x64

# 5. 실행
./build/macos-x64/toss-pos
```

### macOS ARM64 (M1/M2/M3)

```bash
# 1-3번은 위와 동일

# 4. 빌드
cmake --preset macos-arm64
cmake --build --preset macos-arm64

# 5. 실행
./build/macos-arm64/toss-pos
```

---

## 시스템 요구사항

### 공통 요구사항

- **CMake**: 4.2.0 이상
- **Git**: 최신 버전
- **C++ 컴파일러**: C++17 지원

### Windows

- **운영체제**: Windows 10 이상
- **컴파일러**: Visual Studio 2022 Community/Professional/Enterprise
  - [다운로드](https://visualstudio.microsoft.com/vs/)
  - 설치 시 "Desktop development with C++" 선택
- **빌드 도구**: MSVC 2022

### macOS

- **운영체제**: macOS 10.15 이상 (Intel), 11.0 이상 (Apple Silicon)
- **컴파일러**: Apple Clang (Xcode Command Line Tools)
  ```bash
  xcode-select --install
  ```
- **패키지 관리자** (권장): Homebrew
  ```bash
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```

---

## 상세 설정 (Windows)

### Step 1: 필수 도구 설치

1. **Visual Studio 2022** 설치
   - [공식 사이트](https://visualstudio.microsoft.com/vs/)에서 다운로드
   - 설치 시 "Desktop development with C++" 워크로드 선택

2. **CMake** 설치
   - [cmake.org](https://cmake.org/download/) 에서 설치
   - 또는 `winget install cmake`

3. **Git** 설치
   - [git-scm.com](https://git-scm.com/download/win)에서 설치
   - 또는 `winget install git`

### Step 2: vcpkg 자동 설정

프로젝트 루트에서:
```bash
.\build-scripts\setup-dev.bat
```

이 스크립트가 자동으로:
- vcpkg를 `C:\vcpkg`에 다운로드 (또는 기존 설치 감지)
- bootstrap-vcpkg.bat 실행
- `VCPKG_ROOT` 환경 변수 설정 (영구)

### Step 3: 새 명령 프롬프트에서 빌드

```bash
cd C:\Dev\ai-supported-desktop-sw\toss-pos

# CMake 설정 (처음 한 번만)
cmake --preset windows-x64

# 빌드
cmake --build --preset windows-release --config Release
```

생성된 실행 파일:
```
build\windows-x64\Release\toss-pos.exe
```

---

## 상세 설정 (macOS)

### Step 1: 필수 도구 설치

```bash
# Xcode Command Line Tools
xcode-select --install

# Homebrew (패키지 관리자)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# CMake
brew install cmake

# Git (이미 설치되어 있음)
```

### Step 2: vcpkg 자동 설정

프로젝트 루트에서:
```bash
./build-scripts/setup-dev.sh
```

이 스크립트가 자동으로:
- vcpkg를 `$HOME/vcpkg`에 다운로드 (또는 기존 설치 감지)
- bootstrap-vcpkg.sh 실행
- `~/.bashrc` 또는 `~/.zshrc`에 `VCPKG_ROOT` 환경 변수 추가

### Step 3: 셸 설정 재로드

```bash
# bash 사용자
source ~/.bashrc

# zsh 사용자 (기본값, macOS Catalina+)
source ~/.zshrc
```

### Step 4: 빌드

#### Intel Mac
```bash
cd toss-pos

# CMake 설정
cmake --preset macos-x64

# 빌드
cmake --build --preset macos-x64

# 실행
./build/macos-x64/toss-pos
```

#### Apple Silicon (M1/M2/M3)
```bash
cd toss-pos

# CMake 설정
cmake --preset macos-arm64

# 빌드
cmake --build --preset macos-arm64

# 실행
./build/macos-arm64/toss-pos
```

---

## 빌드 명령어

### CMake Presets 목록

```bash
# 사용 가능한 모든 preset 확인
cmake --list-presets

# 출력 예시:
# Available configure presets:
#   "windows-x64"
#   "windows-x64-debug"
#   "macos-x64"
#   "macos-x64-debug"
#   "macos-arm64"
#   "macos-arm64-debug"
```

### 빌드 변형

#### Release 빌드 (최적화)
```bash
cmake --preset <preset-name>
cmake --build --preset <preset-name> --config Release
```

#### Debug 빌드 (디버깅 정보 포함)
```bash
cmake --preset <preset-name>-debug
cmake --build --preset <preset-name>-debug --config Debug
```

#### Clean 빌드
```bash
# 해당 preset의 빌드 폴더 완전 삭제
rm -rf build/<preset-name>

# 다시 빌드
cmake --preset <preset-name>
cmake --build --preset <preset-name>
```

---

## 개발자 가이드

### IDE 통합

#### Visual Studio 2022 (Windows)

CMakePresets.json을 자동으로 인식합니다:
1. Visual Studio 2022에서 폴더 열기 (`File > Open Folder`)
2. 프로젝트 폴더 선택
3. CMakePresets.json 자동 감지
4. Build 메뉴에서 preset 선택 및 빌드

#### VS Code (모든 플랫폼)

확장 프로그램 설치:
- CMake Tools
- C/C++ IntelliSense

`.vscode/settings.json` (선택사항):
```json
{
  "cmake.configureOnOpen": true,
  "cmake.sourceDirectory": "${workspaceFolder}/toss-pos",
  "cmake.buildDirectory": "${workspaceFolder}/toss-pos/build-${env:USERNAME}"
}
```

#### Xcode (macOS)

```bash
# CMake로 Xcode 프로젝트 생성
cd toss-pos
cmake -B build-xcode -G Xcode -DCMAKE_TOOLCHAIN_FILE=$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake

# Xcode에서 열기
open build-xcode/toss-pos.xcodeproj
```

### 의존성 관리 (vcpkg)

#### 새로운 라이브러리 추가

1. `toss-pos/vcpkg.json` 편집:
```json
{
  "dependencies": [
    "sqlite3",
    "spdlog",
    "fmt",      // 새로 추가
    "nlohmann-json"
  ]
}
```

2. Clean 빌드:
```bash
rm -rf build/<preset-name>
cmake --preset <preset-name>
cmake --build --preset <preset-name>
```

#### 설치된 패키지 확인

```bash
vcpkg list
```

#### 패키지 검색

```bash
vcpkg search <keyword>
```

---

## 문제 해결

### "cmake not found" 오류

**Windows:**
- CMake를 설치했는지 확인
- 시스템 환경 변수에 CMake 경로 추가
- 명령 프롬프트 재시작

**macOS:**
```bash
brew install cmake
# 또는 환경 변수 확인
echo $PATH
```

### "VCPKG_ROOT" 미설정

**Windows:**
```bash
echo %VCPKG_ROOT%  # 값이 비어있으면 미설정
# 다시 실행
.\build-scripts\setup-dev.bat
```

**macOS:**
```bash
echo $VCPKG_ROOT  # 값이 비어있으면 미설정
# 다시 실행
./build-scripts/setup-dev.sh
source ~/.bashrc  # 또는 ~/.zshrc
```

### "CMAKE_TOOLCHAIN_FILE not found"

```bash
# VCPKG_ROOT 경로 확인
echo $VCPKG_ROOT  # macOS/Linux
echo %VCPKG_ROOT%  # Windows

# 경로가 올바른지 확인
ls $VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake
```

### Qt 빌드 시간 오래 걸림 (30-60분)

**이것은 정상입니다!**
- Qt 6.5를 처음 빌드할 때만 시간이 걸립니다
- 이후 빌드는 캐시로 5-10분 정도 소요됩니다
- 백그라운드에서 실행하고 잠시 기다려주세요

진행 상황을 보려면:
```bash
cmake --build --preset <preset-name> -- --verbose
```

### "Visual Studio Generator not found" (Windows)

Visual Studio 2022가 설치되어 있는지 확인:
```bash
"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
```

설치 경로가 다른 경우 CMakePresets.json을 수정할 수 있습니다.

### 포트 충돌 또는 vcpkg 오류

```bash
# vcpkg 캐시 정리
rm -rf $VCPKG_ROOT/buildtrees
rm -rf $VCPKG_ROOT/downloads

# Clean 빌드 재시작
rm -rf build/<preset-name>
cmake --preset <preset-name>
```

---

## 추가 리소스

- [CMake 공식 문서](https://cmake.org/documentation/)
- [vcpkg 가이드](https://github.com/Microsoft/vcpkg)
- [Qt 6 공식 문서](https://doc.qt.io/)
- [개발자 온보딩 가이드](DEVELOPMENT.md)

---

**질문이나 문제가 있으신가요?**

이 문서에 오류나 누락이 있으면 리포트해주세요!
