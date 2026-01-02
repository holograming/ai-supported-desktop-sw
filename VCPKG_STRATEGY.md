# Windows/macOS 크로스 플랫폼 vcpkg 관리 전략

## 현황 분석

### 프로젝트 특성
```
✅ vcpkg.json           존재함 (manifest mode 준비됨)
✅ CMake 4.2.0+        설치됨 (CMakePresets 지원)
❌ CMakePresets.json   미설정
❌ VCPKG_ROOT 환경변수 미설정
❌ vcpkg 설치          미실행
```

### 문제점
1. **일관성 부족**: Windows/macOS에서 서로 다른 경로/설정
2. **신규 개발자 온보딩**: 매번 수동 설정 필요
3. **CI/CD 미자동화**: 환경 변수 의존성 높음
4. **빌드 재현성**: 버전 관리 불명확

---

## 3가지 접근 방식 비교

### 1️⃣ **CMakePresets.json + 환경변수 (권장)**

#### 구조
```
프로젝트/
├── CMakePresets.json          ← 추가 (CMake 설정 중앙화)
├── vcpkg.json                 ← 기존 (의존성 명세)
├── vcpkg-configuration.json   ← 추가 (registry baseline)
├── build-scripts/
│   ├── setup-vcpkg-mac.sh     ← 신규
│   └── setup-vcpkg-win.bat    ← 신규
└── ...
```

#### 동작 방식
```bash
# 1회: 환경 변수 설정 (각 개발자)
export VCPKG_ROOT=/path/to/vcpkg

# 매번: CMake 자동 감지
cmake --preset default              # CMakePresets.json이 vcpkg 자동 구성
cmake --build --preset default
```

#### 장점 ✅
- **프로젝트 크기**: vcpkg 미포함 (0 추가)
- **초기 설정**: 스크립트로 자동화 가능
- **버전 관리**: baseline hash로 명시적 관리
- **IDE 지원**: Visual Studio, VS Code 직접 지원
- **최신성**: 항상 최신 vcpkg 사용 가능
- **공식 권장**: Microsoft 공식 가이드

#### 단점 ❌
- 각 개발자가 VCPKG_ROOT 환경변수 설정 필요
- CI/CD에서 별도 설정 필요

#### 설정 예시
```json
// CMakePresets.json
{
  "version": 3,
  "configurePresets": [
    {
      "name": "default",
      "hidden": true,
      "cacheVariables": {
        "CMAKE_TOOLCHAIN_FILE": "$env{VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake"
      }
    },
    {
      "name": "windows-x64",
      "inherits": "default",
      "cacheVariables": {
        "VCPKG_TARGET_TRIPLET": "x64-windows"
      }
    },
    {
      "name": "macos-x64",
      "inherits": "default",
      "cacheVariables": {
        "VCPKG_TARGET_TRIPLET": "x64-osx"
      }
    },
    {
      "name": "macos-arm64",
      "inherits": "default",
      "cacheVariables": {
        "VCPKG_TARGET_TRIPLET": "arm64-osx"
      }
    }
  ],
  "buildPresets": [
    {
      "name": "windows-release",
      "configurePreset": "windows-x64",
      "configuration": "Release"
    }
  ]
}
```

---

### 2️⃣ **프로젝트 내 vcpkg 포함 (자동화 극대화)**

#### 구조
```
프로젝트/
├── vcpkg/                      ← 서브모듈 또는 tar.gz
│   ├── CMakeLists.txt
│   ├── bootstrap-vcpkg.bat
│   └── ...
├── CMakePresets.json           ← 로컬 vcpkg 경로 지정
├── vcpkg.json
└── build-scripts/
    ├── setup-dev.sh            ← 이것만 실행하면 됨
    └── setup-dev.bat
```

#### 동작 방식
```bash
# Windows
.\build-scripts\setup-dev.bat

# macOS/Linux
./build-scripts/setup-dev.sh

# 이후: 환경변수 설정 없이 빌드
cmake --preset default
```

#### 장점 ✅
- **최고의 자동화**: 한 줄 명령으로 완전 자동 설정
- **일관성 보장**: 모든 개발자가 동일한 vcpkg 버전 사용
- **오프라인 지원**: 초기 설정 후 의존성 캐싱 가능
- **신규 개발자**: 최소 교육 비용

