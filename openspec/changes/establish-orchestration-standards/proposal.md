# Change: establish-orchestration-standards

## Why

AI 에이전트 팀 기반 오케스트레이션 프레임워크가 **"어떤 미션이 들어와도 일관된 결과물"**을 생산하려면 다음 6가지 핵심 문제를 해결해야 한다:

1. **에이전트 네이밍 불일치**: `cppbuilder` vs `cpp-builder` 혼재로 트리거 매칭 실패 위험
2. **세션 복구 미완성**: blocker 자동 감지 없이 수동 복구만 가능
3. **병렬화 미지원**: 순차 실행만 가능하여 복잡한 태스크에서 비효율
4. **OpenSpec 초기화 담당자 미정의**: 신규 프로젝트에서 누가 openspec 구조를 생성하는지 불명확
5. **프로젝트 폴더 구성 미표준화**: 미션별로 다른 구조 생성 가능성
6. **크로스 플랫폼 빌드 폴더 불일치**: `build/${presetName}/` 규칙이 명시적으로 강제되지 않음

### 현재 구현 상태

| 항목 | 완성도 | 비고 |
|------|--------|------|
| 에이전트 시스템 | 95% | 9개 에이전트, 25개 규칙, 네이밍 불일치 |
| 세션 복구 | 60% | 구조 정의됨, 자동 복구 미완성 |
| 병렬화 | 0% | 순차 실행만 가능 |
| OpenSpec | 템플릿만 | project.md 내용 비어있음 |

---

## What Changes

### 1. 에이전트 워크플로우 일관성 **BREAKING**
- workflow.json의 `cppbuilder` → `cpp-builder`로 통일
- 모든 에이전트 트리거 키워드 표준화
- AVAILABLE_AGENTS 목록과 트리거 맵 동기화

### 2. 프로젝트 폴더 구성 표준화
- `.claude/templates/project-structure.md` 신규 생성
- 신규 프로젝트 스캐폴딩 스킬 추가

### 3. 크로스 플랫폼 빌드 폴더 위치 명시
- `build/${presetName}/` 규칙 CMakePresets.json에서 강제
- 빌드 아티팩트 경로 검증 로직 추가

### 4. OpenSpec 초기화 담당자 지정
- task-manager(달미)가 초기화 담당
- `/openspec:init` 명령어 신규 스킬로 추가

### 5. 세션 복구 방법 완성화
- blocker 자동 감지 로직 session-protocol에 추가
- 복구 시 상태 검증 및 자동 재개 지원

### 6. Git Worktree 병렬 에이전트 시스템 **ARCHITECTURE**
- git worktree 기반 병렬 실행 아키텍처 설계
- 의존성 그래프 기반 병렬화 가능 태스크 식별
- 브랜치 전략 및 머지 정책 정의

---

## Impact

### 영향받는 스펙 (신규)
- `orchestration/spec.md` - 에이전트 네이밍, 상태 프로토콜
- `session-management/spec.md` - 세션 저장/복구, blocker 감지
- `parallel-agents/spec.md` - Git worktree 병렬화
- `project-scaffolding/spec.md` - 폴더 구조, 빌드 규칙

### 영향받는 코드
- `.claude/workflow.json` - 트리거 및 규칙 수정
- `.claude/orchestrator/main.py` - 병렬화 로직 추가
- `.claude/skills/session-protocol/SKILL.md` - blocker 감지 추가
- `.claude/agents/task-manager.md` - OpenSpec 초기화 모드 추가
- `openspec/project.md` - 프로젝트 컨벤션 채우기
