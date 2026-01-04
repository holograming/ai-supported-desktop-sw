"""
UI module - User interaction for decisions and fallbacks.

Handles:
- Displaying decisions and getting user choice
- Fallback prompts when no rule matches
- Progress display
"""

from typing import List, Dict, Any, Optional


class WorkflowUI:
    """Handle user interaction during workflow execution."""

    # ANSI colors for terminal
    COLORS = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "dim": "\033[2m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
    }

    def __init__(self, use_colors: bool = True, use_unicode: bool = False):
        """
        Initialize UI.

        Args:
            use_colors: Whether to use ANSI colors
            use_unicode: Whether to use Unicode characters (disable on Windows)
        """
        self.use_colors = use_colors
        self.use_unicode = use_unicode

        # ASCII alternatives for Unicode characters
        self.BORDER_H = "=" if not use_unicode else "="
        self.BORDER_L = "-" if not use_unicode else "-"

    def _c(self, color: str, text: str) -> str:
        """Apply color to text if colors enabled."""
        if not self.use_colors:
            return text
        return f"{self.COLORS.get(color, '')}{text}{self.COLORS['reset']}"

    def print_header(self, title: str):
        """Print workflow header."""
        print()
        print(self._c("cyan", self.BORDER_H * 65))
        print(self._c("cyan", f"  {title}"))
        print(self._c("cyan", self.BORDER_H * 65))
        print()

    def print_iteration(self, iteration: int, agent: str, is_mock: bool = False):
        """Print iteration header."""
        mode = self._c("dim", "[MOCK]") if is_mock else ""
        print()
        print(self._c("blue", self.BORDER_L * 65))
        print(
            self._c("bold", f"[>] Iteration {iteration}: ")
            + self._c("cyan", agent)
            + f" {mode}"
        )
        print(self._c("blue", self.BORDER_L * 65))

    def print_status(self, status: str, context: str, source: str):
        """Print parsed status."""
        status_colors = {
            "READY": "green",
            "BLOCKED": "yellow",
            "FAILED": "red",
            "DECISION_NEEDED": "magenta",
            "UNKNOWN": "dim",
        }
        color = status_colors.get(status, "reset")

        status_icons = {
            "READY": "[OK]",
            "BLOCKED": "[!!]",
            "FAILED": "[XX]",
            "DECISION_NEEDED": "[??]",
            "UNKNOWN": "[..]",
        }
        icon = status_icons.get(status, "[..]")

        print()
        print(f"  {icon} " + self._c(color, f"Status: {status}") + f" (via {source})")
        if context:
            print(f"     Context: {context[:80]}{'...' if len(context) > 80 else ''}")

    def print_rule_match(self, rule_id: str, description: str = ""):
        """Print matched rule."""
        print()
        print(self._c("green", f"  [+] Matched rule: ") + self._c("bold", rule_id))
        if description:
            print(f"    {description}")

    def print_no_match(self):
        """Print no rule matched."""
        print()
        print(self._c("yellow", "  [!] No matching rule found"))

    def print_error(self, message: str):
        """Print error message."""
        print()
        print(self._c("red", f"  [X] Error: {message}"))

    def print_info(self, message: str):
        """Print info message."""
        print(self._c("cyan", f"  [i] {message}"))

    def print_complete(self, message: str):
        """Print completion message."""
        print()
        print(self._c("green", self.BORDER_H * 65))
        print(self._c("green", f"  [OK] {message}"))
        print(self._c("green", self.BORDER_H * 65))
        print()

    def ask_decision(
        self, message: str, options: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        Ask user to choose from options.

        Args:
            message: Message to display
            options: List of option dicts with 'key', 'label', 'agent'

        Returns:
            Selected option dict, or None if cancelled
        """
        print()
        print(self._c("magenta", self.BORDER_H * 65))
        print(self._c("bold", f"  [?] {message}"))
        print(self._c("magenta", self.BORDER_L * 65))

        for opt in options:
            key = opt.get("key", "?")
            label = opt.get("label", "Unknown")
            agent = opt.get("agent", "")
            print(f"    [{key}] {label}")
            if agent:
                print(self._c("dim", f"        -> {agent}"))

        print()
        print(self._c("dim", "    [q] Quit workflow"))
        print(self._c("magenta", self.BORDER_H * 65))
        print()

        while True:
            try:
                choice = input(self._c("cyan", "  Your choice: ")).strip().lower()
            except (EOFError, KeyboardInterrupt):
                print()
                return None

            if choice == "q":
                return None

            # Find matching option
            for opt in options:
                if opt.get("key", "").lower() == choice:
                    return opt

            print(self._c("yellow", f"  Invalid choice: {choice}"))

    def ask_fallback(self, available_agents: List[str]) -> Optional[tuple]:
        """
        Ask user what to do when no rule matches.

        Args:
            available_agents: List of available agent names

        Returns:
            Tuple of (agent, prompt) or None if cancelled
        """
        print()
        print(self._c("yellow", self.BORDER_H * 65))
        print(self._c("bold", "  [?] No matching rule. Choose action:"))
        print(self._c("yellow", self.BORDER_L * 65))

        for i, agent in enumerate(available_agents, 1):
            print(f"    [{i}] Run {agent}")

        print()
        print(self._c("dim", "    [q] Quit workflow"))
        print(self._c("yellow", self.BORDER_H * 65))
        print()

        while True:
            try:
                choice = input(self._c("cyan", "  Your choice: ")).strip().lower()
            except (EOFError, KeyboardInterrupt):
                print()
                return None

            if choice == "q":
                return None

            try:
                idx = int(choice) - 1
                if 0 <= idx < len(available_agents):
                    agent = available_agents[idx]
                    prompt = input(
                        self._c("cyan", f"  Prompt for {agent}: ")
                    ).strip()
                    if prompt:
                        return (agent, prompt)
                    print(self._c("yellow", "  Prompt cannot be empty"))
            except ValueError:
                pass

            print(self._c("yellow", f"  Invalid choice: {choice}"))

    def ask_continue_after_limit(self, limit_type: str) -> bool:
        """
        Ask user whether to continue after hitting a limit.

        Args:
            limit_type: Description of the limit hit

        Returns:
            True to continue, False to stop
        """
        print()
        print(self._c("yellow", self.BORDER_H * 65))
        print(self._c("bold", f"  [!] Limit reached: {limit_type}"))
        print(self._c("yellow", self.BORDER_H * 65))
        print()

        try:
            choice = input(
                self._c("cyan", "  Continue anyway? [y/N]: ")
            ).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return False

        return choice in ("y", "yes")

    def print_output_preview(self, output: str, max_lines: int = 10):
        """Print preview of agent output."""
        lines = output.strip().split("\n")

        print()
        print(self._c("dim", "  Output preview:"))

        for line in lines[:max_lines]:
            # Truncate long lines
            if len(line) > 70:
                line = line[:67] + "..."
            print(self._c("dim", f"    | {line}"))

        if len(lines) > max_lines:
            print(self._c("dim", f"    | ... ({len(lines) - max_lines} more lines)"))

    # ========================================
    # Parallel Execution UI Methods
    # ========================================

    def print_parallel_header(self, group_num: int, total_groups: int, agents: List[str]):
        """Print parallel group execution header."""
        print()
        print(self._c("magenta", self.BORDER_H * 65))
        print(self._c("bold", f"  [P] PARALLEL GROUP {group_num}/{total_groups}"))
        print(self._c("magenta", self.BORDER_L * 65))
        print(f"  Agents: {', '.join(self._c('cyan', a) for a in agents)}")
        print(self._c("magenta", self.BORDER_H * 65))
        print()

    def print_parallel_task_start(self, task_id: str, agent: str, worktree_path: str = ""):
        """Print when a parallel task starts."""
        worktree_info = f" @ {worktree_path}" if worktree_path else ""
        print(f"  [>>] " + self._c("cyan", agent) +
              self._c("dim", f" ({task_id}){worktree_info}"))

    def print_parallel_task_complete(self, task_id: str, agent: str, success: bool, duration: float):
        """Print when a parallel task completes."""
        if success:
            icon = self._c("green", "[OK]")
            status = self._c("green", "completed")
        else:
            icon = self._c("red", "[XX]")
            status = self._c("red", "failed")

        print(f"  {icon} " + self._c("cyan", agent) +
              f" {status} ({duration:.1f}s)")

    def print_parallel_summary(
        self,
        total_tasks: int,
        successful: int,
        failed: int,
        duration: float
    ):
        """Print parallel execution summary."""
        print()
        print(self._c("magenta", self.BORDER_L * 65))
        print(self._c("bold", "  [P] Parallel Execution Summary"))
        print(self._c("magenta", self.BORDER_L * 65))

        success_rate = (successful / total_tasks * 100) if total_tasks > 0 else 0

        print(f"  Total tasks:  {total_tasks}")
        print(f"  Successful:   " + self._c("green", str(successful)))
        print(f"  Failed:       " + self._c("red" if failed > 0 else "dim", str(failed)))
        print(f"  Success rate: " +
              self._c("green" if success_rate == 100 else "yellow", f"{success_rate:.0f}%"))
        print(f"  Duration:     {duration:.1f}s")
        print()

    def print_merge_status(self, branch: str, success: bool, conflicts: List[str] = None):
        """Print merge status for a branch."""
        if success:
            print(f"  " + self._c("green", "[M]") + f" Merged: {branch}")
        else:
            print(f"  " + self._c("red", "[!]") + f" Merge failed: {branch}")
            if conflicts:
                for conflict_file in conflicts[:5]:
                    print(self._c("red", f"      - {conflict_file}"))
                if len(conflicts) > 5:
                    print(self._c("dim", f"      ... and {len(conflicts) - 5} more"))

    def print_conflict_report(self, conflicts: List[Dict[str, Any]]):
        """Print detailed conflict report."""
        print()
        print(self._c("red", self.BORDER_H * 65))
        print(self._c("bold", "  MERGE CONFLICT DETECTED"))
        print(self._c("red", self.BORDER_H * 65))
        print()

        for i, conflict in enumerate(conflicts, 1):
            file_path = conflict.get("file", "unknown")
            branches = conflict.get("branches", ("?", "?"))
            conflict_type = conflict.get("type", "content")

            print(f"  {i}. {self._c('yellow', file_path)}")
            print(f"     Type: {conflict_type}")
            print(f"     Branches: {branches[0]} vs {branches[1]}")
            print()

        print(self._c("red", self.BORDER_L * 65))
        print("  Options:")
        print("    [1] Abort and rollback")
        print("    [2] Manual conflict resolution")
        print("    [3] Keep first branch changes")
        print("    [4] Keep second branch changes")
        print(self._c("red", self.BORDER_H * 65))
        print()

    def print_worktree_status(self, worktrees: List[Dict[str, str]]):
        """Print status of active worktrees."""
        print()
        print(self._c("blue", self.BORDER_L * 65))
        print(self._c("bold", "  [W] Active Worktrees"))
        print(self._c("blue", self.BORDER_L * 65))

        if not worktrees:
            print(self._c("dim", "  No active worktrees"))
        else:
            for wt in worktrees:
                agent = wt.get("agent", "unknown")
                branch = wt.get("branch", "?")
                status = wt.get("status", "unknown")

                status_colors = {
                    "created": "dim",
                    "active": "cyan",
                    "completed": "green",
                    "failed": "red",
                    "cleaned": "dim",
                }
                color = status_colors.get(status, "dim")

                print(f"    - " + self._c("cyan", agent) +
                      f": {branch} " + self._c(color, f"[{status}]"))
        print()
