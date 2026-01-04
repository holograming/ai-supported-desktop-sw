---
name: session-protocol
description: "세션 관리 프로토콜. 세션 상태 저장/복원 방법."
---

# Session Protocol

## 1. 세션 상태 위치

```
.claude/session-state.json
```

**주의**: 이 파일은 커밋하지 않음 (로컬 작업 상태)

---

## 2. session-state.json 형식

```json
{
  "mode": "quick|sync|full",
  "saved_at": "2025-01-15T14:30:00",
  "git_branch": "feature/user-auth",
  "git_commit": "abc1234",
  "git_pushed": true,
  "openspec": "00027",
  "openspec_status": "IN_PROGRESS",
  "working_on": "사용자 인증 기능 구현 중",
  "next_steps": [
    "UserService 테스트 작성",
    "로그인 UI 구현"
  ],
  "blocker": null,
  "completed_tasks": [
    "UserModel 클래스 작성",
    "API 클라이언트 구현"
  ],
  "pending_tasks": [
    "UserService 테스트",
    "로그인 UI",
    "문서화"
  ],
  "task_progress": {
    "completed": 5,
    "total": 12,
    "percentage": 42
  }
}
```

### 필드 설명

| 필드 | 필수 | 설명 |
|------|------|------|
| mode | ✅ | 저장 모드: quick, sync, full |
| saved_at | ✅ | ISO 형식 타임스탬프 |
| git_branch | ✅ | 현재 브랜치 |
| git_commit | ✅ | 마지막 커밋 해시 |
| git_pushed | ✅ | 원격에 푸시 여부 |
| openspec | ✅ | 현재 OpenSpec 번호 |
| openspec_status | ✅ | OpenSpec 상태 |
| working_on | ✅ | 현재 작업 설명 |
| next_steps | ✅ | 다음 작업 목록 |
| blocker | ❌ | 블로커 정보 (있을 경우) |
| completed_tasks | ❌ | 완료된 태스크 목록 |
| pending_tasks | ❌ | 대기 중인 태스크 목록 |
| task_progress | ❌ | 진행률 |

---

## 3. 저장 모드

| 모드 | 소요 시간 | 사용 시점 |
|------|----------|----------|
| **quick** | ~15초 | 시간별 체크포인트, WIP, 위험한 변경 전 |
| **sync** | ~30초 | 일과 종료, 서브태스크 완료 |
| **full** | ~3-5분 | 태스크 완료, 마일스톤 완료 |

---

## 4. /session:save 명령어

### Quick (기본)

```bash
/session:save
```

동작:
1. 수정된 파일 git add
2. WIP 커밋 생성: "WIP: [context] - checkpoint"
3. session-state.json 저장
4. 푸시 안 함

### Sync

```bash
/session:save --sync
```

동작:
1. Quick 동작 모두 수행
2. git push origin <branch>
3. session-state.json의 git_pushed = true

### Full

```bash
/session:save --full
```

동작:
1. Sync 동작 모두 수행
2. CHANGELOG.md 검증
3. ROADMAP.md 검증
4. CI/CD 결과 확인 (선택)

---

## 5. /session:load 명령어

```bash
/session:load
```

동작:
1. session-state.json 읽기
2. OpenSpec 로드
3. 상태 표시
4. 계속 여부 질문

---

## 6. 블로커 추적

### 블로커 타입 정의

| 타입 | 설명 | 자동 감지 | 복구 담당 |
|------|------|----------|----------|
| `build_error` | 빌드 실패 | ✓ | cpp-builder |
| `test_failure` | 테스트 실패 | ✓ | tester → code-editor |
| `dependency` | 의존성 문제 | ✓ | cpp-builder (vcpkg) |
| `design_issue` | 설계 문제 | ✗ | architect |
| `review_blocked` | 코드 리뷰 이슈 | ✓ | code-editor |
| `ci_failure` | CI/CD 파이프라인 실패 | ✓ | devops |
| `merge_conflict` | Git 머지 충돌 | ✓ | 수동 해결 |
| `other` | 기타 | ✗ | 수동 해결 |

### 블로커 스키마

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

### 자동 블로커 감지 로직

#### 빌드 오류 감지

