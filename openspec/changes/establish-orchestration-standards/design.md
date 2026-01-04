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

## Open Questions

1. **worktree 최대 개수 제한은?**
   - 제안: CPU 코어 수와 동일하게 제한

2. **에이전트 타임아웃 시 worktree 정리 방법은?**
   - 제안: 타임아웃 발생 시 해당 worktree만 삭제, 다른 에이전트는 계속 실행

3. **부분 성공 시 머지 정책은?**
   - 제안: 성공한 에이전트의 결과만 머지, 실패한 에이전트는 BLOCKED 상태로 보고
