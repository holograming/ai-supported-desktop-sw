# toss-pos Windows 빌드 환경 구축 - Spec Delta

## ADDED Requirements

### Requirement: Windows 빌드 지원
앱은 Windows 10 이상에서 CMake + vcpkg + MSVC 2022를 사용하여 빌드 가능해야 한다(SHALL).

#### Scenario: vcpkg를 통한 Qt 6.5 설치
- **WHEN** Windows 개발자가 `C:\vcpkg`에 vcpkg를 설치하고 manifest mode로 의존성을 설치할 때
- **THEN** Qt 6.5 이상, sqlite3, spdlog이 자동으로 다운로드되고 빌드된다
- **AND** CMake 설정에서 `/DCMAKE_TOOLCHAIN_FILE`를 vcpkg 경로로 지정하면 모든 의존성이 자동 연결된다

#### Scenario: CMake 프로젝트 설정 (Windows)
- **WHEN** `CMakeLists.txt`를 CMake 4.2.0 이상으로 실행할 때 (Windows MSVC 2022 환경)
- **THEN** Qt6 패키지가 vcpkg에서 제공되는 경로로 자동 발견된다
- **AND** MSVC 컴파일러로 C++17 표준 준수하여 빌드된다

#### Scenario: UTF-8 인코딩 (Windows)
- **WHEN** CMakeLists.txt가 MSVC 컴파일러로 빌드될 때
- **THEN** 컴파일 옵션 `/utf-8`이 자동 적용된다 (기존: MSVC 조건부 설정)
- **AND** 한글 문자열이 소스 코드에서 올바르게 처리된다

#### Scenario: 실행 파일 생성 (Windows)
- **WHEN** Release/Debug 모드로 빌드가 완료될 때
- **THEN** `build\Release\toss-pos.exe` 또는 `build\Debug\toss-pos.exe` 실행 파일이 생성된다
- **AND** 앱이 Windows 시스템에서 자동으로 실행 가능한 상태가 된다

### Requirement: 크로스 플랫폼 빌드 호환성
Windows 빌드 환경 설정이 기존 macOS 빌드를 방해하지 않아야 한다(SHALL).

#### Scenario: 캐시 초기화
- **WHEN** 이전 macOS 빌드의 CMake 캐시가 남아있을 때
- **THEN** `build/` 디렉토리를 완전히 삭제 후 재생성한다
- **AND** 새로운 Windows 경로 기반의 캐시가 생성된다

#### Scenario: 경로 표준화
- **WHEN** CMakeLists.txt에서 파일 경로가 지정될 때
- **THEN** 상대 경로 또는 CMake 변수 (`${CMAKE_CURRENT_SOURCE_DIR}` 등)를 사용한다
- **AND** 절대 경로는 플랫폼별로 자동 변환된다 (Windows: `\` / Unix: `/`)

## MODIFIED Requirements

### Requirement: UTF-8 인코딩 지원
소스 코드 내 한글 문자열이 올바르게 컴파일되어야 한다(MUST).

#### Scenario: 한글 문자열 컴파일 (Windows)
- Given: C++ 소스 코드에 한글 문자열이 포함되고, Windows MSVC 컴파일러로 빌드될 때
- When: 프로젝트가 CMake로 설정될 때
- Then: MSVC의 경우 `/utf-8` 컴파일 옵션이 자동 적용된다 (CMakeLists.txt:11-13)
- And: 한글이 UTF-8로 올바르게 인코딩되고 런타임에 깨지지 않는다

#### Scenario: 한글 문자열 컴파일 (macOS/Linux)
- Given: Unix 계열 시스템에서 GCC/Clang 컴파일러로 빌드될 때
- When: 프로젝트가 CMake로 설정될 때
- Then: MSVC 조건이 무시되고 시스템 기본 인코딩 설정이 유지된다
- And: 한글이 여전히 올바르게 처리된다

