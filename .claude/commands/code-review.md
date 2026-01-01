---
description: "코드 리뷰 수행"
argument-hint: "[파일 경로 또는 OpenSpec 번호]"
---

# Code Review Command

지정된 파일 또는 OpenSpec의 변경사항에 대해 코드 리뷰를 수행합니다.

## 사용법

```bash
/code-review                      # 현재 OpenSpec의 변경사항
/code-review src/core/user.cpp    # 특정 파일
/code-review 00027                # 특정 OpenSpec
```

## 인자

$ARGUMENTS

## 동작

code-reviewer 에이전트를 호출하여 코드 품질을 검사합니다.

## 체크리스트

### C++ 품질
- [ ] 네이밍 컨벤션 준수
- [ ] Modern C++ 패턴 사용
- [ ] const correctness
- [ ] 스마트 포인터 사용
- [ ] 예외 안전성

### QML 품질
- [ ] 컴포넌트 구조
- [ ] required property 사용
- [ ] 바인딩 최적화
- [ ] 로직 분리 (C++ vs QML)

### 테스트
- [ ] 테스트 존재 여부
- [ ] 커버리지 적절성
- [ ] 엣지 케이스 처리

### 보안
- [ ] 입력 검증
- [ ] 민감 정보 노출

## 결과

- **READY**: 리뷰 통과, 다음 단계로
- **BLOCKED**: 이슈 발견, 수정 필요

## 관련 에이전트

`.claude/agents/code-reviewer.md`
