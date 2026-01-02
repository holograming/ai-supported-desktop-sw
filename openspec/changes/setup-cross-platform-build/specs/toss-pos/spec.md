# toss-pos 크로스 플랫폼 빌드 - Spec Delta

## ADDED Requirements

### Requirement: Windows 빌드 지원 (MSVC 2022)
TossPlace POS 앱은 Windows 10 이상에서 Visual Studio 2022 (MSVC) + CMake + vcpkg를 사용하여 빌드 가능해야 한다(SHALL).

#### Scenario: Windows CMake 설정
- **WHEN** 개발자가 Windows에서 `cmake --preset windows-x64` 명령을 실행할 때
- **THEN** CMakePresets.json이 자동으로 다음을 설정한다:
  - `CMAKE_TOOLCHAIN_FILE`: `$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake`
  - `VCPKG_TARGET_TRIPLET`: `x64-windows`
  - `CMAKE_GENERATOR`: `Visual Studio 17 2022`
- **AND** vcpkg manifest mode가 자동으로 활성화되어 의존성 설치

#### Scenario: Windows 앱 빌드 및 실행
- **WHEN** `cmake --build --preset windows-release` 명령으로 Release 모드 빌드 완료 시
- **THEN** `build-windows-x64/Release/toss-pos.exe` 실행 파일이 생성된다
- **AND** Windows에서 직접 실행 가능한 상태 (DLL 경로 자동 구성)

---

### Requirement: macOS Intel 빌드 지원 (x64)
TossPlace POS 앱은 macOS 10.15 이상의 Intel 기반 Mac에서 빌드 가능해야 한다(SHALL).

#### Scenario: macOS Intel CMake 설정
- **WHEN** 개발자가 Intel Mac에서 `cmake --preset macos-x64` 명령을 실행할 때
- **THEN** CMakePresets.json이 자동으로 다음을 설정한다:
  - `VCPKG_TARGET_TRIPLET`: `x64-osx`
  - `CMAKE_GENERATOR`: `Unix Makefiles` (또는 Ninja)
  - Apple Clang 컴파일러 자동 감지
- **AND** vcpkg가 macOS x64 호환 의존성 다운로드 및 빌드

#### Scenario: macOS Intel 앱 빌드 및 실행
- **WHEN** `cmake --build --preset macos-x64` 명령으로 빌드 완료 시
- **THEN** `build-macos-x64/toss-pos` 실행 파일이 생성된다
- **AND** macOS에서 직접 실행 가능 (`./build-macos-x64/toss-pos`)

---

### Requirement: macOS ARM64 빌드 지원 (M1/M2/M3)
TossPlace POS 앱은 macOS 11 이상의 Apple Silicon 기반 Mac (M1/M2/M3)에서 네이티브 빌드 가능해야 한다(SHALL).

#### Scenario: macOS ARM64 CMake 설정
- **WHEN** 개발자가 Apple Silicon Mac에서 `cmake --preset macos-arm64` 명령을 실행할 때
- **THEN** CMakePresets.json이 자동으로 다음을 설정한다:
  - `VCPKG_TARGET_TRIPLET`: `arm64-osx`
  - Apple Clang 컴파일러 (ARM64 지원)
  - Qt 6.5+ ARM64 바이너리 다운로드

#### Scenario: macOS ARM64 앱 빌드 및 실행
- **WHEN** `cmake --build --preset macos-arm64` 명령으로 빌드 완료 시
- **THEN** `build-macos-arm64/toss-pos` (ARM64 네이티브 바이너리) 생성
- **AND** M1/M2/M3 Mac에서 최적 성능으로 실행 가능

---

### Requirement: CMakePresets.json 기반 빌드 설정
CMake 빌드 구성이 CMakePresets.json 파일에 중앙화되어야 한다(MUST).

#### Scenario: 플랫폼별 preset 선택
- **WHEN** 개발자가 `cmake --preset <name>` 명령 실행 시
- **THEN** 선택 가능한 preset:
  - `default` (숨겨진 기본 설정)
  - `windows-x64`
  - `macos-x64`
  - `macos-arm64`
- **AND** 선택된 preset의 모든 CMake 캐시 변수가 자동 적용

---

