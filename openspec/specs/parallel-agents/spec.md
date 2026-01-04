# Parallel Agents Spec

## Purpose

병렬 에이전트 시스템은 Git worktree를 사용하여 여러 에이전트를 동시에 격리된 환경에서 실행합니다.
독립적인 태스크를 병렬로 처리하여 워크플로우 효율성을 향상시킵니다.
## Requirements
### Requirement: 병렬 실행 환경 격리
각 에이전트는 독립된 Git worktree에서 실행되어야(SHALL) 합니다.

#### Scenario: Worktree 생성
- **WHEN** 병렬 에이전트 실행이 요청됨
- **THEN** 각 에이전트별 독립된 worktree가 생성됨

### Requirement: 충돌 감지
시스템은 병렬 에이전트들이 동일 파일을 수정할 경우 충돌을 감지해야(SHALL) 합니다.

#### Scenario: 파일 충돌 감지
- **WHEN** 두 에이전트가 같은 파일을 수정
- **THEN** 충돌이 보고되고 수동 해결이 요청됨

### Requirement: Git Worktree Isolation
The system SHALL execute parallel agents in isolated environments using git worktree.

#### Scenario: Worktree creation
- **WHEN** 병렬 태스크가 시작될 때
- **THEN** `.worktrees/{change-id}/{agent-name}/` 경로에 worktree가 생성된다
- **AND** `parallel/{change-id}/{agent-name}` 브랜치가 생성된다

#### Scenario: Worktree cleanup on success
- **WHEN** 병렬 태스크가 성공적으로 완료될 때
- **THEN** 결과가 main 브랜치에 머지된다
- **AND** worktree와 브랜치가 삭제된다

#### Scenario: Worktree cleanup on failure
- **WHEN** 병렬 태스크가 실패하거나 타임아웃될 때
- **THEN** worktree와 브랜치가 삭제된다
- **AND** BLOCKED 상태가 보고된다

---

### Requirement: Task Dependency Graph
The system SHALL analyze task dependencies to determine parallel execution eligibility.

#### Scenario: Independent tasks detection
- **WHEN** 두 태스크의 예상 수정 파일이 겹치지 않을 때
- **THEN** 병렬 실행이 가능하다

#### Scenario: Dependent tasks detection
- **WHEN** 태스크 B가 태스크 A의 결과 파일을 수정할 때
- **THEN** A 완료 후 B가 실행된다

#### Scenario: Unknown dependency fallback
- **WHEN** 예상 수정 파일을 판단할 수 없을 때
- **THEN** 순차 실행으로 폴백한다

---

### Requirement: Conflict Resolution
The system SHALL detect and handle conflicts when merging parallel execution results.

#### Scenario: No conflict merge
- **WHEN** 두 worktree에서 수정한 파일이 겹치지 않을 때
- **THEN** 자동으로 main 브랜치에 순차 머지한다

#### Scenario: File conflict detection
- **WHEN** 두 worktree에서 같은 파일을 수정했을 때
- **THEN** 충돌을 감지하고 DECISION_NEEDED 상태를 반환한다
- **AND** 충돌 파일 목록을 사용자에게 표시한다

#### Scenario: Partial success merge
- **WHEN** 일부 에이전트만 성공했을 때
- **THEN** 성공한 에이전트의 결과만 머지한다
- **AND** 실패한 에이전트는 BLOCKED 상태로 보고한다

## Version

- Current: 1.0.0
- Last Updated: 2026-01-04

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     WorkflowOrchestrator                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ Sequential  │  │  Parallel   │  │   State     │         │
│  │   Runner    │  │   Runner    │  │   Manager   │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         │                │                │                  │
│         └────────────────┼────────────────┘                  │
│                          │                                   │
│                 ┌────────┴────────┐                         │
│                 │  WorktreeManager │                         │
│                 └────────┬────────┘                         │
│                          │                                   │
│         ┌────────────────┼────────────────┐                 │
│         ↓                ↓                ↓                 │
│    ┌─────────┐     ┌─────────┐      ┌─────────┐            │
│    │Worktree │     │Worktree │      │Worktree │            │
│    │   #1    │     │   #2    │      │   #3    │            │
│    │(Agent A)│     │(Agent B)│      │(Agent C)│            │
│    └─────────┘     └─────────┘      └─────────┘            │
└─────────────────────────────────────────────────────────────┘
```

---

## Configuration

### workflow.json

```json
"parallel": {
  "enabled": false,
  "max_concurrent_agents": 4,
  "worktree_dir": ".worktrees",
  "branch_prefix": "parallel",
  "auto_merge": true,
  "conflict_resolution": "abort",
  "parallel_capable_agents": [
    "code-writer",
    "code-editor",
    "code-reviewer",
    "cpp-builder"
  ],
  "always_sequential": [
    ["code-writer", "code-reviewer"],
    ["cpp-builder", "tester"]
  ]
}
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| enabled | bool | false | 병렬 실행 활성화 |
| max_concurrent_agents | int | 4 | 최대 동시 에이전트 수 |
| worktree_dir | string | ".worktrees" | Worktree 디렉토리 |
| branch_prefix | string | "parallel" | 브랜치 접두사 |
| auto_merge | bool | true | 자동 머지 활성화 |
| conflict_resolution | string | "abort" | 충돌 해결 정책 |

---

## Branch Strategy

### Naming Convention

