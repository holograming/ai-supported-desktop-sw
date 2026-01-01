# OpenSpec 지침서

OpenSpec을 사용한 명세 주도 개발(Spec-Driven Development)을 위한 AI 코딩 어시스턴트 지침서입니다.

## 빠른 체크리스트

- 기존 작업 검색: `openspec spec list --long`, `openspec list` (전문 검색은 `rg` 사용)
- 범위 결정: 새 기능 vs 기존 기능 수정
- 고유한 `change-id` 선택: kebab-case, 동사로 시작 (`add-`, `update-`, `remove-`, `refactor-`)
- 스캐폴딩: `proposal.md`, `tasks.md`, `design.md` (필요시), 영향받는 기능별 델타 스펙
- 델타 작성: `## ADDED|MODIFIED|REMOVED|RENAMED Requirements` 사용; 요구사항당 최소 하나의 `#### Scenario:` 포함
- 검증: `openspec validate [change-id] --strict` 실행 후 이슈 수정
- 승인 요청: 제안이 승인되기 전까지 구현 시작 금지

## 3단계 워크플로우

### 1단계: 변경 제안 작성

제안이 필요한 경우:
- 기능 추가
- 브레이킹 체인지 (API, 스키마)
- 아키텍처/패턴 변경
- 성능 최적화 (동작 변경)
- 보안 패턴 업데이트

제안 트리거 (예시):
- "변경 제안 작성해줘"
- "변경 계획 세워줘"
- "스펙 제안 작성해줘"

제안 생략 가능한 경우:
- 버그 수정 (의도된 동작 복원)
- 오타, 포맷, 주석
- 의존성 업데이트 (논브레이킹)
- 설정 변경
- 기존 동작에 대한 테스트

**작업 절차**
1. `openspec/project.md`, `openspec list`, `openspec list --specs`로 현재 컨텍스트 파악
2. 동사로 시작하는 고유한 `change-id` 선택, `openspec/changes/<id>/` 아래에 `proposal.md`, `tasks.md`, 선택적 `design.md`, 스펙 델타 스캐폴딩
3. `## ADDED|MODIFIED|REMOVED Requirements`로 스펙 델타 작성, 요구사항당 최소 하나의 `#### Scenario:` 포함
4. `openspec validate <id> --strict` 실행 후 이슈 수정, 제안 공유

### 2단계: 변경 구현

단계별로 TODO 추적하며 진행:
1. **proposal.md 읽기** - 무엇을 만드는지 이해
2. **design.md 읽기** (있는 경우) - 기술 결정 검토
3. **tasks.md 읽기** - 구현 체크리스트 확인
4. **순차적으로 태스크 구현** - 순서대로 완료
5. **완료 확인** - `tasks.md`의 모든 항목 완료 확인
6. **체크리스트 업데이트** - 모든 태스크를 `- [x]`로 변경
7. **승인 게이트** - 제안 검토 및 승인 전까지 구현 시작 금지

### 3단계: 변경 아카이브

배포 후 별도 PR 생성:
- `changes/[name]/` → `changes/archive/YYYY-MM-DD-[name]/`로 이동
- 기능이 변경된 경우 `specs/` 업데이트
- 도구 전용 변경은 `openspec archive <change-id> --skip-specs --yes` 사용
- `openspec validate --strict`로 아카이브된 변경 검증

## 작업 시작 전 체크리스트

**컨텍스트 확인:**
- [ ] `specs/[capability]/spec.md`에서 관련 스펙 읽기
- [ ] `changes/`에서 진행 중인 변경과 충돌 확인
- [ ] `openspec/project.md`에서 규칙 확인
- [ ] `openspec list`로 활성 변경 확인
- [ ] `openspec list --specs`로 기존 기능 확인

**스펙 작성 전:**
- 항상 기능이 이미 존재하는지 확인
- 중복 생성보다 기존 스펙 수정 선호
- `openspec show [spec]`으로 현재 상태 검토
- 요청이 모호하면 스캐폴딩 전에 1-2개 명확화 질문

