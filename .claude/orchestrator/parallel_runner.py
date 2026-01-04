"""
Parallel Runner - Concurrent agent execution with git worktree isolation.

Handles:
- Task dependency analysis
- Parallel agent execution via asyncio
- Git worktree-based code isolation
- Result merging and conflict detection
"""

import asyncio
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

from .runner import AgentRunner
from .worktree_manager import WorktreeManager, WorktreeInfo, MergeResult

logger = logging.getLogger(__name__)


@dataclass
class TaskNode:
    """Task node for dependency graph"""
    id: str
    agent: str
    prompt: str
    files: set[str] = field(default_factory=set)  # Expected modified files
    depends_on: list[str] = field(default_factory=list)
    status: str = "pending"  # pending, running, completed, failed, skipped

    def __hash__(self):
        return hash(self.id)


@dataclass
class AgentTask:
    """Task for a single agent execution"""
    id: str
    agent: str
    prompt: str
    worktree: Optional[WorktreeInfo] = None
    change_id: str = ""


@dataclass
class AgentResult:
    """Result of agent execution"""
    task_id: str
    agent: str
    success: bool
    output: str
    duration_seconds: float
    worktree_branch: Optional[str] = None
    error: Optional[str] = None


@dataclass
class ParallelExecutionResult:
    """Result of parallel execution"""
    success: bool
    results: list[AgentResult]
    merge_results: list[MergeResult] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)
    total_duration_seconds: float = 0.0


class DependencyGraph:
    """Task dependency graph for parallel execution planning"""

    def __init__(self):
        self.nodes: dict[str, TaskNode] = {}
        self.edges: dict[str, list[str]] = {}  # child -> parents

    def add_task(self, task: TaskNode) -> None:
        """Add a task to the graph"""
        self.nodes[task.id] = task
        self.edges[task.id] = task.depends_on.copy()

    def remove_task(self, task_id: str) -> None:
        """Remove a task from the graph"""
        self.nodes.pop(task_id, None)
        self.edges.pop(task_id, None)
        # Remove from dependencies
        for deps in self.edges.values():
            if task_id in deps:
                deps.remove(task_id)

    def get_ready_tasks(self) -> list[TaskNode]:
        """Get tasks that are ready to execute (no pending dependencies)"""
        ready = []
        for task_id, task in self.nodes.items():
            if task.status != "pending":
                continue
            deps = self.edges.get(task_id, [])
            # Check all dependencies are completed
            all_deps_done = all(
                self.nodes.get(dep_id, TaskNode(id=dep_id, agent="")).status == "completed"
                for dep_id in deps
            )
            if all_deps_done:
                ready.append(task)
        return ready

    def get_parallel_groups(self) -> list[list[TaskNode]]:
        """
        Get groups of tasks that can run in parallel.

        Returns list of lists, where each inner list contains tasks
        that can run concurrently.
        """
        groups = []
        remaining = set(self.nodes.keys())
        completed = set()

        while remaining:
            # Find tasks with all dependencies completed
            ready = []
            for task_id in remaining:
                task = self.nodes[task_id]
                deps = self.edges.get(task_id, [])
                if all(dep_id in completed for dep_id in deps):
                    ready.append(task)

            if not ready:
                # Circular dependency or error
                logger.error(f"Circular dependency detected. Remaining: {remaining}")
                break

            # Check for file conflicts within the group
            ready = self._resolve_file_conflicts(ready)

            groups.append(ready)
            for task in ready:
                remaining.discard(task.id)
                completed.add(task.id)

        return groups

    def _resolve_file_conflicts(self, tasks: list[TaskNode]) -> list[TaskNode]:
        """
        Remove tasks with file conflicts from parallel group.

        Tasks with overlapping files must run sequentially.
        """
        if len(tasks) <= 1:
            return tasks

        resolved = [tasks[0]]
        used_files = tasks[0].files.copy()

        for task in tasks[1:]:
            if task.files & used_files:
                # Conflict - this task must wait
                logger.info(
                    f"File conflict: {task.id} conflicts with previous tasks. "
                    f"Overlapping files: {task.files & used_files}"
                )
                # Don't add to this group - will be in next group
            else:
                resolved.append(task)
                used_files |= task.files

        return resolved

    def detect_file_conflicts(self, tasks: list[TaskNode]) -> list[tuple[str, str, set[str]]]:
        """
        Detect potential file conflicts between tasks.

        Returns list of (task1_id, task2_id, overlapping_files) tuples.
        """
        conflicts = []
        task_list = list(tasks)
        for i, t1 in enumerate(task_list):
            for t2 in task_list[i+1:]:
                overlap = t1.files & t2.files
                if overlap:
                    conflicts.append((t1.id, t2.id, overlap))
        return conflicts

    def topological_sort(self) -> list[TaskNode]:
        """Return tasks in topological order"""
        result = []
        visited = set()
        temp_visited = set()

        def visit(task_id: str):
            if task_id in temp_visited:
                raise ValueError(f"Circular dependency detected at {task_id}")
            if task_id in visited:
                return
            temp_visited.add(task_id)
            for dep_id in self.edges.get(task_id, []):
                if dep_id in self.nodes:
                    visit(dep_id)
            temp_visited.remove(task_id)
            visited.add(task_id)
            result.append(self.nodes[task_id])

        for task_id in self.nodes:
            if task_id not in visited:
                visit(task_id)

        return result