#### 단점 ❌
- **저장소 크기**: +300-500MB (submodule) 또는 +1-2GB (전체 tar.gz)
- **초기 복제**: 5-10분 추가 시간
- **관리 복잡성**: vcpkg 업데이트 시 별도 작업
- **CI/CD**: 저장소 용량 제약 (GitHub Actions 스토리지)

#### 구현 옵션
```bash
# A. Git Submodule (추천, 경량)
git submodule add https://github.com/Microsoft/vcpkg.git vcpkg
git submodule update --init --recursive

# B. 타르볼 다운로드 (자동화)
# build-scripts/setup-dev.sh가 자동으로 다운로드

# C. vcpkg 초기화 스크립트 (하이브리드)
# setup-dev.sh가 $HOME/vcpkg 체크 후 필요시만 다운로드
```

---

### 3️⃣ **하이브리드: 환경변수 + 자동 다운로드**

#### 구조 (최적의 균형)
```
프로젝트/
├── CMakePresets.json
├── vcpkg.json
├── vcpkg-configuration.json
├── cmake/
│   └── FindOrDownloadVcpkg.cmake  ← 신규
└── build-scripts/
    ├── setup-dev.sh               ← 신규 (자동 다운로드)
    └── setup-dev.bat
```

#### 동작 방식
```bash
# 1회: 자동 다운로드 + 환경 변수 설정
source build-scripts/setup-dev.sh
# VCPKG_ROOT=/Users/dev/vcpkg (또는 C:\vcpkg)로 자동 설정

# 이후: 일반적인 CMake 빌드
cmake --preset default
```

#### 장점 ✅
- **적당한 자동화**: 초기 설정 스크립트만 실행하면 됨
- **유연성**: VCPKG_ROOT 이미 설정되어 있으면 사용
- **저장소 경량**: 프로젝트에 포함 안 함 (0 추가)
- **버전 관리**: vcpkg.json baseline으로 명시적 관리
- **IDE 지원**: 여전히 CMakePresets.json으로 자동 감지

#### 단점 ❌
- 초기 다운로드 필요 (처음만)
- 약간의 셸 스크립팅 필요

#### 구현 예시
```bash
# setup-dev.sh
#!/bin/bash

VCPKG_ROOT="${VCPKG_ROOT:-$HOME/vcpkg}"

if [ ! -d "$VCPKG_ROOT" ]; then
    echo "📦 vcpkg 설치 중..."
    git clone https://github.com/Microsoft/vcpkg.git "$VCPKG_ROOT"
    cd "$VCPKG_ROOT"
    ./bootstrap-vcpkg.sh
    cd -
fi

export VCPKG_ROOT
echo "✅ VCPKG_ROOT=$VCPKG_ROOT"
echo "💡 export VCPKG_ROOT='$VCPKG_ROOT'" >> ~/.bashrc
echo "다음 명령으로 빌드:"
echo "  cmake --preset default"
```

---

## 권장 전략: 3번 + CMakePresets.json

### 선택 이유
```
최적 지표:
  • 저장소 크기        : ⭐⭐⭐⭐⭐ (0 추가)
  • 자동화 수준        : ⭐⭐⭐⭐☆ (스크립트로 충분)
  • 일관성             : ⭐⭐⭐⭐⭐ (baseline으로 명시적)
  • 신규 개발자 경험   : ⭐⭐⭐⭐⭐ (한 줄 스크립트)
  • 크로스 플랫폼 지원 : ⭐⭐⭐⭐⭐ (CMakePresets.json 자동)
```

### 최종 구성 파일

#### 1. CMakePresets.json (추가)
```json
{
  "version": 3,
  "configurePresets": [
    {
      "name": "default",
      "hidden": true,
      "binaryDir": "${sourceDir}/build-${presetName}",
      "cacheVariables": {
        "CMAKE_TOOLCHAIN_FILE": "$env{VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake",
        "VCPKG_MANIFEST_MODE": "ON",
        "CMAKE_CXX_STANDARD": "17"
      }
    },
    {
      "name": "windows-x64",
      "displayName": "Windows x64",
      "description": "MSVC 2022 + vcpkg (x64)",
      "inherits": "default",
      "generator": "Visual Studio 17 2022",
      "cacheVariables": {
        "VCPKG_TARGET_TRIPLET": "x64-windows"
      }
    },
    {
      "name": "macos-x64",
      "displayName": "macOS Intel",
      "description": "Apple Clang + vcpkg (x64)",
      "inherits": "default",
      "generator": "Unix Makefiles",
      "cacheVariables": {
        "VCPKG_TARGET_TRIPLET": "x64-osx"
      }
    },
    {
      "name": "macos-arm64",
      "displayName": "macOS ARM64",
      "description": "Apple Clang + vcpkg (ARM64)",
      "inherits": "default",
      "generator": "Unix Makefiles",
      "cacheVariables": {
        "VCPKG_TARGET_TRIPLET": "arm64-osx"
      }
    }
  ],
  "buildPresets": [
    {
      "name": "windows-release",
      "configurePreset": "windows-x64",
      "configuration": "Release",
      "jobs": 4
    },
    {
      "name": "macos-release",
      "configurePreset": "macos-x64",
      "configuration": "Release"
    }
  ]
}
```

