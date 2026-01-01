---
name: openspec-workflow
description: "OpenSpec 태스크 관리 워크플로우. 태스크 생성, 추적, 종료 방법."
---

# OpenSpec Workflow

## 1. 폴더 구조

```
openspec/
├── changes/              # 진행 중인 변경
│   └── NNNNN-name/
│       ├── proposal.md   # 요구사항, 설계
│       └── tasks.md      # 체크박스 태스크 목록
├── archive/              # 완료된 변경
│   └── NNNNN-name/
└── AGENTS.md             # OpenSpec 사용 안내
```

---

## 2. 번호 체계

### 새 번호 찾기

```bash
# 마지막 번호 확인
ls openspec/changes/ | sort -r | head -1

# 또는
ls openspec/archive/ | sort -r | head -1
```

### 번호 형식
- 5자리 숫자, 0으로 패딩
- 예: `00001`, `00027`, `00128`
- 새 번호 = 가장 큰 번호 + 1

---

## 3. proposal.md 템플릿

```markdown
# NNNNN: Change Name

## Status
PENDING | IN_PROGRESS | DEPLOYED

## Summary
간단한 변경 요약 (1-2 문장)

## Goal
무엇을 달성하려고 하는가?

## Scope

### Included
- 포함되는 기능/변경 1
- 포함되는 기능/변경 2

### Excluded
- 제외되는 것 1
- 제외되는 것 2

## Acceptance Criteria
- [ ] 완료 기준 1
- [ ] 완료 기준 2
- [ ] 완료 기준 3

## Design
(architect 에이전트가 추가)

### UI 필요 여부
- [ ] UI 작업 필요 (designer 에이전트 호출)
- [ ] UI 작업 불필요

### 수정할 파일
- `path/to/file1.cpp`
- `path/to/file2.h`

### 새 파일
- `path/to/new_file.cpp`
- `path/to/new_file.h`

### 클래스 구조
- ClassName
  - m_member : Type
  - methodName() : ReturnType

## UI Design
(designer 에이전트가 추가, UI 필요시)

### 화면 구조
(ASCII 다이어그램)

### 컴포넌트 계층
- PageName.qml
  - ComponentA.qml
  - ComponentB.qml

## Notes
추가 컨텍스트, 결정 사항, 참조 링크 등
```

---

## 4. tasks.md 템플릿

```markdown
# Tasks for #NNNNN

## Phase 1: [Phase Name]

### Setup
- [ ] Task description
- [ ] Task description

### Implementation
- [ ] Task description
- [ ] Task description
- [ ] Task description

## Phase 2: [Phase Name]

### Feature A
- [ ] Task description
- [ ] Task description

## Testing
- [ ] Write unit tests
- [ ] Manual testing
- [ ] Edge case testing

## Documentation
- [ ] Update CHANGELOG.md
- [ ] Update ROADMAP.md (if new feature)
- [ ] Update API documentation

## Final
- [ ] Code review passed
- [ ] All tests passed
- [ ] Documentation complete
```

---

## 5. 상태 생명주기

```
PENDING → IN_PROGRESS → DEPLOYED
```

### PENDING
- 요구사항 수집 완료
- 설계 전 또는 설계 중
- 구현 시작 전

### IN_PROGRESS
- 설계 완료
- 구현 진행 중
- 테스트 진행 중

### DEPLOYED
- 모든 태스크 완료
- 코드 리뷰 통과
- 테스트 통과
- 문서 업데이트 완료
- Git 커밋 완료

---

## 6. 태스크 생성 절차

1. **아이디어 확인**
   - 사용자에게 구체적인 아이디어가 있는지 확인
   - 없으면 ROADMAP.md에서 미완료 항목 제안

2. **요구사항 수집**
   - GOAL: 무엇을 달성?
   - SCOPE: 무엇이 포함/제외?
   - CRITERIA: 어떻게 완료 확인?
   - 사용자가 "OK"라고 할 때까지 반복

3. **번호 할당**
   - 마지막 번호 확인
   - +1 증가

4. **폴더 및 파일 생성**
   ```
   openspec/changes/NNNNN-name/
   ├── proposal.md
   └── tasks.md
   ```

5. **상태 설정**
   - Status: PENDING

---

## 7. 진행상황 추적

### 활성 태스크 찾기

```bash
grep -l "Status.*IN_PROGRESS\|Status.*PENDING" openspec/changes/*/proposal.md
```

### 진행률 계산

```bash
# tasks.md에서 체크박스 카운트
# [x] = 완료
# [ ] = 미완료

completed=$(grep -c "\[x\]" tasks.md)
total=$(grep -c "\[.\]" tasks.md)
echo "Progress: $completed / $total"
```

---

## 8. 태스크 종료 절차

### 종료 전 검증

1. **tasks.md 검증**
   - 모든 체크박스가 [x]인지 확인

2. **문서 검증**
   - CHANGELOG.md에 [Unreleased] 항목 있는지
   - ROADMAP.md에 체크박스 [x] (새 기능인 경우)

3. **품질 검증**
   - 코드 리뷰 통과
   - 테스트 통과

### 종료 절차

1. proposal.md에서 Status → DEPLOYED 변경
2. 커밋 메시지 생성:
   ```
   feat(scope): Brief description
   
   - Detail 1
   - Detail 2
   
   Closes OpenSpec #NNNNN
   ```

### 아카이브 (선택)

```bash
# 완료된 OpenSpec을 archive로 이동
mv openspec/changes/NNNNN-name openspec/archive/
```

---

## 9. 커밋 메시지 형식

```
<type>(<scope>): <description>

[body]

Closes OpenSpec #NNNNN

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

### Type 목록
- `feat`: 새 기능
- `fix`: 버그 수정
- `docs`: 문서 변경
- `style`: 코드 스타일 (동작 변경 없음)
- `refactor`: 리팩토링
- `test`: 테스트 추가/수정
- `chore`: 빌드, 도구 설정 등
- `build`: 빌드 시스템 변경

---

## 10. 팁

### 좋은 태스크 작성법
- 구체적이고 검증 가능하게
- 한 태스크 = 한 커밋 정도 크기
- 의존성 순서대로 나열

### OpenSpec 크기
- 너무 크면 분할 고려
- 1-2주 분량이 적당
- Phase로 나누어 관리
