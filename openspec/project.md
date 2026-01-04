# Project Context

## Purpose

AI 에이전트 팀이 스펙 기반으로 협업하는 **오케스트레이션 프레임워크**.

- 어떤 미션이 들어와도 일관된 결과물을 생산
- 9개 전문 에이전트가 역할 분담하여 협업
- OpenSpec 기반 명세 주도 개발 (Spec-Driven Development)

## Tech Stack

### Core
- **C++17/20**: 애플리케이션 백엔드
- **Qt6/QML**: 데스크톱 UI 프레임워크
- **CMake 3.21+**: 빌드 시스템 (Ninja generator)
- **vcpkg**: C++ 패키지 관리자 (Git 서브모듈)

### Orchestrator
- **Python 3.10+**: 오케스트레이터 엔진
- **asyncio**: 비동기 에이전트 실행
- **Claude Code SDK**: AI 에이전트 연동

### CI/CD
- **GitHub Actions**: 크로스 플랫폼 빌드 (Windows/Linux/macOS)

## Project Conventions

### Code Style

#### C++
- **네이밍**: PascalCase (클래스), camelCase (메서드/변수), UPPER_SNAKE_CASE (상수)
- **파일 네이밍**: PascalCase.cpp, PascalCase.h
- **들여쓰기**: 4 spaces
- **참조**: `.claude/skills/cpp-qml-rule/SKILL.md`

#### QML
- **컴포넌트**: PascalCase.qml
- **속성**: camelCase
- **참조**: `.claude/skills/qml-desktop-ui/SKILL.md`

#### Python (Orchestrator)
- **네이밍**: snake_case (함수/변수), PascalCase (클래스)
- **파일 네이밍**: snake_case.py
- **타입 힌트**: 필수

### Architecture Patterns

#### Agent-Based Orchestration
```
Orchestrator (main.py)
    ↓
WorkflowEngine (engine.py) ← workflow.json 규칙
    ↓
AgentRunner (runner.py)
    ↓
Agents (.claude/agents/*.md)
```

#### State Machine Workflow
- 상태: READY, BLOCKED, FAILED, DECISION_NEEDED
- 전이: workflow.json의 규칙에 따라 다음 에이전트 결정

### Testing Strategy
- **단위 테스트**: Catch2 (C++), pytest (Python)
- **통합 테스트**: Mock 모드로 에이전트 시뮬레이션
- **빌드 검증**: 6개 프리셋 빌드 성공 확인

### Git Workflow
- **메인 브랜치**: main
- **기능 브랜치**: feature/{feature-name}
- **커밋 메시지**: Conventional Commits (feat:, fix:, docs:, refactor:)
- **PR 필수**: 코드 리뷰 후 머지

## Domain Context

### Agent Team (드라마 "스타트업" 기반)
| 별칭 | 역할 | subagent_type |
|------|------|---------------|
| 달미 | 태스크 매니저 | task-manager |
| 도산 | 아키텍트 | architect |
| 용산 | 코드 작성자 | code-writer |
| 철산 | 코드 수정자 | code-editor |
| 영실 | 코드 리뷰어 | code-reviewer |
| 사하 | UI/UX 디자이너 | designer |
| 로컬빌더 | C++ 빌드 전문가 | cpp-builder |
| 지평 | 테스터 | tester |
| 인재 | DevOps | devops |

### Agent Naming Convention
- **subagent_type**: kebab-case 필수 (예: `cpp-builder`, `code-writer`)
- **별칭**: 한글 이름으로 workflow.json triggers에 등록
- **파일 위치**: `.claude/agents/{subagent_type}.md`
- **동기화 필수**:
  1. `AVAILABLE_AGENTS` 목록 (main.py)
  2. `workflow.json` triggers
  3. Agent Team 테이블 (project.md)

### OpenSpec Workflow
1. **Proposal 단계**: 변경 제안 작성 (proposal.md, tasks.md, design.md)
2. **Apply 단계**: 승인 후 구현 (tasks.md 순서대로)
3. **Archive 단계**: 배포 후 specs/ 업데이트

## Important Constraints

### Technical
- **크로스 플랫폼**: Windows, Linux, macOS 모두 지원 필수
- **Qt6 필수**: Qt5 미지원
- **vcpkg 서브모듈**: external/vcpkg/ 경로 고정

### Orchestration
- **순차 실행**: 현재 병렬화 미지원 (Phase 6에서 구현 예정)
- **에이전트 네이밍**: kebab-case 필수 (예: `cpp-builder`, `code-writer`)
- **상태 프로토콜**: [WORKFLOW_STATUS] 블록 필수
- **OpenSpec 초기화**: task-manager(달미)가 담당

### Build Convention
- **빌드 폴더**: `build/${presetName}/` (예: `build/windows-debug/`)
- **CMakePresets.json**: binaryDir 규칙 준수 필수
- **아티팩트 경로**: `build/${presetName}/bin/` (실행 파일)

### Project Folder Structure
```
project-root/
├── .claude/                 # AI 에이전트 설정
│   ├── agents/              # 에이전트 정의
│   ├── skills/              # 스킬 정의
│   ├── workflow.json        # 워크플로우 규칙
│   └── session-state.json   # 세션 상태
├── external/
│   └── vcpkg/               # vcpkg 서브모듈 (고정 경로)
├── openspec/                # OpenSpec 명세
│   ├── project.md           # 프로젝트 컨벤션
│   ├── specs/               # 현재 스펙
│   └── changes/             # 변경 제안
├── src/                     # C++ 소스
├── qml/                     # QML 파일
├── tests/                   # 테스트
├── build/                   # 빌드 출력 (gitignore)
│   └── ${presetName}/       # 프리셋별 빌드
├── CMakeLists.txt
├── CMakePresets.json
└── vcpkg.json               # vcpkg 의존성
```

## External Dependencies

### Build Tools
- CMake 3.21+
- Ninja (권장)
- MSVC (Windows), GCC/Clang (Linux/macOS)

### vcpkg Packages (vcpkg.json 참조)
- Qt6 (Core, Quick, Widgets)
- fmt, spdlog (로깅)
- Catch2 (테스트)

### Services
- GitHub Actions (CI/CD)
- Claude Code SDK (AI 에이전트)
