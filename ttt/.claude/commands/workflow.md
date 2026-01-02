---
description: "워크플로우 실행 - 태스크 자동 오케스트레이션"
argument-hint: <태스크 설명>
---

# Workflow Command

태스크에 대한 전체 워크플로우를 실행합니다.

## 사용법

```bash
/workflow "사용자 인증 기능 구현"
/workflow "버그 수정: 로그인 버튼 동작 안 함"
```

## 워크플로우 순서

```
1. task-manager  → OpenSpec 생성 (요구사항 수집)
2. architect     → 코드 분석, 솔루션 설계
3. [UI 필요?]
   ├─ YES → designer → UI/UX 디자인
   └─ NO  → (skip)
4. code-writer   → 코드 구현
5. code-reviewer → 코드 리뷰
6. tester        → 빌드 및 테스트
7. task-manager  → 태스크 종료
```

## 입력

$ARGUMENTS

## 동작

1. task-manager 에이전트로 태스크 생성
2. workflow.json 규칙에 따라 순차 실행
3. 각 단계에서 사용자 확인 요청 (필요시)
4. 완료 시 요약 표시

## 주요 결정 포인트

- **architect 완료 후**: UI 필요 여부 판단
- **code-reviewer 이슈 발견**: 수정 후 재리뷰
- **tester 실패**: 수정 후 재테스트

## 중단 시

워크플로우 중단 시 `/session:save`으로 상태 저장 권장
