# 변경: Windows 빌드 환경 구축

## 이유

TossPlace POS 프로젝트가 macOS 환경에서 개발되었으며, Windows 개발 환경으로 전환하는 과정에서 다음 문제가 발생했습니다:

1. **구식 CMake 캐시**: 이전 macOS 빌드 캐시 (`/Users/devman/...`) 충돌
2. **Qt 6.5 미설치**: 빌드에 필수인 Qt 6.5+ 라이브러리 부재
3. **vcpkg 미설치**: CMake 의존성 관리 도구 미설치
4. **환경 변수 미설정**: Qt/vcpkg 경로 환경 변수 설정 필요

프로젝트가 이미 **vcpkg manifest mode** (`vcpkg.json`)를 지원하므로, Windows에서도 자동화된 빌드 환경을 구축할 수 있습니다.

## 변경 내용

- ✅ **vcpkg 설치 및 부트스트랩** (C:\vcpkg)
- ✅ **Qt 6.5+ 의존성 설치** (vcpkg 통합)
- ✅ **CMake 빌드 설정** (Windows MSVC 2022 호환)
- ✅ **빌드 검증** (Release 및 Debug 모드)
- ✅ **개발자 가이드 작성** (Windows 빌드 매뉴얼)

## 영향

- **영향받는 스펙**: `toss-pos` (requirements)
- **영향받는 코드**:
  - `CMakeLists.txt` (Windows 경로 정규화)
  - `toss-pos/build/` (캐시 초기화)
  - `.cmake/` 또는 빌드 스크립트 추가 (선택사항)
- **새로운 산출물**:
  - `BUILD_WINDOWS.md` (빌드 가이드)
  - `.cmake/CMakePresets.json` (CMake 프리셋, 선택사항)

## 기술 결정 사항

1. **vcpkg 위치**: `C:\vcpkg` (표준 위치)
2. **빌드 시스템**: MSVC 2022 (Visual Studio 17)
3. **CMake 프리셋**: `-DCMAKE_TOOLCHAIN_FILE` 수동 전달 (추후 자동화 가능)
4. **Qt 버전**: 6.5 이상 (vcpkg 최신 버전 사용)

