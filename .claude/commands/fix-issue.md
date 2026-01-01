---
description: "이슈 수정"
argument-hint: "<이슈 설명 또는 파일:라인>"
---

# Fix Issue Command

코드 리뷰나 테스트에서 발견된 이슈를 수정합니다.

## 사용법

```bash
/fix-issue "메모리 누수 수정"
/fix-issue src/core/user.cpp:45
/fix-issue                        # 현재 BLOCKED 이슈
```

## 인자

$ARGUMENTS

## 동작

1. 이슈 식별
   - 인자로 지정된 이슈
   - 또는 현재 세션의 blocker
   - 또는 code-reviewer/tester의 BLOCKED 컨텍스트

2. code-writer 에이전트 호출
   - 이슈 분석
   - 수정 코드 작성
   - 테스트 업데이트

3. 자동 재검증
   - 수정 후 code-reviewer 재실행
   - 또는 tester 재실행

## 이슈 소스

| 소스 | 동작 |
|------|------|
| code-reviewer BLOCKED | 리뷰 이슈 목록 수정 |
| tester BLOCKED | 빌드/테스트 오류 수정 |
| session blocker | 블로커 해결 |

## 결과

수정 완료 후 자동으로 이전 단계 재실행

## 관련 에이전트

`.claude/agents/code-writer.md`