### 검색 가이드
- 스펙 나열: `openspec spec list --long` (스크립트용 `--json`)
- 변경 나열: `openspec list` (또는 `openspec change list --json`)
- 상세 보기:
  - 스펙: `openspec show <spec-id> --type spec` (필터용 `--json`)
  - 변경: `openspec show <change-id> --json --deltas-only`
- 전문 검색 (ripgrep): `rg -n "Requirement:|Scenario:" openspec/specs`

## CLI 명령어

```bash
# 필수 명령어
openspec list                  # 활성 변경 목록
openspec list --specs          # 스펙 목록
openspec show [item]           # 변경 또는 스펙 보기
openspec validate [item]       # 변경 또는 스펙 검증
openspec archive <change-id> [--yes|-y]   # 배포 후 아카이브

# 프로젝트 관리
openspec init [path]           # OpenSpec 초기화
openspec update [path]         # 지침 파일 업데이트

# 대화형 모드
openspec show                  # 선택 프롬프트
openspec validate              # 일괄 검증 모드

# 디버깅
openspec show [change] --json --deltas-only
openspec validate [change] --strict
```

### 명령어 플래그

- `--json` - 기계 읽기 가능 출력
- `--type change|spec` - 항목 구분
- `--strict` - 종합 검증
- `--no-interactive` - 프롬프트 비활성화
- `--skip-specs` - 스펙 업데이트 없이 아카이브
- `--yes`/`-y` - 확인 프롬프트 건너뛰기

## 디렉토리 구조

```
openspec/
├── project.md              # 프로젝트 규칙
├── specs/                  # 현재 진실 - 구축된 것
│   └── [capability]/       # 단일 집중 기능
│       ├── spec.md         # 요구사항과 시나리오
│       └── design.md       # 기술 패턴
├── changes/                # 제안 - 변경할 것
│   ├── [change-name]/
│   │   ├── proposal.md     # 이유, 내용, 영향
│   │   ├── tasks.md        # 구현 체크리스트
│   │   ├── design.md       # 기술 결정 (선택)
│   │   └── specs/          # 델타 변경
│   │       └── [capability]/
│   │           └── spec.md # ADDED/MODIFIED/REMOVED
│   └── archive/            # 완료된 변경
```

## 변경 제안 작성

### 결정 트리

```
새 요청?
├─ 스펙 동작 복원하는 버그 수정? → 바로 수정
├─ 오타/포맷/주석? → 바로 수정
├─ 새 기능? → 제안 작성
├─ 브레이킹 체인지? → 제안 작성
├─ 아키텍처 변경? → 제안 작성
└─ 불확실? → 제안 작성 (더 안전함)
```

### 제안 구조

1. **디렉토리 생성:** `changes/[change-id]/` (kebab-case, 동사 시작, 고유)

2. **proposal.md 작성:**
```markdown
# 변경: [변경 간략 설명]

## 이유
[문제/기회에 대한 1-2문장]

## 변경 내용
- [변경 사항 글머리 목록]
- [브레이킹 체인지는 **BREAKING** 표시]

## 영향
- 영향받는 스펙: [기능 목록]
- 영향받는 코드: [주요 파일/시스템]
```

3. **스펙 델타 생성:** `specs/[capability]/spec.md`
```markdown
## ADDED Requirements
### Requirement: 새 기능
시스템은 ...를 제공해야 한다(SHALL).

#### Scenario: 성공 케이스
- **WHEN** 사용자가 작업 수행
- **THEN** 예상 결과

## MODIFIED Requirements
### Requirement: 기존 기능
[완전한 수정된 요구사항]

## REMOVED Requirements
### Requirement: 이전 기능
**이유**: [제거 이유]
**마이그레이션**: [처리 방법]
```
여러 기능이 영향받으면 `changes/[change-id]/specs/<capability>/spec.md`에 기능별로 여러 델타 파일 생성.

