# Capability: project-scaffolding

프로젝트 폴더 구조 및 빌드 규칙을 정의한다.

---

## ADDED Requirements

### Requirement: Standard Project Structure
The system SHALL enforce standard folder structure for all C++/QML projects.

#### Scenario: New project creation
- **WHEN** 새 프로젝트가 생성될 때
- **THEN** 다음 폴더 구조가 자동 생성된다:
  ```
  project-root/
  ├── external/vcpkg/        # Git 서브모듈
  ├── src/                   # 소스 코드
  ├── tests/                 # 테스트 코드
  ├── qml/                   # QML UI 파일 (UI 앱인 경우)
  ├── images/                # 리소스 (UI 앱인 경우)
  ├── CMakeLists.txt
  ├── CMakePresets.json
  ├── vcpkg.json
  └── .gitignore
  ```

#### Scenario: Structure validation
- **WHEN** 프로젝트 구조를 검증할 때
- **THEN** 필수 파일(CMakeLists.txt, CMakePresets.json, vcpkg.json)의 존재를 확인한다
- **AND** 누락된 파일이 있으면 경고를 표시한다

---

### Requirement: Build Directory Convention
The system SHALL use `build/${presetName}/` path for build output.

#### Scenario: CMake preset build
- **WHEN** CMake 프리셋으로 빌드할 때
- **THEN** 출력은 `build/{preset-name}/`에 생성된다
- **AND** 실행 파일은 `build/{preset-name}/bin/`에 위치한다

#### Scenario: Platform preset mapping
- **WHEN** 빌드 명령이 실행될 때
- **THEN** 플랫폼에 따라 적절한 프리셋이 선택된다:
  - Windows: windows-debug, windows-release
  - Linux: linux-debug, linux-release
  - macOS: osx-debug, osx-release

#### Scenario: Build directory gitignore
- **WHEN** 프로젝트가 초기화될 때
- **THEN** `build/` 패턴이 .gitignore에 포함된다

---

### Requirement: OpenSpec Initialization
The system SHALL delegate OpenSpec structure initialization to task-manager (달미).

#### Scenario: First-time setup
- **WHEN** openspec/ 폴더가 없을 때
- **AND** 사용자가 OpenSpec 기반 작업을 요청할 때
- **THEN** task-manager가 기본 구조를 생성한다:
  ```
  openspec/
  ├── project.md
  ├── AGENTS.md
  ├── specs/
  └── changes/
      └── archive/
  ```

#### Scenario: Existing structure detection
- **WHEN** openspec/ 폴더가 이미 존재할 때
- **THEN** 초기화를 건너뛰고 기존 구조를 사용한다

#### Scenario: Partial structure repair
- **WHEN** openspec/ 폴더는 있지만 필수 파일이 누락됐을 때
- **THEN** 누락된 파일만 생성한다