class ParallelRunner:
    """Execute multiple agents in parallel using git worktrees"""

    def __init__(
        self,
        project_dir: Path,
        runner: AgentRunner,
        worktree_manager: Optional[WorktreeManager] = None,
        max_parallel: int = 4,
    ):
        """
        Initialize parallel runner.

        Args:
            project_dir: Project root directory
            runner: AgentRunner instance for executing agents
            worktree_manager: WorktreeManager instance (created if None)
            max_parallel: Maximum concurrent agent executions
        """
        self.project_dir = project_dir
        self.runner = runner
        self.worktree_manager = worktree_manager or WorktreeManager(project_dir)
        self.max_parallel = max_parallel

    async def run_parallel(
        self,
        tasks: list[AgentTask],
        change_id: str,
        base_branch: str = "HEAD"
    ) -> ParallelExecutionResult:
        """
        Execute tasks in parallel with worktree isolation.

        Args:
            tasks: List of agent tasks to execute
            change_id: OpenSpec change ID for branch naming
            base_branch: Base branch to create worktrees from

        Returns:
            ParallelExecutionResult with all results and merge status
        """
        start_time = datetime.now()
        results: list[AgentResult] = []
        merge_results: list[MergeResult] = []
        conflicts: list[str] = []

        if not tasks:
            return ParallelExecutionResult(
                success=True,
                results=[],
                total_duration_seconds=0.0
            )

        # Limit parallel execution
        semaphore = asyncio.Semaphore(self.max_parallel)

        async def run_task(task: AgentTask) -> AgentResult:
            async with semaphore:
                return await self._execute_task(task, change_id, base_branch)

        try:
            # Execute all tasks concurrently
            results = await asyncio.gather(
                *[run_task(task) for task in tasks],
                return_exceptions=True
            )

            # Handle exceptions
            final_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    final_results.append(AgentResult(
                        task_id=tasks[i].id,
                        agent=tasks[i].agent,
                        success=False,
                        output="",
                        duration_seconds=0.0,
                        error=str(result)
                    ))
                else:
                    final_results.append(result)

            results = final_results

            # Merge successful results
            successful_branches = [
                r.worktree_branch for r in results
                if r.success and r.worktree_branch
            ]

            for branch in successful_branches:
                merge_result = self.worktree_manager.merge_to_branch(
                    source_branch=branch,
                    target_branch=base_branch
                )
                merge_results.append(merge_result)
                if not merge_result.success and merge_result.conflicts:
                    conflicts.extend(merge_result.conflicts)

        finally:
            # Cleanup worktrees
            for task in tasks:
                self.worktree_manager.delete_worktree(task.agent, force=True)

        total_duration = (datetime.now() - start_time).total_seconds()
        all_success = all(r.success for r in results) and not conflicts

        return ParallelExecutionResult(
            success=all_success,
            results=results,
            merge_results=merge_results,
            conflicts=conflicts,
            total_duration_seconds=total_duration
        )

    async def _execute_task(
        self,
        task: AgentTask,
        change_id: str,
        base_branch: str
    ) -> AgentResult:
        """Execute a single task in its own worktree"""
        start_time = datetime.now()

        # Create worktree
        worktree = self.worktree_manager.create_worktree(
            agent=task.agent,
            change_id=change_id,
            base_branch=base_branch
        )

        if not worktree:
            return AgentResult(
                task_id=task.id,
                agent=task.agent,
                success=False,
                output="",
                duration_seconds=0.0,
                error="Failed to create worktree"
            )

        try:
            # Update task with worktree info
            task.worktree = worktree

            # Build prompt with worktree context
            full_prompt = self._build_worktree_prompt(task, worktree)

            # Execute agent
            output = await self.runner.run(task.agent, full_prompt)

            duration = (datetime.now() - start_time).total_seconds()

            # Check for success in output
            success = self._check_success(output)

            return AgentResult(
                task_id=task.id,
                agent=task.agent,
                success=success,
                output=output,
                duration_seconds=duration,
                worktree_branch=worktree.branch
            )

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            logger.error(f"Task {task.id} failed: {e}")
            return AgentResult(
                task_id=task.id,
                agent=task.agent,
                success=False,
                output="",
                duration_seconds=duration,
                worktree_branch=worktree.branch,
                error=str(e)
            )

    def _build_worktree_prompt(self, task: AgentTask, worktree: WorktreeInfo) -> str:
        """Build prompt with worktree context"""
        return f"""[PARALLEL EXECUTION MODE]

Working Directory: {worktree.path}
Branch: {worktree.branch}

IMPORTANT:
- You are running in an isolated worktree
- Make all changes within this directory
- Commit your changes before completing

---

{task.prompt}"""

    def _check_success(self, output: str) -> bool:
        """Check if agent output indicates success"""
        if "[WORKFLOW_STATUS]" in output:
            if "status: READY" in output:
                return True
            if "status: BLOCKED" in output or "status: FAILED" in output:
                return False
        # Default to success if no clear indicator
        return True

    async def run_dependency_graph(
        self,
        graph: DependencyGraph,
        change_id: str,
        base_branch: str = "HEAD"
    ) -> ParallelExecutionResult:
        """
        Execute tasks according to dependency graph.

        Runs tasks in parallel groups, where each group contains
        tasks that can run concurrently.

        Args:
            graph: DependencyGraph with tasks and dependencies
            change_id: OpenSpec change ID
            base_branch: Base branch for worktrees

        Returns:
            Combined ParallelExecutionResult
        """
        start_time = datetime.now()
        all_results: list[AgentResult] = []
        all_merge_results: list[MergeResult] = []
        all_conflicts: list[str] = []

        groups = graph.get_parallel_groups()

        for group_idx, group in enumerate(groups):
            logger.info(f"Executing parallel group {group_idx + 1}/{len(groups)}: "
                       f"{[t.agent for t in group]}")

            # Convert TaskNodes to AgentTasks
            agent_tasks = [
                AgentTask(
                    id=task.id,
                    agent=task.agent,
                    prompt=task.prompt,
                    change_id=change_id
                )
                for task in group
            ]

            # Execute group
            result = await self.run_parallel(agent_tasks, change_id, base_branch)

            # Update task statuses
            for agent_result in result.results:
                task = graph.nodes.get(agent_result.task_id)
                if task:
                    task.status = "completed" if agent_result.success else "failed"

            all_results.extend(result.results)
            all_merge_results.extend(result.merge_results)
            all_conflicts.extend(result.conflicts)

            # Stop if any task failed
            if not result.success:
                logger.warning(f"Group {group_idx + 1} had failures. "
                             f"Remaining groups will be skipped.")
                # Mark remaining tasks as skipped
                for remaining_group in groups[group_idx + 1:]:
                    for task in remaining_group:
                        task.status = "skipped"
                break

        total_duration = (datetime.now() - start_time).total_seconds()
        all_success = all(r.success for r in all_results) and not all_conflicts

        return ParallelExecutionResult(
            success=all_success,
            results=all_results,
            merge_results=all_merge_results,
            conflicts=all_conflicts,
            total_duration_seconds=total_duration
        )


