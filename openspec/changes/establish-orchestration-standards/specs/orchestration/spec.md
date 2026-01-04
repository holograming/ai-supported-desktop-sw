# Capability: orchestration

에이전트 오케스트레이션의 핵심 규칙을 정의한다.

---

## ADDED Requirements

### Requirement: Agent Naming Convention
The system SHALL enforce kebab-case naming for all agents.

#### Scenario: Agent name validation
- **WHEN** 새 에이전트를 workflow.json에 추가할 때
- **THEN** 이름은 `[a-z][a-z0-9-]*` 패턴을 따라야 한다
- **AND** `.claude/agents/{name}.md` 파일이 존재해야 한다

#### Scenario: Trigger synchronization
- **WHEN** workflow.json의 triggers가 정의될 때
- **THEN** 모든 에이전트 이름은 AVAILABLE_AGENTS 목록과 정확히 일치해야 한다

---

### Requirement: Workflow Status Protocol
The system SHALL require all agents to include a [WORKFLOW_STATUS] block at the end of their response.

#### Scenario: Status block format
- **WHEN** 에이전트가 태스크를 완료할 때
- **THEN** 다음 형식의 상태 블록을 반환해야 한다:
  ```
  [WORKFLOW_STATUS]
  status: READY|BLOCKED|FAILED|DECISION_NEEDED
  context: <설명>
  next_hint: <다음 단계>
  ```

#### Scenario: Status fallback parsing
- **WHEN** 명시적 상태 블록이 없을 때
- **THEN** 출력의 마지막 10줄에서 패턴 매칭으로 상태를 추론한다

---

### Requirement: Workflow Rule Matching
The system SHALL match workflow rules based on agent, status, and context combination.

#### Scenario: Rule priority
- **WHEN** 여러 규칙이 매칭될 때
- **THEN** priority가 높은 규칙이 우선 적용된다

#### Scenario: Retry loop detection
- **WHEN** 동일한 agent-status 조합이 3회 이상 반복될 때
- **THEN** 루프로 간주하고 DECISION_NEEDED 상태로 전환한다