```
main
├── feature/{change-id}
│   ├── parallel/{agent-1}
│   ├── parallel/{agent-2}
│   └── parallel/{agent-3}
```

### Example

```
main
├── parallel/establish-orchestration-standards/code-writer
├── parallel/establish-orchestration-standards/code-reviewer
└── parallel/establish-orchestration-standards/cpp-builder
```

### Branch Lifecycle

```bash
# 1. 병렬 실행 시작
git worktree add .worktrees/code-writer -b parallel/code-writer HEAD

# 2. 에이전트 실행
cd .worktrees/code-writer && run_agent()

# 3. 머지
git checkout main
git merge parallel/code-writer --no-ff

# 4. 정리
git worktree remove .worktrees/code-writer
git branch -d parallel/code-writer
```

---

## Directory Structure

```
project-root/
├── .worktrees/              # Worktree 디렉토리 (gitignore)
│   ├── code-writer/         # Agent 1 worktree
│   │   └── (전체 프로젝트)
│   ├── code-reviewer/       # Agent 2 worktree
│   └── cpp-builder/         # Agent 3 worktree
├── src/
└── .git/
```

---

## Dependency Graph

### TaskNode

```python
@dataclass
class TaskNode:
    id: str
    agent: str
    prompt: str
    files: set[str]  # 예상 수정 파일
    depends_on: list[str]
    status: str  # pending, running, completed, failed, skipped
```

### Dependency Detection

```
1. 명시적 의존성 (tasks.md Phase 순서)
2. 파일 기반 의존성 (수정 파일 교집합)
3. 에이전트 기반 의존성
   - code-writer → code-reviewer
   - cpp-builder → tester
```

### Parallel Execution Conditions

병렬 실행 가능 조건:
- 명시적 의존성 없음 AND
- 파일 교집합 없음 AND
- 에이전트 체인 독립

---

## Conflict Resolution

### Conflict Types

| Type | Description | Auto-resolve |
|------|-------------|--------------|
| Content | 같은 파일 같은 줄 수정 | ✗ |
| Add-Add | 같은 경로에 다른 파일 | ✗ |
| Modify-Delete | 한쪽 수정, 한쪽 삭제 | ✗ |
| Non-Overlapping | 같은 파일 다른 줄 | ✓ (Git) |

### Resolution Strategy

```
충돌 발생
    ↓
1. 자동 머지 시도
    ├─ 성공 → 커밋
    └─ 실패 → 충돌 분석
        ↓
2. 충돌 심각도 판단
    ├─ Minor (1-2 파일)
    │   → code-editor 자동 해결
    └─ Major (3+ 파일)
        → DECISION_NEEDED
```

### Conflict Report

```
═══════════════════════════════════════════════════════════════
MERGE CONFLICT DETECTED
═══════════════════════════════════════════════════════════════

충돌 브랜치:
- parallel/code-writer
- parallel/code-reviewer

충돌 파일:
1. src/UserService.cpp (lines 45-50)
   - code-writer: 새 메서드 추가
   - code-reviewer: 기존 메서드 리팩토링

권장 조치:
[1] code-editor 자동 해결
[2] 수동 해결 (git mergetool)
[3] code-writer 변경 우선
[4] code-reviewer 변경 우선
═══════════════════════════════════════════════════════════════
```

---

## Rollback Strategy

```python
def rollback_parallel_execution(worktrees: list[Path]):
    # 1. Worktree 정리
    for wt in worktrees:
        run(f"git worktree remove {wt} --force")

    # 2. 병렬 브랜치 삭제
    for branch in get_parallel_branches():
        run(f"git branch -D {branch}")

    # 3. Feature 브랜치 리셋
    run("git reset --hard ORIG_HEAD")
```

---

## Usage

### CLI

```bash
# 병렬 실행 활성화
python -m orchestrator.main --parallel "병렬 태스크"

# Mock + Parallel
python -m orchestrator.main --mock --parallel "테스트"
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| PARALLEL_AGENTS_MAX | 4 | 최대 병렬 에이전트 수 |

---

## Core Classes

### WorktreeManager

```python
class WorktreeManager:
    def create_worktree(agent, change_id, base_branch) -> WorktreeInfo
    def delete_worktree(agent, force=False) -> bool
    def merge_to_branch(source, target, no_ff=True) -> MergeResult
    def detect_conflicts(branches) -> list[Conflict]
    def cleanup_parallel_branches(change_id) -> int
```

### ParallelRunner

```python
class ParallelRunner:
    async def run_parallel(tasks, change_id, base_branch) -> ParallelExecutionResult
    async def run_dependency_graph(graph, change_id, base_branch) -> ParallelExecutionResult
```

### DependencyGraph

```python
class DependencyGraph:
    def add_task(task: TaskNode)
    def get_ready_tasks() -> list[TaskNode]
    def get_parallel_groups() -> list[list[TaskNode]]
    def detect_file_conflicts(tasks) -> list[tuple]
```

---

## Best Practices

1. **독립적인 태스크 식별**: 파일 교집합이 없는 태스크 선별
2. **적절한 그룹 크기**: 2-4개 에이전트가 최적
3. **충돌 예방**: 태스크 분할 시 파일 경계 고려
4. **정리 습관화**: 작업 완료 후 worktree 정리

---

## Related Specs

- [Orchestration](../orchestration/spec.md)
- [Session Management](../session-management/spec.md)
