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

블로커가 있을 경우:

```json
{
  "blocker": {
    "type": "build_error|test_failure|dependency|design_issue|other",
    "description": "CMake 설정 오류로 빌드 실패",
    "resolution": "vcpkg.json 의존성 확인 필요",
    "appeared_after": "Qt6 버전 업그레이드 후"
  }
}
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

## 9. 핵심 규칙

1. **OpenSpec = 태스크의 진실**
   - session-state.json은 "어디까지 했는지"만 추적
   - 태스크 상세는 항상 OpenSpec 참조

2. **저장 습관화**
   - 중요한 변경 후 `/session:save`
   - 일과 종료 전 필수

3. **블로커 기록**
   - 막히면 blocker 필드에 기록
   - 해결 방법도 함께 기록

4. **진행률 추적**
   - completed_tasks, pending_tasks 업데이트
   - task_progress 동기화