4. **tasks.md 작성:**
```markdown
## 1. 구현
- [ ] 1.1 데이터베이스 스키마 생성
- [ ] 1.2 API 엔드포인트 구현
- [ ] 1.3 프론트엔드 컴포넌트 추가
- [ ] 1.4 테스트 작성
```

5. **design.md 작성 (필요시):**
다음 조건 중 하나라도 해당되면 작성, 그렇지 않으면 생략:
- 교차 변경 (여러 서비스/모듈) 또는 새 아키텍처 패턴
- 새 외부 의존성 또는 중요한 데이터 모델 변경
- 보안, 성능, 마이그레이션 복잡성
- 코딩 전 기술 결정이 필요한 모호함

최소 `design.md` 스켈레톤:
```markdown
## 컨텍스트
[배경, 제약, 이해관계자]

## 목표 / 비목표
- 목표: [...]
- 비목표: [...]

## 결정
- 결정: [무엇과 이유]
- 고려한 대안: [옵션 + 근거]

## 위험 / 트레이드오프
- [위험] → 완화

## 마이그레이션 계획
[단계, 롤백]

## 열린 질문
- [...]
```

## 스펙 파일 형식

### 중요: 시나리오 형식

**올바른 형식** (#### 헤더 사용):
```markdown
#### Scenario: 사용자 로그인 성공
- **WHEN** 유효한 자격 증명 제공
- **THEN** JWT 토큰 반환
```

**잘못된 형식** (글머리 또는 굵게 사용 금지):
```markdown
- **Scenario: 사용자 로그인**  ❌
**Scenario**: 사용자 로그인     ❌
### Scenario: 사용자 로그인      ❌
```

모든 요구사항은 최소 하나의 시나리오가 있어야 합니다.

### 요구사항 문구
- 규범적 요구사항에는 SHALL/MUST 사용 (의도적으로 비규범적이 아닌 한 should/may 피함)

### 델타 연산

- `## ADDED Requirements` - 새 기능
- `## MODIFIED Requirements` - 변경된 동작
- `## REMOVED Requirements` - 폐기된 기능
- `## RENAMED Requirements` - 이름 변경

헤더는 `trim(header)`로 매칭 - 공백 무시.

#### ADDED vs MODIFIED 사용 시점
- ADDED: 독립적인 요구사항으로 성립하는 새 기능 도입. 기존 요구사항 의미 변경보다 직교적 변경(예: "슬래시 명령어 설정" 추가)에 ADDED 선호.
- MODIFIED: 기존 요구사항의 동작, 범위, 수락 기준 변경. 항상 전체 업데이트된 요구사항 내용(헤더 + 모든 시나리오) 붙여넣기. 아카이버가 여기 제공된 내용으로 전체 요구사항 교체; 부분 델타는 이전 세부사항 손실.
- RENAMED: 이름만 변경. 동작도 변경하면 RENAMED (이름) + MODIFIED (내용, 새 이름 참조) 사용.

흔한 실수: 이전 텍스트 포함 없이 MODIFIED로 새 관심사 추가. 아카이브 시 세부사항 손실 발생. 기존 요구사항을 명시적으로 변경하지 않으면 ADDED로 새 요구사항 추가.

MODIFIED 요구사항 올바르게 작성:
1) `openspec/specs/<capability>/spec.md`에서 기존 요구사항 찾기.
2) 전체 요구사항 블록 복사 (`### Requirement: ...`부터 시나리오까지).
3) `## MODIFIED Requirements` 아래 붙여넣고 새 동작 반영하여 편집.
4) 헤더 텍스트가 정확히 일치하는지 확인(공백 무관) 및 최소 하나의 `#### Scenario:` 유지.

