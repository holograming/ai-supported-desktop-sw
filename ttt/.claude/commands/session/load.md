---
description: "이전 세션 상태 복원"
argument-hint: ""
---

# Load Session Command

저장된 세션 상태를 복원합니다.

## 사용법

```bash
/session:load
```

## 동작

1. `.claude/session-state.json` 읽기
2. OpenSpec 상태 로드
3. 진행상황 표시
4. 계속 여부 질문

---

## 세션 복원 화면

### 세션 파일 존재 시

```
═══════════════════════════════════════════════════════════════
SESSION RESTORED
═══════════════════════════════════════════════════════════════

OpenSpec: #00027 - 사용자 인증 기능
Status: IN_PROGRESS
Branch: feature/user-auth
Last Commit: abc1234

Progress: 5/12 tasks (42%)

이전 작업:
사용자 인증 구현 중

다음 단계:
- UserService 테스트 작성
- 로그인 UI 구현

═══════════════════════════════════════════════════════════════

OpenSpec #00027 계속할까요, 아니면 새 태스크를 시작할까요?

[1] 계속
[2] 새 태스크
[3] 다른 태스크 보기
```

### 세션 파일 없음

```
═══════════════════════════════════════════════════════════════
NEW SESSION
═══════════════════════════════════════════════════════════════

저장된 세션이 없습니다.

옵션:
- 작업할 내용을 설명해주세요
- "status"로 ROADMAP 확인
- "계속"으로 중단된 태스크 찾기

═══════════════════════════════════════════════════════════════
```

---

## 블로커 감지 시

```
⚠️ 이전 세션에 블로커가 기록되어 있습니다:

Type: build_error
Description: CMake 설정 오류로 빌드 실패
Resolution: vcpkg.json 의존성 확인 필요

블로커를 먼저 해결할까요?
```

---

## Git 상태 확인

세션 복원 시 Git 상태도 확인:

```
📌 Git Status:
- Branch: feature/user-auth
- Unpushed commits: 3
- Uncommitted changes: 2 files

동기화가 필요할 수 있습니다.
```

---

## 관련 명령어

- `/session:save` - 세션 저장
- `workflow` - 워크플로우 실행
- `session` - 세션 트리거 (task-manager)