```bash
# cpp-builder 출력에서 감지
grep -E "(error:|error C[0-9]+|fatal error|LNK[0-9]+)" build_output.log
```

감지 패턴:
- `error:` → GCC/Clang 컴파일 오류
- `error C[0-9]+` → MSVC 컴파일 오류
- `LNK[0-9]+` → 링커 오류
- `Could NOT find` → CMake 패키지 오류

#### 테스트 실패 감지

```bash
# ctest 출력에서 감지
ctest --output-on-failure 2>&1 | grep -E "(FAILED|Error)"
```

감지 패턴:
- `FAILED` → 테스트 케이스 실패
- `Error` → 테스트 런타임 오류

#### CI 실패 감지

```bash
# GitHub Actions 상태 확인
gh run list --limit 1 --json status,conclusion
```

감지 조건:
- `conclusion: "failure"` → CI 실패
- `conclusion: "cancelled"` → CI 취소

### 블로커 자동 기록

에이전트가 `[WORKFLOW_STATUS] status: BLOCKED` 보고 시:

```python
def auto_record_blocker(agent_output, agent_type):
    if "[WORKFLOW_STATUS]" in agent_output and "BLOCKED" in agent_output:
        blocker = detect_blocker_type(agent_output)
        update_session_state({
            "blocker": {
                "type": blocker.type,
                "severity": blocker.severity,
                "description": extract_description(agent_output),
                "detected_at": datetime.now().isoformat(),
                "auto_detected": True,
                "recovery_agent": get_recovery_agent(blocker.type)
            }
        })
```

---

## 7. 세션 시작 시 동작

### session-state.json 존재

```
═══════════════════════════════════════════════════════════════
SESSION RESTORED
═══════════════════════════════════════════════════════════════

OpenSpec: #00027 - 사용자 인증 기능
Status: IN_PROGRESS
Progress: 5/12 tasks (42%)

이전 작업: 사용자 인증 기능 구현 중

다음 단계:
- UserService 테스트 작성
- 로그인 UI 구현

═══════════════════════════════════════════════════════════════

계속할까요, 아니면 새 태스크를 시작할까요?
```

### session-state.json 없음

```
═══════════════════════════════════════════════════════════════
NEW SESSION
═══════════════════════════════════════════════════════════════

활성 태스크가 없습니다.

옵션:
- 작업할 내용을 설명해주세요
- "status"로 ROADMAP 확인
- "계속"으로 중단된 태스크 찾기

═══════════════════════════════════════════════════════════════
```

---

## 8. 세션 종료 시 권장사항

세션 종료 전 항상:

1. **변경사항 확인**
   ```bash
   git status
   ```

2. **세션 저장**
   - 일과 중: `/session:save`
   - 일과 종료: `/session:save --sync`
   - 태스크 완료: `/session:save --full`

3. **다음 단계 기록**
   - session-state.json의 next_steps 업데이트

---

## 9. 세션 복구 고급 기능

### /session:load --resume 옵션

자동 재개 모드로 세션을 복원합니다.

```bash
/session:load --resume
```

동작:
1. session-state.json 로드
2. 블로커 확인 → 자동 복구 시도
3. 마지막 작업 지점에서 자동 재개
4. 사용자 확인 없이 진행

**사용 시점:**
- 예상치 못한 세션 종료 후
- 블로커 자동 복구 시도
- 연속 작업 환경

### 복구 시 상태 검증

세션 로드 시 다음을 검증합니다:

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

#### Git 상태 검증

```bash
# 현재 브랜치 확인
current_branch=$(git branch --show-current)
[ "$current_branch" == "$saved_branch" ] || echo "BRANCH_MISMATCH"

# 커밋 확인
git log --oneline -1 | grep "$saved_commit" || echo "COMMIT_MISMATCH"

# 언커밋 변경 확인
[ -z "$(git status --porcelain)" ] || echo "UNCOMMITTED_CHANGES"
```

#### OpenSpec 존재 검증

```bash
# OpenSpec 디렉토리 확인
[ -d "openspec/changes/$openspec_id" ] || echo "OPENSPEC_NOT_FOUND"

# proposal.md 확인
[ -f "openspec/changes/$openspec_id/proposal.md" ] || echo "PROPOSAL_MISSING"
```