class TaskParser:
    """Parse task definitions from tasks.md files"""

    # Agent dependency chains (always sequential)
    AGENT_CHAINS = {
        "code-writer": ["code-reviewer"],
        "cpp-builder": ["tester"],
    }

    @staticmethod
    def parse_tasks_md(content: str) -> list[TaskNode]:
        """
        Parse tasks.md content into TaskNode list.

        Args:
            content: Contents of tasks.md file

        Returns:
            List of TaskNode objects
        """
        tasks = []
        current_phase = ""
        phase_tasks: dict[str, list[str]] = {}

        lines = content.split("\n")

        for line in lines:
            line = line.strip()

            # Phase header
            if line.startswith("## Phase"):
                current_phase = line.replace("## ", "").split(":")[0].strip()
                phase_tasks[current_phase] = []

            # Task item (unchecked)
            elif line.startswith("- [ ]"):
                task_text = line[5:].strip()
                task_id = task_text.split(" ")[0]

                # Determine agent from task content
                agent = TaskParser._infer_agent(task_text)

                task = TaskNode(
                    id=f"{current_phase}/{task_id}",
                    agent=agent,
                    prompt=task_text,
                    files=TaskParser._infer_files(task_text)
                )

                # Add phase dependency
                if current_phase and phase_tasks.get(current_phase):
                    # Depend on last task in same phase
                    prev_task_id = phase_tasks[current_phase][-1]
                    task.depends_on.append(prev_task_id)

                phase_tasks.setdefault(current_phase, []).append(task.id)
                tasks.append(task)

        return tasks

    @staticmethod
    def _infer_agent(task_text: str) -> str:
        """Infer agent type from task description"""
        text_lower = task_text.lower()

        if any(k in text_lower for k in ["설계", "design", "아키텍처"]):
            return "architect"
        if any(k in text_lower for k in ["구현", "작성", "생성", "implement", "create"]):
            return "code-writer"
        if any(k in text_lower for k in ["수정", "fix", "refactor", "변경"]):
            return "code-editor"
        if any(k in text_lower for k in ["리뷰", "review", "검토"]):
            return "code-reviewer"
        if any(k in text_lower for k in ["빌드", "build", "cmake"]):
            return "cpp-builder"
        if any(k in text_lower for k in ["테스트", "test", "검증"]):
            return "tester"
        if any(k in text_lower for k in ["ui", "ux", "화면"]):
            return "designer"
        if any(k in text_lower for k in ["ci", "cd", "pipeline", "deploy"]):
            return "devops"

        return "task-manager"

    @staticmethod
    def _infer_files(task_text: str) -> set[str]:
        """Infer expected modified files from task description"""
        files = set()

        # Simple pattern matching for common file references
        patterns = [
            r'(\w+\.(?:cpp|h|hpp|qml|py|json|md|yml|yaml))',
            r'(src/\S+)',
            r'(\.claude/\S+)',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, task_text)
            files.update(matches)

        return files
