# Design: Git Worktree Parallel Agent System

## Context

### Background
현재 오케스트레이터는 `while True` 루프로 순차 실행만 지원한다.
복잡한 태스크에서 독립적인 서브태스크들을 병렬로 실행하면 효율성이 크게 향상된다.

### Current Architecture
```python
# orchestrator/main.py
while True:
    output = await self.runner.run(current_agent, full_prompt)  # 순차 실행
    status = self.parser.parse(output)
    match = self.engine.match(current_agent, status)
```

### Constraints
- 기존 순차 실행 모드는 유지해야 함 (backward compatible)
- Git 워크플로우와 충돌 없이 동작해야 함
- Mock 모드에서도 병렬 실행 시뮬레이션 가능해야 함

### Stakeholders
- 에이전트 팀 (격리된 실행 환경 필요)
- 로컬빌더 (빌드 충돌 방지 필요)
- 세션 매니저 (병렬 상태 추적 필요)

---

## Goals / Non-Goals

### Goals
- 독립적인 태스크의 병렬 실행
- Git worktree를 통한 코드 격리
- 자동 충돌 감지 및 머지
- 기존 순차 실행 모드 유지

### Non-Goals
- 분산 시스템 (단일 머신에서만 실행)
- 실시간 에이전트 간 통신
- 복잡한 의존성 그래프 (1단계 의존성만)

---

## Decisions

### Decision 1: Worktree per Agent
각 병렬 에이전트는 별도의 git worktree에서 실행된다.

**Alternatives considered:**
| 방법 | 장점 | 단점 |
|------|------|------|
| 같은 디렉토리 + git stash | 단순함 | 충돌 위험, 복잡한 롤백 |
| Docker 컨테이너 | 완전 격리 | 오버헤드 과다, 설정 복잡 |
| **Git worktree** | 가벼움, 브랜치 격리 | Git 명령어 의존 |

**Rationale:** Git worktree는 가볍고, 브랜치 격리가 자연스럽고, 머지가 쉽다.

### Decision 2: Task Dependency via File Analysis
파일 수정 범위를 분석하여 의존성을 판단한다.

**방법:**
1. 태스크 시작 전 예상 수정 파일 목록 수집
2. 파일 집합이 겹치지 않으면 병렬 실행 가능
3. 겹치면 순차 실행으로 폴백

### Decision 3: Branch Naming Convention
`parallel/{change-id}/{agent-name}` 형식의 브랜치 이름을 사용한다.

**예시:**
```
main
├── parallel/establish-orchestration-standards/code-writer
├── parallel/establish-orchestration-standards/code-reviewer
└── parallel/establish-orchestration-standards/cpp-builder
```

---

## Architecture

### Component Diagram

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

### New Module: WorktreeManager

```python
class WorktreeManager:
    """Git worktree 관리"""

    def create_worktree(self, branch_name: str) -> Path:
        """새 worktree 생성"""
        pass

    def delete_worktree(self, worktree_path: Path) -> None:
        """worktree 삭제"""
        pass

    def merge_to_main(self, branch_name: str) -> MergeResult:
        """main 브랜치로 머지"""
        pass

    def detect_conflicts(self, branches: list[str]) -> list[Conflict]:
        """충돌 감지"""
        pass
```

### New Module: ParallelRunner

```python
class ParallelRunner:
    """병렬 에이전트 실행"""

    async def run_parallel(
        self,
        tasks: list[AgentTask],
        worktree_manager: WorktreeManager
    ) -> list[AgentResult]:
        """병렬 실행"""
        # 1. 각 태스크에 대해 worktree 생성
        # 2. asyncio.gather로 병렬 실행
        # 3. 결과 수집 및 충돌 검사
        # 4. 자동 머지 또는 충돌 보고
        pass
```

### Data Flow

```
1. 태스크 목록 수신
      ↓
2. 의존성 분석 (파일 기반)
      ↓
3. 독립 태스크 그룹 식별
      ↓
4. 그룹별 worktree 생성 + 브랜치 생성
      ↓
5. 병렬 에이전트 실행 (asyncio.gather)
      ↓
6. 결과 수집 + 충돌 검사
      ↓
7. 자동 머지 또는 충돌 보고
      ↓
8. worktree 정리
```

---

## Risks / Trade-offs

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| 머지 충돌 | Medium | High | 충돌 감지 후 순차 재실행 |
| 디스크 공간 부족 | Low | Medium | worktree 크기 제한, 자동 정리 |
| Git 상태 불일치 | Low | High | worktree 상태 검증, 복구 로직 |
| 에이전트 타임아웃 | Medium | Medium | 타임아웃 시 worktree 자동 정리 |

---

## Migration Plan

### Phase 1: 기반 작업 (1주)
- WorktreeManager 클래스 구현
- 단일 worktree 생성/삭제 테스트

### Phase 2: 병렬 러너 구현 (2주)
- ParallelRunner 클래스 구현
- Mock 모드 테스트

### Phase 3: 통합 (1주)
- main.py에 --parallel 옵션 추가
- workflow.json에 parallel_mode 옵션 추가

### Rollback
- `--parallel` 플래그 제거로 즉시 순차 모드로 복귀 가능
- 기존 코드는 수정 없이 유지

---

## Dependency Graph Model (6.1.2)

### Task Dependency Graph

