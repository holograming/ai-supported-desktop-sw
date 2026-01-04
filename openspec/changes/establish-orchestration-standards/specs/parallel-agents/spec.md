# Capability: parallel-agents

Git worktree 기반 병렬 에이전트 시스템을 정의한다.

**참조**: design.md에서 상세 아키텍처 확인

---

## ADDED Requirements

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
