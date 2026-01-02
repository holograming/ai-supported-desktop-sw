# toss-pos Specification

## Purpose
TBD - created by archiving change fix-toss-pos-styling. Update Purpose after archive.
## Requirements
### Requirement: 한글 폰트 지원
앱은 한글 텍스트를 정상적으로 렌더링해야 한다(SHALL).

#### Scenario: macOS에서 한글 표시
- Given: 앱이 macOS에서 실행될 때
- When: 카테고리명, 상품명, 버튼 텍스트 등 한글이 표시될 때
- Then: "Apple SD Gothic Neo" 또는 시스템 기본 한글 폰트로 렌더링된다
- And: 글자 깨짐 없이 정상 표시된다

#### Scenario: Windows에서 한글 표시
- Given: 앱이 Windows에서 실행될 때
- When: 한글 텍스트가 표시될 때
- Then: "Malgun Gothic" 또는 "Noto Sans KR"로 렌더링된다

### Requirement: 토스 디자인 시스템 색상 적용
앱 전체에 토스 디자인 시스템 색상이 일관되게 적용되어야 한다(MUST).

#### Scenario: 배경색 적용
- Given: 앱이 실행될 때
- When: 메인 화면이 표시될 때
- Then: 배경색이 #F2F4F6 (TossTheme.background)로 표시된다

#### Scenario: 카드 컴포넌트 스타일
- Given: 상품 그리드 또는 주문 패널이 표시될 때
- When: 카드 컴포넌트가 렌더링될 때
- Then: 배경색은 #FFFFFF (TossTheme.surface)
- And: 그림자 효과가 적용된다 (DropShadow)
- And: 모서리가 둥글다 (radius: 16px)

#### Scenario: 버튼 색상
- Given: Primary 버튼이 표시될 때
- Then: 배경색은 #3182F6 (TossTheme.primaryBlue)
- And: 텍스트 색상은 #FFFFFF

### Requirement: 카테고리 및 상품 데이터 표시
샘플 데이터가 정상적으로 로드되어 표시되어야 한다(SHALL).

#### Scenario: 카테고리 바 표시
- Given: 주문 페이지가 표시될 때
- When: 카테고리 바가 렌더링될 때
- Then: "전체", "커피", "음료", "디저트", "베이커리" 탭이 표시된다
- And: 기본 선택은 "전체"

#### Scenario: 상품 그리드 표시
- Given: "전체" 카테고리가 선택된 상태에서
- When: 상품 그리드가 렌더링될 때
- Then: 모든 카테고리의 상품이 표시된다
- And: 각 상품에 이름과 가격이 표시된다
- And: 가격은 "원" 단위로 포맷된다 (예: "4,500원")

### Requirement: 카드 그림자 효과
TossCard 컴포넌트에 그림자 효과가 적용되어야 한다(SHALL).

#### Scenario: 그림자 렌더링
- Given: TossCard 컴포넌트가 사용될 때
- When: 카드가 렌더링될 때
- Then: 하단과 우측에 부드러운 그림자가 표시된다
- And: 그림자 색상은 반투명 검정 (약 10% 불투명도)
- And: 그림자 blur 반경은 8-12px

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

