# Orchestration Spec

## Overview

워크플로우 오케스트레이터는 AI 에이전트들의 실행을 자동으로 조율하는 Python 기반 시스템입니다.
`workflow.json`에 정의된 규칙에 따라 에이전트 간 전환을 관리합니다.

## Version

- Current: 1.1.0
- Last Updated: 2026-01-04

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   WorkflowOrchestrator                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ RuleEngine  │  │StatusParser │  │   Runner    │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         └────────────────┼────────────────┘                 │
│                          │                                   │
│                 ┌────────┴────────┐                         │
│                 │  WorkflowState  │                         │
│                 └─────────────────┘                         │
└─────────────────────────────────────────────────────────────┘
```

### Core Modules

| Module | Path | Description |
|--------|------|-------------|
| main.py | `.claude/orchestrator/main.py` | Entry point, CLI |
| engine.py | `.claude/orchestrator/engine.py` | Rule matching logic |
| protocol.py | `.claude/orchestrator/protocol.py` | Agent output parsing |
| runner.py | `.claude/orchestrator/runner.py` | Agent execution (sequential) |
| parallel_runner.py | `.claude/orchestrator/parallel_runner.py` | Agent execution (parallel) |
| worktree_manager.py | `.claude/orchestrator/worktree_manager.py` | Git worktree management |
| state.py | `.claude/orchestrator/state.py` | Workflow state tracking |
| ui.py | `.claude/orchestrator/ui.py` | Terminal UI |

---

## Configuration

### workflow.json Structure

```json
{
  "workflow": {
    "name": "openspec-qt-workflow",
    "version": "1.1",
    "triggers": { ... },
    "protocol": { ... },
    "rules": [ ... ],
    "auto_actions": { ... },
    "limits": { ... },
    "parallel": { ... }
  }
}
```

### Triggers

에이전트별 트리거 키워드 정의:

```json
"triggers": {
  "task-manager": ["새 태스크", "status", "달미"],
  "architect": ["설계", "design", "도산"],
  "cpp-builder": ["빌드", "build", "로컬빌더"],
  ...
}
```

### Rules

워크플로우 전환 규칙:

```json
{
  "id": "task_to_architect",
  "trigger": {
    "agent": "task-manager",
    "status": "READY"
  },
  "action": {
    "agent": "architect",
    "prompt": "OpenSpec 기반 설계. Context: {context}"
  }
}
```

---

## Agent Protocol

### Status Block

모든 에이전트는 응답 끝에 상태 블록을 포함해야 합니다:

```
===============================================================
[WORKFLOW_STATUS]
status: READY|BLOCKED|FAILED|DECISION_NEEDED
context: 작업 결과 설명
next_hint: 다음 에이전트 힌트
===============================================================
```

### Valid Statuses

| Status | Description | Next Action |
|--------|-------------|-------------|
| READY | 작업 완료, 다음 진행 가능 | 규칙에 따라 다음 에이전트 |
| BLOCKED | 일시적 문제 발생 | 재시도 또는 수정 |
| FAILED | 심각한 오류 | 워크플로우 중단 |
| DECISION_NEEDED | 사용자 결정 필요 | 사용자 입력 대기 |

---

## Available Agents

| Agent | Alias | Role |
|-------|-------|------|
| task-manager | 달미 | 태스크 생성/관리 |
| architect | 도산 | 설계/분석 |
| designer | 사하 | UI/UX 디자인 |
| code-writer | 용산 | 새 코드 작성 |
| code-editor | 철산 | 기존 코드 수정 |
| code-reviewer | 영실 | 코드 리뷰 |
| cpp-builder | 로컬빌더 | C++ 빌드 |
| tester | 지평 | 테스트 실행 |
| devops | 인재 | CI/CD 관리 |

---

## Usage

### CLI

```bash
# 기본 실행
python -m orchestrator.main "새 태스크 - 사용자 서비스"

# Mock 모드
python -m orchestrator.main --mock "테스트"

# 병렬 실행
python -m orchestrator.main --parallel "병렬 테스트"

# Verbose
python -m orchestrator.main -v --mock "상세 테스트"
```

### Options

| Flag | Description |
|------|-------------|
| `--mock` | Mock 모드 (SDK 없이 테스트) |
| `--parallel`, `-p` | 병렬 에이전트 실행 활성화 |
| `--verbose`, `-v` | 상세 출력 |
| `--config PATH` | 커스텀 workflow.json 경로 |
| `--project-dir PATH` | 프로젝트 디렉토리 |

---

## Workflow Flow

```
사용자 입력
    ↓
task-manager (태스크 생성)
    ↓
architect (설계)
    ↓
[UI 필요?] → designer
    ↓
code-writer / code-editor (구현)
    ↓
code-reviewer (리뷰)
    ↓ [BLOCKED → code-editor 루프]
cpp-builder (빌드)
    ↓ [BLOCKED → code-editor 루프]
tester (테스트)
    ↓ [BLOCKED → code-editor 루프]
task-manager (종료)
```

---

## Limits

```json
"limits": {
  "max_workflow_iterations": 20,
  "max_retries_per_rule": 3,
  "agent_timeout_seconds": 300
}
```

---

## Related Specs

- [Session Management](../session-management/spec.md)
- [Parallel Agents](../parallel-agents/spec.md)
