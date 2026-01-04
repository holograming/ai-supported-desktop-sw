"""
OpenSpec-Qt Project Workflow Orchestrator

A Python-based workflow automation engine for Claude Code.
Manages agent transitions based on rules defined in workflow.json.

Modules:
- main.py           : Entry point, CLI interface
- engine.py         : Rule matching logic
- protocol.py       : Agent output parsing
- runner.py         : Agent execution (sequential)
- parallel_runner.py: Agent execution (parallel with worktrees)
- worktree_manager.py: Git worktree management
- state.py          : Workflow state management
- ui.py             : Terminal UI
"""

__version__ = "1.1.0"