```python
@dataclass
class TaskNode:
    """태스크 노드"""
    id: str
    agent: str
    files: set[str]  # 예상 수정 파일
    depends_on: list[str] = field(default_factory=list)
    status: str = "pending"  # pending, running, completed, failed

class DependencyGraph:
    """의존성 그래프"""

    def __init__(self):
        self.nodes: dict[str, TaskNode] = {}
        self.edges: dict[str, list[str]] = {}  # child -> parents

    def add_task(self, task: TaskNode) -> None:
        self.nodes[task.id] = task
        self.edges[task.id] = task.depends_on

    def get_parallel_groups(self) -> list[list[TaskNode]]:
        """병렬 실행 가능한 그룹 반환"""
        # 토폴로지 정렬 후 같은 레벨의 태스크 그룹화
        pass

    def detect_file_conflicts(self, tasks: list[TaskNode]) -> list[tuple]:
        """파일 충돌 감지"""
        conflicts = []
        for i, t1 in enumerate(tasks):
            for t2 in tasks[i+1:]:
                overlap = t1.files & t2.files
                if overlap:
                    conflicts.append((t1.id, t2.id, overlap))
        return conflicts
```

### Dependency Detection Strategy

```
태스크 분석
    ↓
1. 명시적 의존성 (tasks.md 순서)
    - Phase 순서 기반
    - "의존성: Phase X 완료 필요" 파싱

2. 파일 기반 의존성
    - 예상 수정 파일 교집합 확인
    - 교집합 존재 → 순차 실행

3. 에이전트 기반 의존성
    - code-writer → code-reviewer (항상)
    - cpp-builder → tester (항상)

병렬 실행 가능 조건:
    - 명시적 의존성 없음 AND
    - 파일 교집합 없음 AND
    - 에이전트 체인 독립
```

---

## Branch Strategy (6.1.3)

### Branch Naming Convention

```
main                                    # 프로덕션 브랜치
├── feature/{change-id}                 # OpenSpec 변경 브랜치
│   ├── parallel/{agent-1}              # 병렬 에이전트 브랜치
│   ├── parallel/{agent-2}
│   └── parallel/{agent-3}
```

### Branch Lifecycle

```
1. 병렬 실행 시작
   git checkout -b feature/{change-id} main
   git worktree add .worktrees/{agent-1} -b parallel/{agent-1}
   git worktree add .worktrees/{agent-2} -b parallel/{agent-2}

2. 에이전트 실행
   # 각 worktree에서 독립 실행
   cd .worktrees/{agent-1} && run_agent()

3. 머지
   git checkout feature/{change-id}
   git merge parallel/{agent-1} --no-ff
   git merge parallel/{agent-2} --no-ff

4. 정리
   git worktree remove .worktrees/{agent-1}
   git worktree remove .worktrees/{agent-2}
   git branch -d parallel/{agent-1}
   git branch -d parallel/{agent-2}
```

### Worktree Directory Structure

```
project-root/
├── .worktrees/                     # 병렬 worktree 디렉토리 (gitignore)
│   ├── code-writer/                # Agent 1 worktree
│   │   └── (전체 프로젝트 복사본)
│   ├── code-reviewer/              # Agent 2 worktree
│   └── cpp-builder/                # Agent 3 worktree
├── src/
├── ...
└── .git/
```

---

## Conflict Resolution Policy (6.1.4)

### Conflict Types

| 유형 | 설명 | 자동 해결 | 해결 방법 |
|------|------|----------|----------|
| **Content Conflict** | 같은 파일 같은 줄 수정 | ✗ | 수동 해결 |
| **Add-Add Conflict** | 같은 경로에 다른 파일 추가 | ✗ | 수동 해결 |
| **Modify-Delete** | 한쪽 수정, 한쪽 삭제 | ✗ | 수동 해결 |
| **Non-Overlapping** | 같은 파일 다른 줄 | ✓ | Git 자동 머지 |

### Resolution Strategy

```
충돌 발생
    ↓
1. 자동 머지 시도 (git merge --no-commit)
    ├─ 성공 → 커밋 진행
    │
    └─ 실패 → 충돌 분석
        ↓
2. 충돌 파일 목록 수집
    ↓
3. 충돌 심각도 판단
    ├─ Minor (1-2개 파일, 간단한 변경)
    │   → code-editor 자동 해결 시도
    │
    └─ Major (3개+ 파일, 복잡한 변경)
        → DECISION_NEEDED 상태로 에스컬레이션
        → 사용자에게 해결 방법 제안
```

### Conflict Report Format

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
[1] code-editor가 자동 해결 시도
[2] 수동 해결 (git mergetool)
[3] code-writer 변경 우선
[4] code-reviewer 변경 우선

═══════════════════════════════════════════════════════════════
```

### Rollback Strategy

```python
def rollback_parallel_execution(worktrees: list[Path]):
    """병렬 실행 롤백"""
    for wt in worktrees:
        # 1. worktree 정리
        run(f"git worktree remove {wt} --force")

    # 2. 병렬 브랜치 삭제
    for branch in get_parallel_branches():
        run(f"git branch -D {branch}")

    # 3. feature 브랜치를 마지막 성공 커밋으로 리셋
    run("git checkout feature/{change-id}")
    run("git reset --hard ORIG_HEAD")
```

---

## Open Questions (Resolved)

1. **worktree 최대 개수 제한은?**
   - **결정**: CPU 코어 수와 동일하게 제한 (기본값: 4)
   - 환경 변수로 오버라이드 가능: `PARALLEL_AGENTS_MAX`

2. **에이전트 타임아웃 시 worktree 정리 방법은?**
   - **결정**: 타임아웃 발생 시 해당 worktree만 삭제
   - 다른 에이전트는 계속 실행
   - 정리 실패 시 로그 기록 후 다음 실행 시 재정리

3. **부분 성공 시 머지 정책은?**
   - **결정**: 성공한 에이전트의 결과만 머지
   - 실패한 에이전트는 BLOCKED 상태로 보고
   - 실패 브랜치는 보존 (디버깅용)
