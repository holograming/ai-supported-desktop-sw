# Session Management Spec

## Purpose

세션 관리 시스템은 작업 상태를 저장하고 복원하여 세션 간 연속성을 보장합니다.
블로커 추적, 자동 감지, 복구 기능을 제공합니다.
## Requirements
### Requirement: 세션 상태 저장
시스템은 현재 작업 상태를 파일로 저장할 수 있어야(SHALL) 합니다.

#### Scenario: 세션 저장
- **WHEN** `/session:save` 명령 실행
- **THEN** 현재 상태가 session-state.json에 저장됨

### Requirement: 세션 복원
시스템은 이전 세션 상태를 복원할 수 있어야(SHALL) 합니다.

#### Scenario: 세션 로드
- **WHEN** `/session:load` 명령 실행
- **THEN** 저장된 상태가 복원되고 작업 재개 가능

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

## Version

- Current: 1.0.0
- Last Updated: 2026-01-04

---

## Session State File

### Location

```
.claude/session-state.json
```

**주의**: 이 파일은 커밋하지 않음 (로컬 작업 상태)

### Schema

```json
{
  "mode": "quick|sync|full",
  "saved_at": "ISO 8601 timestamp",
  "git_branch": "feature/user-auth",
  "git_commit": "abc1234",
  "git_pushed": true,
  "openspec": "change-id",
  "openspec_status": "IN_PROGRESS",
  "working_on": "현재 작업 설명",
  "next_steps": ["다음 작업 1", "다음 작업 2"],
  "blocker": null | { blocker object },
  "completed_tasks": ["완료된 태스크"],
  "pending_tasks": ["대기 중인 태스크"],
  "task_progress": {
    "completed": 5,
    "total": 12,
    "percentage": 42
  }
}
```

---

## Save Modes

| Mode | Duration | Use Case |
|------|----------|----------|
| **quick** | ~15초 | 체크포인트, WIP |
| **sync** | ~30초 | 일과 종료, 서브태스크 완료 |
| **full** | ~3-5분 | 태스크 완료, 마일스톤 |

---

## Commands

### /session:save

```bash
/session:save          # Quick (기본)
/session:save --sync   # Sync (GitHub push 포함)
/session:save --full   # Full (전체 검증 + push)
```

#### Quick Mode

1. 수정된 파일 `git add`
2. WIP 커밋 생성
3. `session-state.json` 저장
4. 푸시 안 함

#### Sync Mode

1. Quick 동작 + `git push`
2. `git_pushed = true`

#### Full Mode

1. Sync 동작 + 검증
2. CHANGELOG.md, ROADMAP.md 확인
3. CI/CD 결과 확인 (선택)

### /session:load

```bash
/session:load          # 세션 복원
/session:load --resume # 자동 재개 모드
```

#### --resume 옵션

1. 세션 로드
2. 블로커 확인 → 자동 복구 시도
3. 마지막 작업 지점에서 자동 재개
4. 사용자 확인 없이 진행

---

## Blocker System

### Blocker Types

| Type | Description | Auto-detect | Recovery Agent |
|------|-------------|-------------|----------------|
| `build_error` | 빌드 실패 | ✓ | cpp-builder |
| `test_failure` | 테스트 실패 | ✓ | tester → code-editor |
| `dependency` | 의존성 문제 | ✓ | cpp-builder (vcpkg) |
| `design_issue` | 설계 문제 | ✗ | architect |
| `review_blocked` | 코드 리뷰 이슈 | ✓ | code-editor |
| `ci_failure` | CI/CD 실패 | ✓ | devops |
| `merge_conflict` | Git 충돌 | ✓ | 수동 해결 |
| `other` | 기타 | ✗ | 수동 해결 |

### Blocker Schema

```json
{
  "blocker": {
    "type": "build_error",
    "severity": "critical|high|medium|low",
    "description": "CMake 설정 오류로 빌드 실패",
    "error_pattern": "Could NOT find Qt6",
    "resolution": "vcpkg.json 의존성 확인 필요",
    "appeared_after": "Qt6 버전 업그레이드 후",
    "detected_at": "2026-01-04T10:30:00Z",
    "auto_detected": true,
    "recovery_agent": "cpp-builder",
    "recovery_attempted": 0,
    "max_recovery_attempts": 3
  }
}
```

### Auto-Detection Patterns

#### Build Errors

```bash
grep -E "(error:|error C[0-9]+|fatal error|LNK[0-9]+)" build_output.log
```

- `error:` → GCC/Clang
- `error C[0-9]+` → MSVC
- `LNK[0-9]+` → Linker
- `Could NOT find` → CMake

#### Test Failures

```bash
ctest --output-on-failure 2>&1 | grep -E "(FAILED|Error)"
```

#### CI Failures

```bash
gh run list --limit 1 --json status,conclusion
```

---

## State Validation

### validate_session_state()

세션 로드 시 검증:

```python
def validate_session_state(state):
    checks = {
        "git_sync": verify_git_state(state.git_branch, state.git_commit),
        "openspec_exists": verify_openspec(state.openspec),
        "files_intact": verify_modified_files(state),
        "blocker_resolved": check_blocker_status(state.blocker)
    }
    return SessionValidation(checks)
```

### Validation Results

| Status | Action |
|--------|--------|
| ALL_VALID | 정상 복원 |
| BRANCH_MISMATCH | 브랜치 전환 질문 |
| COMMIT_MISMATCH | 동기화 경고 |
| UNCOMMITTED_CHANGES | 커밋/스태시 질문 |
| OPENSPEC_NOT_FOUND | 새 태스크 제안 |
| BLOCKER_EXISTS | 블로커 해결 우선 |

### verify_session_integrity()

```python
def verify_session_integrity(state):
    # 1. 필수 필드 확인
    # 2. 타임스탬프 유효성
    # 3. 진행률 일관성
    # 4. 블로커 스키마 검증
    return IntegrityOK() | IntegrityError()
```

---

## Recovery Workflow

```
세션 로드
    ↓
상태 검증
    ↓
    ├─ 블로커 존재?
    │   ├─ auto_detected = true → 자동 복구 시도
    │   │   ├─ build_error → cpp-builder 호출
    │   │   ├─ test_failure → tester 호출
    │   │   └─ 복구 성공? → 블로커 해제
    │   │
    │   └─ auto_detected = false → 해결 방법 제안
    │
    └─ 블로커 없음 → 마지막 작업에서 계속
```

---

## Best Practices

1. **저장 습관화**: 중요 변경 후 `/session:save`
2. **일과 종료 전**: `/session:save --sync` 필수
3. **블로커 기록**: 막히면 즉시 기록
4. **진행률 추적**: completed_tasks, pending_tasks 업데이트
5. **복구 우선순위**: 블로커 해결 → Git 동기화 → 작업 재개

---

## Related Specs

- [Orchestration](../orchestration/spec.md)
- [Parallel Agents](../parallel-agents/spec.md)
