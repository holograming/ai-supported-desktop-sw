# Changelog

All notable changes to the OpenSpec-Qt Workflow Orchestrator will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-01-04

### Added

#### Parallel Agent System (Phase 6)
- **parallel_runner.py**: New module for parallel agent execution
  - `TaskNode`, `AgentTask`, `AgentResult` dataclasses
  - `DependencyGraph` for task dependency management
  - `ParallelRunner` for asyncio-based parallel execution
  - `TaskParser` for parsing tasks.md files
- **worktree_manager.py**: Git worktree management for isolated execution
  - `WorktreeInfo`, `MergeResult` dataclasses
  - `WorktreeManager` class for worktree lifecycle management
- `--parallel` / `-p` flag in main.py for parallel execution mode
- Parallel UI methods in ui.py:
  - `print_parallel_header()`, `print_parallel_task_start()`
  - `print_parallel_summary()`, `print_merge_status()`
- `parallel` section in workflow.json:
  - `max_concurrent_agents`, `worktree_dir`, `parallel_capable_agents`
  - `always_sequential` chain definitions

#### Session Recovery Enhancement (Phase 5)
- Extended blocker types (8 types with severity levels)
- Auto-recovery agent mapping
- Session state validation and integrity verification
- `--resume` option for /session:load

#### OpenSpec Initialization (Phase 4)
- `openspec-init` skill for project initialization
- Skip logic for existing OpenSpec detection
- Essential file templates (proposal.md, tasks.md)

#### Project Scaffolding (Phase 2)
- `project-scaffolding` skill for C++/QML projects
- Standard directory structure templates
- CMake and vcpkg integration templates

#### Documentation (Phase 7)
- `openspec/specs/orchestration/spec.md`
- `openspec/specs/session-management/spec.md`
- `openspec/specs/parallel-agents/spec.md`
- `openspec/specs/project-scaffolding/spec.md`

#### Testing
- 69 unit/integration tests with 100% pass rate
  - T.1: Workflow trigger matching (17 tests)
  - T.2: Session recovery scenarios (16 tests)
  - T.3: Parallel execution mock mode (22 tests)
  - T.4: OpenSpec initialization e2e (14 tests)

### Changed
- Updated workflow.json triggers: build keywords moved from `tester` to `cpp-builder`
- Agent alias `알렉스` changed to `로컬빌더`
- Updated CLAUDE.md with new skills, parallel execution docs, specs references

### Fixed
- Consistent agent naming and trigger keywords
- Build folder convention using `build/${presetName}/` pattern

## [1.0.0] - 2026-01-01

### Added
- Initial orchestrator framework
- 9 specialized AI agents
- Basic workflow rules engine
- Session state management
- OpenSpec workflow integration