#### 파일 무결성 검증

```bash
# 수정된 파일 목록과 실제 상태 비교
for file in "${modified_files[@]}"; do
    [ -f "$file" ] || echo "FILE_MISSING: $file"
done
```

### 검증 결과 처리

| 상태 | 조치 |
|------|------|
| ALL_VALID | 정상 복원, 작업 계속 |
| BRANCH_MISMATCH | 브랜치 전환 질문 |
| COMMIT_MISMATCH | 동기화 상태 경고 |
| UNCOMMITTED_CHANGES | 커밋 또는 스태시 질문 |
| OPENSPEC_NOT_FOUND | 새 태스크 시작 제안 |
| BLOCKER_EXISTS | 블로커 해결 우선 제안 |

### 자동 복구 워크플로우

```
세션 로드
    ↓
상태 검증
    ↓
    ├─ 블로커 존재?
    │   ├─ auto_detected = true → 자동 복구 시도
    │   │   ├─ build_error → cpp-builder 호출
    │   │   ├─ test_failure → tester 호출
    │   │   ├─ dependency → vcpkg install
    │   │   └─ 복구 성공? → 블로커 해제
    │   │
    │   └─ auto_detected = false → 사용자에게 해결 방법 제안
    │
    └─ 블로커 없음 → 마지막 작업 지점에서 계속
```

### 세션 상태 무결성 검증

세션 저장/로드 시 무결성을 보장합니다:

```python
def verify_session_integrity(state):
    """세션 상태 무결성 검증"""

    # 1. 필수 필드 존재 확인
    required = ["mode", "saved_at", "git_branch", "openspec"]
    for field in required:
        if field not in state:
            return IntegrityError(f"Missing required field: {field}")

    # 2. 타임스탬프 유효성
    try:
        datetime.fromisoformat(state["saved_at"])
    except ValueError:
        return IntegrityError("Invalid timestamp format")

    # 3. 진행률 일관성
    if state.get("task_progress"):
        progress = state["task_progress"]
        if progress["completed"] > progress["total"]:
            return IntegrityError("Invalid progress: completed > total")

        expected_pct = (progress["completed"] / progress["total"]) * 100
        if abs(progress["percentage"] - expected_pct) > 1:
            return IntegrityError("Progress percentage mismatch")

    # 4. 블로커 스키마 검증
    if state.get("blocker"):
        blocker = state["blocker"]
        valid_types = ["build_error", "test_failure", "dependency",
                       "design_issue", "review_blocked", "ci_failure",
                       "merge_conflict", "other"]
        if blocker.get("type") not in valid_types:
            return IntegrityError(f"Invalid blocker type: {blocker.get('type')}")

    return IntegrityOK()
```

### 복구 실패 시 대응

```
═══════════════════════════════════════════════════════════════
SESSION RECOVERY FAILED
═══════════════════════════════════════════════════════════════

문제: Git 브랜치가 일치하지 않습니다.
- 저장된 브랜치: feature/user-auth
- 현재 브랜치: main

옵션:
[1] 저장된 브랜치로 전환 (git checkout feature/user-auth)
[2] 현재 브랜치에서 계속 (세션 상태 업데이트)
[3] 새 세션 시작

═══════════════════════════════════════════════════════════════
```

---

## 10. 핵심 규칙

1. **OpenSpec = 태스크의 진실**
   - session-state.json은 "어디까지 했는지"만 추적
   - 태스크 상세는 항상 OpenSpec 참조

2. **저장 습관화**
   - 중요한 변경 후 `/session:save`
   - 일과 종료 전 필수

3. **블로커 기록**
   - 막히면 blocker 필드에 자동/수동 기록
   - 해결 방법도 함께 기록
   - 복구 담당 에이전트 명시

4. **진행률 추적**
   - completed_tasks, pending_tasks 업데이트
   - task_progress 동기화

5. **복구 우선순위**
   - 블로커 해결 → Git 동기화 → 작업 재개

6. **무결성 검증**
   - 저장/로드 시 항상 검증
   - 불일치 발견 시 사용자에게 알림
