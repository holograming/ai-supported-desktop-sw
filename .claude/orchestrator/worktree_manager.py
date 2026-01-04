"""
Git Worktree Manager for Parallel Agent Execution

Manages git worktrees for isolated parallel agent execution.
"""

import asyncio
import logging
import os
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def _get_max_worktrees() -> int:
    """Safely parse PARALLEL_AGENTS_MAX environment variable."""
    try:
        return int(os.environ.get("PARALLEL_AGENTS_MAX", 4))
    except ValueError:
        return 4


@dataclass
class WorktreeInfo:
    """Worktree information"""
    path: Path
    branch: str
    agent: str
    created_at: str = ""
    status: str = "created"  # created, active, completed, failed, cleaned


@dataclass
class MergeResult:
    """Merge result"""
    success: bool
    branch: str
    conflicts: list[str] = field(default_factory=list)
    message: str = ""


@dataclass
class Conflict:
    """Merge conflict information"""
    file: str
    branches: tuple[str, str]
    conflict_type: str  # content, add-add, modify-delete


class WorktreeManager:
    """Git worktree management for parallel execution"""

    WORKTREE_DIR = ".worktrees"
    MAX_WORKTREES = _get_max_worktrees()

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.worktrees_dir = project_dir / self.WORKTREE_DIR
        self.active_worktrees: dict[str, WorktreeInfo] = {}

    def _run_git(self, *args: str, cwd: Optional[Path] = None) -> subprocess.CompletedProcess:
        """Run git command"""
        cmd = ["git", *args]
        result = subprocess.run(
            cmd,
            cwd=cwd or self.project_dir,
            capture_output=True,
            text=True
        )
        return result

    def _ensure_worktrees_dir(self) -> None:
        """Ensure worktrees directory exists"""
        self.worktrees_dir.mkdir(exist_ok=True)

        # Add to gitignore if not present
        gitignore = self.project_dir / ".gitignore"
        if gitignore.exists():
            content = gitignore.read_text()
            if self.WORKTREE_DIR not in content:
                with gitignore.open("a") as f:
                    f.write(f"\n# Parallel agent worktrees\n{self.WORKTREE_DIR}/\n")

    def create_worktree(
        self,
        agent: str,
        change_id: str,
        base_branch: str = "HEAD"
    ) -> Optional[WorktreeInfo]:
        """
        Create a new worktree for parallel agent execution.

        Args:
            agent: Agent name (e.g., "code-writer")
            change_id: OpenSpec change ID
            base_branch: Base branch to create from

        Returns:
            WorktreeInfo or None if failed
        """
        if len(self.active_worktrees) >= self.MAX_WORKTREES:
            logger.error(f"Maximum worktrees ({self.MAX_WORKTREES}) reached")
            return None

        self._ensure_worktrees_dir()

        branch_name = f"parallel/{change_id}/{agent}"
        worktree_path = self.worktrees_dir / agent

        # Remove existing worktree if present
        if worktree_path.exists():
            self.delete_worktree(agent)

        # Create worktree with new branch
        result = self._run_git(
            "worktree", "add",
            str(worktree_path),
            "-b", branch_name,
            base_branch
        )

        if result.returncode != 0:
            logger.error(f"Failed to create worktree: {result.stderr}")
            return None

        info = WorktreeInfo(
            path=worktree_path,
            branch=branch_name,
            agent=agent,
            status="created"
        )
        self.active_worktrees[agent] = info
        logger.info(f"Created worktree for {agent} at {worktree_path}")
        return info

    def delete_worktree(self, agent: str, force: bool = False) -> bool:
        """
        Delete a worktree.

        Args:
            agent: Agent name
            force: Force deletion even with uncommitted changes

        Returns:
            True if successful
        """
        if agent not in self.active_worktrees:
            worktree_path = self.worktrees_dir / agent
        else:
            worktree_path = self.active_worktrees[agent].path

        if not worktree_path.exists():
            self.active_worktrees.pop(agent, None)
            return True

        # Remove worktree
        args = ["worktree", "remove", str(worktree_path)]
        if force:
            args.append("--force")

        result = self._run_git(*args)

        if result.returncode != 0:
            logger.warning(f"Failed to remove worktree normally: {result.stderr}")
            # Try force remove
            if not force:
                return self.delete_worktree(agent, force=True)
            # Last resort: manual cleanup
            try:
                shutil.rmtree(worktree_path)
                self._run_git("worktree", "prune")
            except Exception as e:
                logger.error(f"Failed to cleanup worktree: {e}")
                return False

        self.active_worktrees.pop(agent, None)
        logger.info(f"Deleted worktree for {agent}")
        return True

    def merge_to_branch(
        self,
        source_branch: str,
        target_branch: str,
        no_ff: bool = True
    ) -> MergeResult:
        """
        Merge source branch to target branch.

        Args:
            source_branch: Branch to merge from
            target_branch: Branch to merge into
            no_ff: Use --no-ff flag

        Returns:
            MergeResult
        """
        # Checkout target
        result = self._run_git("checkout", target_branch)
        if result.returncode != 0:
            return MergeResult(
                success=False,
                branch=source_branch,
                message=f"Failed to checkout {target_branch}: {result.stderr}"
            )

        # Merge
        merge_args = ["merge", source_branch]
        if no_ff:
            merge_args.append("--no-ff")
        merge_args.extend(["-m", f"Merge {source_branch} into {target_branch}"])

        result = self._run_git(*merge_args)

        if result.returncode != 0:
            # Check for conflicts
            conflicts = self._get_conflict_files()
            if conflicts:
                # Abort merge
                self._run_git("merge", "--abort")
                return MergeResult(
                    success=False,
                    branch=source_branch,
                    conflicts=conflicts,
                    message="Merge conflicts detected"
                )
            return MergeResult(
                success=False,
                branch=source_branch,
                message=f"Merge failed: {result.stderr}"
            )

        return MergeResult(
            success=True,
            branch=source_branch,
            message="Merge successful"
        )

    def _get_conflict_files(self) -> list[str]:
        """Get list of conflicted files"""
        result = self._run_git("diff", "--name-only", "--diff-filter=U")
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip().split("\n")
        return []

    def detect_conflicts(self, branches: list[str]) -> list[Conflict]:
        """
        Detect potential conflicts between branches.

        Args:
            branches: List of branch names to check

        Returns:
            List of Conflict objects
        """
        conflicts = []

        # Get modified files for each branch
        branch_files: dict[str, set[str]] = {}
        for branch in branches:
            result = self._run_git(
                "diff", "--name-only",
                f"HEAD...{branch}"
            )
            if result.returncode == 0:
                files = set(result.stdout.strip().split("\n")) if result.stdout.strip() else set()
                branch_files[branch] = files

        # Check for overlapping files
        branch_list = list(branch_files.keys())
        for i, b1 in enumerate(branch_list):
            for b2 in branch_list[i+1:]:
                overlap = branch_files[b1] & branch_files[b2]
                for file in overlap:
                    conflicts.append(Conflict(
                        file=file,
                        branches=(b1, b2),
                        conflict_type="content"  # Simplified
                    ))

        return conflicts

    def cleanup_parallel_branches(self, change_id: str) -> int:
        """
        Clean up all parallel branches for a change.

        Args:
            change_id: OpenSpec change ID

        Returns:
            Number of branches deleted
        """
        # List branches
        result = self._run_git("branch", "--list", f"parallel/{change_id}/*")
        if result.returncode != 0 or not result.stdout.strip():
            return 0

        branches = [b.strip().lstrip("* ") for b in result.stdout.strip().split("\n")]
        deleted = 0

        for branch in branches:
            result = self._run_git("branch", "-D", branch)
            if result.returncode == 0:
                deleted += 1
                logger.info(f"Deleted branch {branch}")

        return deleted

    def cleanup_all_worktrees(self) -> int:
        """
        Clean up all worktrees.

        Returns:
            Number of worktrees cleaned
        """
        cleaned = 0
        agents = list(self.active_worktrees.keys())

        for agent in agents:
            if self.delete_worktree(agent, force=True):
                cleaned += 1

        # Prune stale worktrees
        self._run_git("worktree", "prune")

        return cleaned

    def get_worktree_status(self) -> dict[str, WorktreeInfo]:
        """Get status of all active worktrees"""
        return self.active_worktrees.copy()