#### 2. vcpkg-configuration.json (추가)
```json
{
  "default-registry": {
    "kind": "builtin",
    "baseline": "해시값 (git ls-remote로 최신값 확인)",
    "packages": ["*"]
  }
}
```

#### 3. build-scripts/setup-dev.sh (추가)
```bash
#!/bin/bash
set -e

# macOS 또는 Linux
VCPKG_ROOT="${VCPKG_ROOT:-$HOME/vcpkg}"

if [ ! -d "$VCPKG_ROOT" ]; then
    echo "📦 vcpkg를 $VCPKG_ROOT에 설치 중..."
    git clone https://github.com/Microsoft/vcpkg.git "$VCPKG_ROOT"
fi

echo "🔧 vcpkg 초기화 중..."
cd "$VCPKG_ROOT"
if [ ! -f "vcpkg" ]; then
    ./bootstrap-vcpkg.sh
fi
cd -

# 환경 변수 설정
export VCPKG_ROOT

echo ""
echo "✅ 설정 완료!"
echo "📍 VCPKG_ROOT=$VCPKG_ROOT"
echo ""
echo "🚀 빌드 시작:"
echo "  cmake --preset default"
echo "  cmake --build --preset default --config Release"
echo ""
echo "💡 다음번부터 VCPKG_ROOT 자동 설정하려면:"
echo "  echo 'export VCPKG_ROOT=$VCPKG_ROOT' >> ~/.bashrc"
echo "  source ~/.bashrc"
```

#### 4. build-scripts/setup-dev.bat (추가)
```batch
@echo off
setlocal enabledelayedexpansion

REM Windows
if not defined VCPKG_ROOT (
    set "VCPKG_ROOT=C:\vcpkg"
)

if not exist "%VCPKG_ROOT%" (
    echo 📦 vcpkg를 %VCPKG_ROOT%에 설치 중...
    git clone https://github.com/Microsoft/vcpkg.git "%VCPKG_ROOT%"
)

echo 🔧 vcpkg 초기화 중...
cd /d "%VCPKG_ROOT%"
if not exist "vcpkg.exe" (
    call bootstrap-vcpkg.bat
)
cd /d %~dp0..

REM 환경 변수 설정
setx VCPKG_ROOT "%VCPKG_ROOT%"
set "VCPKG_ROOT=%VCPKG_ROOT%"

echo.
echo ✅ 설정 완료!
echo 📍 VCPKG_ROOT=%VCPKG_ROOT%
echo.
echo 🚀 빌드 시작:
echo   cmake --preset windows-x64
echo   cmake --build --preset windows-release
echo.
echo 💡 새 터미널에서는 환경 변수가 자동 설정됩니다 (setx 사용)
```

---

## 구현 계획

### Phase 1: 기본 설정
- [ ] CMakePresets.json 작성
- [ ] vcpkg-configuration.json 작성 (baseline 버전 지정)
- [ ] build-scripts/setup-dev.sh, setup-dev.bat 작성

### Phase 2: 빌드 검증
- [ ] Windows: setup-dev.bat → cmake --preset windows-x64
- [ ] macOS: setup-dev.sh → cmake --preset macos-x64 (또는 arm64)
- [ ] 성공 여부 확인

### Phase 3: 문서화
- [ ] BUILD.md (크로스 플랫폼 빌드 가이드)
- [ ] DEVELOPMENT.md (개발자 온보딩)

---

## 참고자료

- [vcpkg manifest mode - Microsoft Learn](https://learn.microsoft.com/en-us/vcpkg/concepts/manifest-mode)
- [CMakePresets with vcpkg - Microsoft Learn](https://learn.microsoft.com/en-us/cpp/build/cmake-presets-vs)
- [vcpkg cmake integration](https://learn.microsoft.com/en-us/vcpkg/users/buildsystems/cmake-integration)

