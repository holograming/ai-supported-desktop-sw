---
description: "세션 상태 저장"
argument-hint: "[--sync | --full]"
---

# Save Session Command

현재 작업 세션 상태를 저장합니다.

## 사용법

```bash
/session:save          # Quick - 로컬 체크포인트 (~15초)
/session:save --sync   # Sync - GitHub 푸시 포함 (~30초)
/session:save --full   # Full - 전체 검증 (~3-5분)
```

## 모드 선택 가이드

| 상황 | 명령어 |
|------|--------|
| 시간별 체크포인트 | `/session:save` |
| 위험한 변경 전 | `/session:save` |
| 일과 종료 | `/session:save --sync` |
| 서브태스크 완료 | `/session:save --sync` |
| 태스크 완료 | `/session:save --full` |
| 마일스톤 완료 | `/session:save --full` |

## 인자

$ARGUMENTS

---

## Quick 모드 (기본)

**동작:**
1. 수정된 파일 git add (임시 파일 제외)
2. WIP 커밋: "WIP: [context] - checkpoint"
3. `.claude/session-state.json` 저장
4. 푸시 안 함

**출력:**
```
Quick checkpoint saved (~12s)
Session: .claude/session-state.json
Commit: abc1234 (local only)
Progress: 5/8 tasks (62%)
```

---

## Sync 모드 (--sync)

**동작:**
1. Quick 모드 전체
2. git push origin <branch>
3. session-state.json의 git_pushed = true

**출력:**
```
Session synced to GitHub (~28s)
Commits: 5 pushed
Progress: 6/8 tasks (75%)
```

---

## Full 모드 (--full)

**동작:**
1. Sync 모드 전체
2. CHANGELOG.md 검증
3. ROADMAP.md 검증
4. (선택) CI/CD 결과 확인

**출력:**
```
Full verification complete (~4m)

Git: 8 commits pushed
Docs: CHANGELOG/ROADMAP verified
Task #00027: COMPLETE (8/8 tasks)
```

---

## session-state.json 형식

```json
{
  "mode": "quick",
  "saved_at": "2025-01-15T14:30:00",
  "git_branch": "feature/user-auth",
  "git_commit": "abc1234",
  "git_pushed": false,
  "openspec": "00027",
  "openspec_status": "IN_PROGRESS",
  "working_on": "사용자 인증 구현 중",
  "next_steps": ["테스트 작성", "UI 구현"],
  "task_progress": {
    "completed": 5,
    "total": 12,
    "percentage": 42
  }
}
```

---

## 세션 종료 전 필수

작업 종료 전 반드시 `/session:save` 실행!
