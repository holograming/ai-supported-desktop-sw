# Tasks for establish-orchestration-standards

## Phase 0: Foundation (선행 작업)
- [x] 0.1 openspec/project.md 템플릿 내용 채우기
- [x] 0.2 기존 구현 상태 정리 문서 작성 → `status.md`

## Phase 1: Agent Workflow Consistency (항목 1)
**의존성**: Phase 0 완료 필요

- [x] 1.1 workflow.json 트리거 수정 (빌드 키워드 tester→cpp-builder, 별칭 알렉스→로컬빌더)
- [x] 1.2 AVAILABLE_AGENTS 목록에 cpp-builder 추가 (main.py)
- [x] 1.3 에이전트 별칭 트리거 일관성 검증 완료
- [x] 1.4 문서화: Agent Naming Convention 섹션 추가 (project.md)

## Phase 2: Project Folder Structure (항목 2)
**의존성**: Phase 1과 병렬 가능

- [x] 2.1 .claude/templates/project-structure.md 생성
- [x] 2.2 C++/QML 프로젝트 표준 구조 정의 (project-structure.md에 포함)
- [x] 2.3 신규 프로젝트 스캐폴딩 스크립트 작성 (SKILL.md에 포함)
- [x] 2.4 project-scaffolding 스킬 추가

## Phase 3: Build Folder Convention (항목 3)
**의존성**: Phase 2와 병렬 가능

- [x] 3.1 CMakePresets.json의 binaryDir 규칙 검증 (modern-cmake 스킬에 문서화)
- [x] 3.2 빌드 아티팩트 경로 검증 함수 cpp-builder에 추가
- [x] 3.3 modern-cmake 스킬에 빌드 폴더 규칙 명시 추가 (Section 8)
- [x] 3.4 .gitignore 표준화 (build/ 패턴 추가 완료)

## Phase 4: OpenSpec Initialization (항목 4)
**의존성**: Phase 0 완료 필요

- [x] 4.1 task-manager.md에 OpenSpec 초기화 MODE 5 추가
- [x] 4.2 /openspec:init 스킬 명세 작성 (openspec-init/SKILL.md)
- [x] 4.3 초기화 시 필수 파일 생성 로직 구현 (SKILL.md에 포함)
- [x] 4.4 기존 openspec 감지 및 스킵 로직 (Skip Decision Tree)

## Phase 5: Session Recovery Enhancement (항목 5)
**의존성**: Phase 1 완료 필요

- [x] 5.1 blocker 타입 정의 확장 (8개 타입 + severity + recovery_agent)
- [x] 5.2 자동 blocker 감지 로직 session-protocol에 추가
- [x] 5.3 복구 시 상태 검증 함수 구현 (validate_session_state)
- [x] 5.4 자동 재개 옵션 추가 (/session:load --resume)
- [x] 5.5 세션 상태 무결성 검증 로직 (verify_session_integrity)

## Phase 6: Parallel Agent System (항목 6)
**의존성**: Phase 1, 5 완료 필요
**참조**: design.md 참조 필요

### 6.1 설계
- [ ] 6.1.1 design.md 완성: Git worktree 아키텍처 설계
- [ ] 6.1.2 의존성 그래프 모델링
- [ ] 6.1.3 브랜치 전략 정의
- [ ] 6.1.4 충돌 해결 정책 문서화

### 6.2 구현
- [ ] 6.2.1 parallel_runner.py 신규 모듈 구현
- [ ] 6.2.2 worktree 생성/삭제 유틸리티
- [ ] 6.2.3 태스크 의존성 그래프 파서
- [ ] 6.2.4 병렬 실행 상태 추적
- [ ] 6.2.5 결과 머지 및 충돌 감지

### 6.3 통합
- [ ] 6.3.1 workflow.json에 parallel_mode 옵션 추가
- [ ] 6.3.2 main.py에 병렬 실행 플래그 추가 (--parallel)
- [ ] 6.3.3 UI에 병렬 상태 표시 추가

## Phase 7: Documentation & Specs
**의존성**: 모든 구현 완료 후

- [ ] 7.1 openspec/specs/orchestration/spec.md 작성
- [ ] 7.2 openspec/specs/session-management/spec.md 작성
- [ ] 7.3 openspec/specs/parallel-agents/spec.md 작성
- [ ] 7.4 openspec/specs/project-scaffolding/spec.md 작성
- [ ] 7.5 CLAUDE.md 업데이트 (새 스킬/명령어 반영)

## Testing
- [ ] T.1 workflow.json 트리거 매칭 단위 테스트
- [ ] T.2 세션 복구 시나리오 테스트
- [ ] T.3 병렬 실행 통합 테스트 (mock mode)
- [ ] T.4 OpenSpec 초기화 end-to-end 테스트

## Final
- [ ] F.1 코드 리뷰 통과
- [ ] F.2 모든 테스트 통과
- [ ] F.3 문서화 완료
- [ ] F.4 CHANGELOG.md 업데이트
