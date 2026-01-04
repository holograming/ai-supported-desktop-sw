---
name: openspec-init
description: "OpenSpec 구조 초기화 - 신규 프로젝트에 OpenSpec 디렉토리와 필수 파일 생성"
---

# OpenSpec Initialization Skill

## Overview

신규 프로젝트에 OpenSpec 명세 주도 개발(Spec-Driven Development) 구조를 초기화합니다.

## Usage

```bash
/openspec:init
```

## Trigger Keywords

- `/openspec:init`
- "openspec 초기화"
- "init openspec"
- "openspec 설정"

## Prerequisites

- Git 저장소가 초기화되어 있어야 함
- 프로젝트 루트에서 실행

---

## Initialization Process

### Step 1: Detect Existing OpenSpec

```bash
# 기존 OpenSpec 감지
if [ -f "openspec/project.md" ]; then
    echo "EXISTING"
else
    echo "NEW"
fi
```

**기존 존재 시 처리:**
- 사용자에게 옵션 제시 (유지/덮어쓰기/취소)
- 기본값: 유지 (권장)

### Step 2: Create Directory Structure

```bash
mkdir -p openspec/{specs,changes,changes/archive}
```

결과:
```
openspec/
├── specs/           # 현재 스펙 (구축된 것)
├── changes/         # 변경 제안
│   └── archive/     # 완료된 변경
├── project.md       # 프로젝트 컨벤션
└── AGENTS.md        # AI 에이전트 지침
```

### Step 3: Generate project.md

```markdown
# Project Context

## Purpose

[프로젝트의 목적과 비전을 설명]

## Tech Stack

### Core
- [주요 언어/프레임워크]
- [빌드 시스템]
- [패키지 관리자]

### CI/CD
- [CI/CD 도구]

## Project Conventions

### Code Style

[코딩 스타일 가이드]

### Architecture Patterns

[아키텍처 패턴 설명]

### Testing Strategy

[테스트 전략]

### Git Workflow

- **메인 브랜치**: main
- **기능 브랜치**: feature/{feature-name}
- **커밋 메시지**: Conventional Commits

## Domain Context

[도메인 특화 컨텍스트]

## Important Constraints

[기술적 제약사항]

## External Dependencies

[외부 의존성 목록]
```

### Step 4: Generate AGENTS.md

OpenSpec CLI에서 제공하는 표준 AGENTS.md 템플릿을 사용합니다.

```bash
# OpenSpec CLI가 설치되어 있으면
openspec init .

# 또는 수동으로 템플릿 복사
```

### Step 5: Update CLAUDE.md

CLAUDE.md에 OpenSpec 지침 블록을 추가합니다:

```markdown
<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals
- Introduces new capabilities, breaking changes, architecture shifts
- Sounds ambiguous and you need the authoritative spec

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->
```

### Step 6: Validate

```bash
# 구조 검증
ls -la openspec/
ls -la openspec/specs/
ls -la openspec/changes/

# 파일 존재 확인
test -f openspec/project.md && echo "project.md OK"
test -f openspec/AGENTS.md && echo "AGENTS.md OK"
```

---

## Skip Logic

### When to Skip

1. **openspec/project.md 존재**: 사용자 확인 필요
2. **openspec/ 디렉토리만 존재**: 파일 생성 진행
3. **완전히 새로운 프로젝트**: 전체 초기화

### Skip Decision Tree

```
openspec/project.md 존재?
├─ YES → 사용자에게 질문
│        ├─ 유지 → 종료
│        ├─ 덮어쓰기 → 백업 후 재생성
│        └─ 취소 → 종료
│
└─ NO → openspec/ 디렉토리 존재?
        ├─ YES → 파일만 생성
        └─ NO → 전체 초기화
```

---

## Output Format

### Success

```
═══════════════════════════════════════════════════════════════
OPENSPEC INITIALIZED
═══════════════════════════════════════════════════════════════

생성된 파일:
✓ openspec/project.md
✓ openspec/AGENTS.md
✓ openspec/specs/ (디렉토리)
✓ openspec/changes/ (디렉토리)

다음 단계:
1. openspec/project.md 수정
   - Purpose, Tech Stack, Conventions 채우기

2. 변경 제안 생성
   - "새 태스크" 또는 "/openspec:proposal"

═══════════════════════════════════════════════════════════════
```

### Already Exists

```
═══════════════════════════════════════════════════════════════
OPENSPEC ALREADY EXISTS
═══════════════════════════════════════════════════════════════

openspec/project.md가 이미 존재합니다.

현재 상태:
- specs: 3개 스펙
- changes: 1개 진행 중

옵션:
[1] 기존 유지 (권장)
[2] 덮어쓰기 (주의: 기존 설정 손실)
[3] 취소

═══════════════════════════════════════════════════════════════
```

### Error

```
═══════════════════════════════════════════════════════════════
OPENSPEC INIT FAILED
═══════════════════════════════════════════════════════════════

오류: Git 저장소가 아닙니다.

해결:
git init

═══════════════════════════════════════════════════════════════
```

---

## Integration with Workflow

### workflow.json 트리거

```json
{
  "triggers": {
    "task-manager": [
      "openspec 초기화",
      "init openspec",
      ...
    ]
  }
}
```

### 담당 에이전트

- **task-manager (달미)**: OpenSpec 초기화 담당
- MODE 5: OPENSPEC INITIALIZATION 참조

---

## Templates Reference

### project.md 템플릿 위치

`.claude/templates/project-structure.md` 참조

### AGENTS.md 템플릿

OpenSpec CLI 또는 공식 GitHub 저장소에서 최신 버전 사용

---

## Best Practices

1. **초기화 전 확인**: 기존 openspec 구조 확인
2. **백업**: 덮어쓰기 전 기존 파일 백업
3. **커밋**: 초기화 후 즉시 커밋
4. **문서화**: project.md를 프로젝트에 맞게 수정

---

## Related Skills

- `openspec-workflow`: OpenSpec 워크플로우 전체
- `session-protocol`: 세션 관리
- `project-scaffolding`: 프로젝트 스캐폴딩
