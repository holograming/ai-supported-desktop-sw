# Capability: session-management

세션 저장 및 복구 메커니즘을 정의한다.

---

## ADDED Requirements

### Requirement: Session State File
The system SHALL store session state in `.claude/session-state.json`.

#### Scenario: Session save
- **WHEN** `/session:save` 명령이 실행될 때
- **THEN** 현재 작업 상태가 JSON 파일로 저장된다
- **AND** 다음 필드가 포함된다:
  - mode, saved_at, git_branch, git_commit
  - openspec, openspec_status, working_on
  - next_steps, blocker, completed_tasks, pending_tasks

#### Scenario: Session restore prompt
- **WHEN** 새 세션이 시작될 때
- **AND** session-state.json이 존재할 때
- **THEN** 복원 옵션을 사용자에게 제시한다

---

### Requirement: Blocker Detection
The system SHALL automatically detect blockers when saving session state.

#### Scenario: Build error blocker
- **WHEN** 마지막 cpp-builder 실행이 FAILED 상태일 때
- **THEN** blocker.type = "build_error"로 기록한다
- **AND** blocker.message에 오류 요약을 포함한다

#### Scenario: Test failure blocker
- **WHEN** 마지막 tester 실행이 FAILED 상태일 때
- **THEN** blocker.type = "test_failure"로 기록한다

#### Scenario: Decision needed blocker
- **WHEN** 에이전트가 DECISION_NEEDED 상태를 반환할 때
- **THEN** blocker.type = "decision_required"로 기록한다

---

### Requirement: Session Continuity
The system SHALL accurately restore previous state when recovering a session.

#### Scenario: OpenSpec continuation
- **WHEN** 이전 세션에서 OpenSpec 변경이 진행 중이었을 때
- **THEN** 복구 시 해당 OpenSpec의 tasks.md를 로드한다
- **AND** 마지막 완료된 태스크 다음부터 재개한다

#### Scenario: Blocker resolution
- **WHEN** 세션 복구 시 blocker가 존재할 때
- **THEN** blocker 정보를 사용자에게 표시한다
- **AND** 해결 방법을 제안한다
