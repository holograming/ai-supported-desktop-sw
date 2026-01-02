#!/usr/bin/env python3
"""
OpenSpec-Qt Project Workflow Orchestrator - Main Entry Point

Usage:
    python -m orchestrator.main "new task - user service"
    python -m orchestrator.main --mock "test task"
    python -m orchestrator.main --verbose --mock "test"

Requirements:
    - Python 3.8+
    - claude-agent-sdk (optional, for real agent execution)
"""

import argparse
import asyncio
import json
import sys
import time
from pathlib import Path
from typing import Optional, Dict, Any

from .protocol import StatusParser, PromptInjector, WorkflowStatus
from .engine import RuleEngine, RuleMatch
from .state import WorkflowState
from .runner import AgentRunner
from .ui import WorkflowUI


def load_config(config_path: Path) -> Dict[str, Any]:
    """Load workflow configuration from JSON file."""
    if not config_path.exists():
        raise FileNotFoundError(f"Workflow config not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


class WorkflowOrchestrator:
    """Main orchestrator class that runs the workflow."""

    AVAILABLE_AGENTS = [
        "task-manager",
        "architect",
        "designer",
        "code-writer",
        "code-editor",
        "code-reviewer",
        "tester",
        "devops",
    ]

    def __init__(
        self,
        project_dir: Path,
        config: Dict[str, Any],
        mock: bool = False,
        verbose: bool = False,
    ):
        self.project_dir = project_dir
        self.config = config.get("workflow", config)
        self.mock = mock
        self.verbose = verbose

        protocol_config = self.config.get("protocol", {})
        limits_config = self.config.get("limits", {})
        rules = self.config.get("rules", [])
        injection_config = self.config.get("prompt_injection", {})

        self.parser = StatusParser(protocol_config)
        self.injector = PromptInjector(enabled=injection_config.get("enabled", True))
        self.engine = RuleEngine(rules)
        self.state = WorkflowState(limits_config)
        self.runner = AgentRunner(
            project_dir=project_dir,
            mock=mock,
            verbose=verbose,
            timeout=limits_config.get("agent_timeout_seconds", 300),
        )
        self.ui = WorkflowUI(use_colors=True)

    async def run(self, initial_prompt: str) -> bool:
        mode_str = "MOCK MODE" if self.mock else "SDK MODE"
        self.ui.print_header(f"OPENSPEC-QT WORKFLOW ORCHESTRATOR ({mode_str})")

        session_file = self.project_dir / ".claude" / "session-state.json"
        session_file_exists = session_file.exists()

        if session_file_exists:
            self.ui.print_info("Session state detected - checking for restore...")

        initial_rule = self.engine.find_initial(
            context=initial_prompt,
            session_file_exists=session_file_exists
        )
        if not initial_rule:
            self.ui.print_error("No initial rule found in workflow.json")
            return False

        current_agent = initial_rule.get("action", {}).get("agent", "task-manager")
        current_prompt = initial_prompt
        current_rule_id = initial_rule.get("id", "initial")

        try:
            while True:
                if self.state.is_at_limit():
                    if not self.ui.ask_continue_after_limit("Max iterations reached"):
                        self.state.failed = True
                        break

                if self.state.is_in_loop():
                    if not self.ui.ask_continue_after_limit("Loop detected"):
                        self.state.failed = True
                        break

                self.state.iteration += 1
                self.ui.print_iteration(self.state.iteration, current_agent, self.mock)

                full_prompt = self.injector.inject(current_prompt)

                if self.verbose:
                    print(f"  Prompt: {current_prompt[:100]}...")

                start_time = time.time()
                output = await self.runner.run(current_agent, full_prompt)
                duration = time.time() - start_time

                if self.verbose:
                    self.ui.print_output_preview(output)

                status = self.parser.parse(output)
                self.ui.print_status(status.status, status.context, status.source)

                self.state.iteration -= 1
                self.state.record(
                    agent=current_agent,
                    prompt=current_prompt,
                    status=status,
                    duration=duration,
                    rule_id=current_rule_id,
                )

                if status.status == "FAILED":
                    self.ui.print_error(f"Agent failed: {status.context}")
                    self.state.failed = True
                    break

                if status.status == "UNKNOWN":
                    result = self.ui.ask_fallback(self.AVAILABLE_AGENTS)
                    if result is None:
                        break
                    current_agent, current_prompt = result
                    current_rule_id = "manual"
                    continue

                match = self.engine.match(current_agent, status)

                if not match:
                    self.ui.print_no_match()
                    result = self.ui.ask_fallback(self.AVAILABLE_AGENTS)
                    if result is None:
                        break
                    current_agent, current_prompt = result
                    current_rule_id = "manual"
                    continue

                self.ui.print_rule_match(match.rule_id, match.rule.get("description", ""))

                action = match.action

                if action.get("type") == "complete":
                    self.ui.print_complete(action.get("message", "Workflow complete!"))
                    self.state.complete = True
                    break

                if action.get("type") == "decision":
                    choice = self.ui.ask_decision(
                        action.get("message", "Choose next action:"),
                        action.get("options", []),
                    )
                    if choice is None:
                        break

                    current_agent = choice.get("agent", "task-manager")
                    prompt_template = action.get("prompt_template", "{context}")
                    current_prompt = prompt_template.replace("{context}", status.context)
                    current_rule_id = match.rule_id + "_decision"
                    continue

                if match.has_retry:
                    if not self.state.can_retry(match.rule_id, match.max_retries):
                        retry_config = match.rule.get("retry", {})
                        on_exhausted = retry_config.get("on_exhausted", {})

                        if on_exhausted.get("type") == "ask_user":
                            self.ui.print_error(on_exhausted.get("message", "Retry limit reached"))
                            result = self.ui.ask_fallback(self.AVAILABLE_AGENTS)
                            if result is None:
                                break
                            current_agent, current_prompt = result
                            current_rule_id = "manual"
                            continue
                        else:
                            self.state.failed = True
                            break

                    self.state.increment_retry(match.rule_id)

                current_agent = action.get("agent", current_agent)
                prompt_template = action.get("prompt", "Continue workflow")
                current_prompt = prompt_template.replace("{context}", status.context)
                current_rule_id = match.rule_id

        except KeyboardInterrupt:
            print("\n")
            self.ui.print_error("Interrupted by user")
            self.state.failed = True

        print(self.state.summary())

        log_dir = self.project_dir / ".claude" / "logs"
        log_file = self.state.save_log(log_dir)
        print(f"  Log saved to: {log_file}")

        return self.state.complete


def main():
    parser = argparse.ArgumentParser(
        description="OpenSpec-Qt Workflow Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python -m orchestrator.main "new task - user service"
    python -m orchestrator.main --mock "test task"
    python -m orchestrator.main --verbose --mock "test"
        """,
    )

    parser.add_argument("prompt", nargs="?", help="Initial task description")
    parser.add_argument("--mock", action="store_true", help="Use mock mode")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--config", type=Path, default=None, help="Path to workflow.json")
    parser.add_argument("--project-dir", type=Path, default=None, help="Project directory")

    args = parser.parse_args()

    if args.project_dir:
        project_dir = args.project_dir.resolve()
    else:
        cwd = Path.cwd()
        if (cwd / ".claude").exists():
            project_dir = cwd
        elif (cwd.parent / ".claude").exists():
            project_dir = cwd.parent
        else:
            project_dir = cwd

    if args.config:
        config_path = args.config
    else:
        config_path = project_dir / ".claude" / "workflow.json"

    if args.prompt:
        prompt = args.prompt
    else:
        try:
            prompt = input("Task description: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled.")
            sys.exit(1)

        if not prompt:
            print("Error: No task description provided")
            sys.exit(1)

    try:
        config = load_config(config_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing workflow.json: {e}")
        sys.exit(1)

    orchestrator = WorkflowOrchestrator(
        project_dir=project_dir,
        config=config,
        mock=args.mock,
        verbose=args.verbose,
    )

    success = asyncio.run(orchestrator.run(prompt))
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