### Requirement: vcpkg Manifest Mode 및 버전 관리
프로젝트의 의존성이 manifest mode로 관리되며, 모든 개발자가 동일한 버전을 사용해야 한다(MUST).

#### Scenario: vcpkg.json 의존성 선언
- **GIVEN** 프로젝트 루트의 `vcpkg.json`에 의존성이 선언된 상태
- **WHEN** CMake 빌드 실행 시
- **THEN** vcpkg가 자동으로:
  - 의존성 목록 읽기 (sqlite3, spdlog, Qt6)
  - 필요한 패키지 다운로드 및 빌드
  - `vcpkg_installed/` 폴더에 설치
- **AND** 모든 개발자가 동일한 의존성 버전 사용

#### Scenario: baseline 버전 고정
- **GIVEN** `vcpkg-configuration.json`에 builtin-baseline 지정됨
- **WHEN** 개발자가 vcpkg 명령 실행 시
- **THEN** 지정된 baseline 커밋의 포트 버전이 사용됨
- **AND** 개발자 간 의존성 버전 불일치 방지

---

### Requirement: 자동화된 개발 환경 설정
신규 개발자가 최소한의 수동 작업으로 빌드 환경을 구축 가능해야 한다(SHALL).

#### Scenario: Windows 환경 자동 설정
- **WHEN** 개발자가 `.\build-scripts\setup-dev.bat` 실행 시
- **THEN** 다음 작업이 자동으로 수행됨:
  - vcpkg이 `C:\vcpkg`에 존재하는지 확인
  - 없으면 GitHub에서 클론
  - `bootstrap-vcpkg.bat` 실행
  - `VCPKG_ROOT` 환경 변수 설정 (setx로 영구 설정)
- **AND** 다음 터미널부터 환경 변수 자동 적용

#### Scenario: macOS/Linux 환경 자동 설정
- **WHEN** 개발자가 `./build-scripts/setup-dev.sh` 실행 시
- **THEN** 다음 작업이 자동으로 수행됨:
  - vcpkg이 `$HOME/vcpkg`에 존재하는지 확인
  - 없으면 GitHub에서 클론
  - `bootstrap-vcpkg.sh` 실행
  - `VCPKG_ROOT` 환경 변수 설정 (셸 시작 파일에 추가)
- **AND** 셸 재시작 후 환경 변수 자동 적용

---

### Requirement: 크로스 플랫폼 호환성 유지
새로운 빌드 설정이 기존 macOS 빌드와 충돌하지 않아야 한다(SHALL).

#### Scenario: 이전 빌드 캐시 초기화
- **WHEN** 이전 macOS (또는 다른 플랫폼) 빌드의 CMake 캐시가 존재할 때
- **THEN** `build-windows-x64/`, `build-macos-x64/` 등 **플랫폼별 디렉토리**로 분리
- **AND** 기존 `/build/` 캐시와 충돌 없음

#### Scenario: 상대 경로 표준화
- **WHEN** CMakeLists.txt에서 파일 경로 참조 시
- **THEN** 상대 경로 또는 CMake 변수만 사용 (절대 경로 제외)
- **AND** Windows와 Unix 모두에서 자동 변환됨

---

## MODIFIED Requirements

### Requirement: UTF-8 인코딩 지원
소스 코드 내 한글 문자열이 올바르게 컴파일되어야 한다(MUST).

**변경 사항**: Windows MSVC에서의 명시적 지원 추가

#### Scenario: 한글 문자열 컴파일 (Windows MSVC)
- Given: C++ 소스 코드에 한글 문자열이 포함되고, Windows에서 MSVC 2022로 빌드될 때
- When: CMakeLists.txt가 MSVC 환경 감지하여 `/utf-8` 컴파일 옵션 적용 시
- Then: 한글이 UTF-8로 올바르게 인코딩되고 런타임에 깨지지 않음
- And: Windows와 macOS에서 동일하게 한글 렌더링됨

#### Scenario: 한글 문자열 컴파일 (macOS/Linux)
- Given: Unix 계열 시스템에서 GCC/Clang 컴파일러로 빌드될 때
- When: CMakeLists.txt가 플랫폼 감지하여 Unix 기본 인코딩 설정 유지 시
- Then: 한글이 여전히 올바르게 처리됨
- And: MSVC 옵션은 무시되고 시스템 기본값 사용