RENAMED 예시:
```markdown
## RENAMED Requirements
- FROM: `### Requirement: 로그인`
- TO: `### Requirement: 사용자 인증`
```

## 문제 해결

### 일반적인 오류

**"변경에 최소 하나의 델타가 있어야 합니다"**
- `changes/[name]/specs/`가 .md 파일과 함께 존재하는지 확인
- 파일에 연산 접두사(## ADDED Requirements)가 있는지 확인

**"요구사항에 최소 하나의 시나리오가 있어야 합니다"**
- 시나리오가 `#### Scenario:` 형식인지 확인 (# 4개)
- 시나리오 헤더에 글머리나 굵게 사용 금지

**시나리오 파싱 실패 (조용히)**
- 정확한 형식 필요: `#### Scenario: 이름`
- 디버그: `openspec show [change] --json --deltas-only`

### 검증 팁

```bash
# 종합 검사에는 항상 strict 모드 사용
openspec validate [change] --strict

# 델타 파싱 디버그
openspec show [change] --json | jq '.deltas'

# 특정 요구사항 확인
openspec show [spec] --json -r 1
```

## 베스트 프랙티스

### 단순함 우선
- 기본적으로 새 코드 100줄 미만
- 불충분함이 증명될 때까지 단일 파일 구현
- 명확한 정당화 없이 프레임워크 피함
- 지루하고 검증된 패턴 선택

### 복잡성 트리거
복잡성 추가는 다음과 함께만:
- 현재 솔루션이 너무 느리다는 성능 데이터
- 구체적인 규모 요구사항 (>1000 사용자, >100MB 데이터)
- 추상화가 필요한 여러 검증된 유즈케이스

### 명확한 참조
- 코드 위치에 `file.ts:42` 형식 사용
- 스펙은 `specs/auth/spec.md`로 참조
- 관련 변경과 PR 링크

### 기능 네이밍
- 동사-명사 사용: `user-auth`, `payment-capture`
- 기능당 단일 목적
- 10분 이해 규칙
- 설명에 "그리고"가 필요하면 분할

### 변경 ID 네이밍
- kebab-case, 짧고 설명적: `add-two-factor-auth`
- 동사 접두사 선호: `add-`, `update-`, `remove-`, `refactor-`
- 고유성 보장; 이미 있으면 `-2`, `-3` 등 추가

## 도구 선택 가이드

| 작업 | 도구 | 이유 |
|------|------|------|
| 패턴으로 파일 찾기 | Glob | 빠른 패턴 매칭 |
| 코드 내용 검색 | Grep | 최적화된 정규식 검색 |
| 특정 파일 읽기 | Read | 직접 파일 접근 |
| 알 수 없는 범위 탐색 | Task | 다단계 조사 |

## 오류 복구

### 변경 충돌
1. `openspec list`로 활성 변경 확인
2. 겹치는 스펙 확인
3. 변경 소유자와 조율
4. 제안 통합 고려

### 검증 실패
1. `--strict` 플래그로 실행
2. 상세 내용은 JSON 출력 확인
3. 스펙 파일 형식 확인
4. 시나리오 형식이 올바른지 확인

### 컨텍스트 부족
1. 먼저 project.md 읽기
2. 관련 스펙 확인
3. 최근 아카이브 검토
4. 명확화 요청

## 빠른 참조

### 단계 지표
- `changes/` - 제안됨, 아직 구축 안 됨
- `specs/` - 구축되어 배포됨
- `archive/` - 완료된 변경

### 파일 목적
- `proposal.md` - 이유와 내용
- `tasks.md` - 구현 단계
- `design.md` - 기술 결정
- `spec.md` - 요구사항과 동작

### CLI 필수
```bash
openspec list              # 진행 중인 것?
openspec show [item]       # 상세 보기
openspec validate --strict # 올바른가?
openspec archive <change-id> [--yes|-y]  # 완료 표시
```

기억하세요: 스펙은 진실입니다. 변경은 제안입니다. 동기화를 유지하세요.
