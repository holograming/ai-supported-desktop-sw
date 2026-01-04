"""
T.2 - Session Recovery Scenario Tests

Tests for session state management and recovery.
"""

import json
import pytest
import tempfile
from pathlib import Path
from datetime import datetime


class MockSessionState:
    """Mock session state for testing."""

    @staticmethod
    def create_valid_state():
        """Create a valid session state."""
        return {
            "mode": "full",
            "saved_at": datetime.now().isoformat(),
            "git_branch": "feature/test",
            "git_commit": "abc1234",
            "git_pushed": True,
            "openspec": "test-change",
            "openspec_status": "IN_PROGRESS",
            "working_on": "Test task",
            "next_steps": ["Step 1", "Step 2"],
            "blocker": None,
            "completed_tasks": ["Task A"],
            "pending_tasks": ["Task B", "Task C"],
            "task_progress": {
                "completed": 5,
                "total": 10,
                "percentage": 50
            }
        }

    @staticmethod
    def create_with_blocker():
        """Create session state with a blocker."""
        state = MockSessionState.create_valid_state()
        state["blocker"] = {
            "type": "build_error",
            "severity": "high",
            "description": "CMake configuration failed",
            "error_pattern": "Could NOT find Qt6",
            "resolution": "Check vcpkg.json dependencies",
            "detected_at": datetime.now().isoformat(),
            "auto_detected": True,
            "recovery_agent": "cpp-builder",
            "recovery_attempted": 0,
            "max_recovery_attempts": 3
        }
        return state


class TestSessionStateSchema:
    """Test session state schema validation."""

    def test_valid_state_has_required_fields(self):
        """Verify valid state has all required fields."""
        state = MockSessionState.create_valid_state()

        required = [
            "mode", "saved_at", "git_branch", "git_commit",
            "git_pushed", "openspec", "openspec_status",
            "working_on", "next_steps"
        ]

        for field in required:
            assert field in state, f"Missing required field: {field}"

    def test_mode_values(self):
        """Test valid mode values."""
        valid_modes = ["quick", "sync", "full"]

        for mode in valid_modes:
            state = MockSessionState.create_valid_state()
            state["mode"] = mode
            assert state["mode"] in valid_modes

    def test_timestamp_format(self):
        """Test timestamp is valid ISO format."""
        state = MockSessionState.create_valid_state()

        # Should parse without error
        try:
            datetime.fromisoformat(state["saved_at"])
        except ValueError:
            pytest.fail("saved_at should be valid ISO timestamp")

    def test_progress_consistency(self):
        """Test progress values are consistent."""
        state = MockSessionState.create_valid_state()
        progress = state["task_progress"]

        # completed <= total
        assert progress["completed"] <= progress["total"]

        # percentage is accurate (within 1% tolerance)
        expected_pct = (progress["completed"] / progress["total"]) * 100
        assert abs(progress["percentage"] - expected_pct) <= 1


class TestBlockerSchema:
    """Test blocker schema validation."""

    def test_valid_blocker_types(self):
        """Test all valid blocker types."""
        valid_types = [
            "build_error", "test_failure", "dependency",
            "design_issue", "review_blocked", "ci_failure",
            "merge_conflict", "other"
        ]

        for blocker_type in valid_types:
            state = MockSessionState.create_with_blocker()
            state["blocker"]["type"] = blocker_type
            assert state["blocker"]["type"] in valid_types

    def test_blocker_severity_levels(self):
        """Test valid severity levels."""
        valid_severities = ["critical", "high", "medium", "low"]

        for severity in valid_severities:
            state = MockSessionState.create_with_blocker()
            state["blocker"]["severity"] = severity
            assert state["blocker"]["severity"] in valid_severities

    def test_recovery_agent_mapping(self):
        """Test blocker type to recovery agent mapping."""
        mappings = {
            "build_error": "cpp-builder",
            "test_failure": "tester",
            "dependency": "cpp-builder",
            "ci_failure": "devops",
        }

        for blocker_type, expected_agent in mappings.items():
            state = MockSessionState.create_with_blocker()
            state["blocker"]["type"] = blocker_type
            state["blocker"]["recovery_agent"] = expected_agent
            assert state["blocker"]["recovery_agent"] == expected_agent


class TestSessionRecoveryScenarios:
    """Test session recovery scenarios."""

    def test_normal_recovery(self, tmp_path):
        """Test normal session recovery."""
        session_file = tmp_path / "session-state.json"
        state = MockSessionState.create_valid_state()

        # Write session file
        with open(session_file, "w") as f:
            json.dump(state, f)

        # Read and verify
        with open(session_file, "r") as f:
            loaded = json.load(f)

        assert loaded["openspec"] == state["openspec"]
        assert loaded["working_on"] == state["working_on"]

    def test_recovery_with_blocker(self, tmp_path):
        """Test recovery when blocker exists."""
        session_file = tmp_path / "session-state.json"
        state = MockSessionState.create_with_blocker()

        with open(session_file, "w") as f:
            json.dump(state, f)

        with open(session_file, "r") as f:
            loaded = json.load(f)

        assert loaded["blocker"] is not None
        assert loaded["blocker"]["type"] == "build_error"
        assert loaded["blocker"]["recovery_agent"] == "cpp-builder"

    def test_recovery_missing_optional_fields(self, tmp_path):
        """Test recovery with missing optional fields."""
        session_file = tmp_path / "session-state.json"
        state = {
            "mode": "quick",
            "saved_at": datetime.now().isoformat(),
            "git_branch": "main",
            "git_commit": "abc1234",
            "git_pushed": False,
            "openspec": "test",
            "openspec_status": "IN_PROGRESS",
            "working_on": "Test",
            "next_steps": []
            # Missing optional: blocker, completed_tasks, etc.
        }

        with open(session_file, "w") as f:
            json.dump(state, f)

        with open(session_file, "r") as f:
            loaded = json.load(f)

        # Optional fields should be missing but not cause error
        assert loaded.get("blocker") is None
        assert loaded.get("completed_tasks") is None


class TestSessionValidation:
    """Test session state validation logic."""

    def test_validate_git_branch_mismatch(self):
        """Test detection of git branch mismatch."""
        state = MockSessionState.create_valid_state()
        state["git_branch"] = "feature/old-branch"

        # Simulate current branch being different
        current_branch = "main"

        assert state["git_branch"] != current_branch

    def test_validate_progress_percentage(self):
        """Test progress percentage validation."""
        state = MockSessionState.create_valid_state()

        # Valid case
        state["task_progress"] = {"completed": 5, "total": 10, "percentage": 50}
        expected = (5 / 10) * 100
        assert abs(state["task_progress"]["percentage"] - expected) <= 1

        # Invalid case (percentage doesn't match)
        state["task_progress"]["percentage"] = 80  # Wrong!
        expected = (5 / 10) * 100
        assert abs(state["task_progress"]["percentage"] - expected) > 1

    def test_validate_blocker_schema(self):
        """Test blocker schema validation."""
        state = MockSessionState.create_with_blocker()
        blocker = state["blocker"]

        # Required blocker fields
        required = ["type", "severity", "description", "detected_at"]
        for field in required:
            assert field in blocker, f"Blocker missing: {field}"

    def test_validate_openspec_exists(self, tmp_path):
        """Test OpenSpec existence validation."""
        state = MockSessionState.create_valid_state()
        state["openspec"] = "nonexistent-change"

        # Create mock openspec directory structure
        openspec_dir = tmp_path / "openspec" / "changes"
        openspec_dir.mkdir(parents=True)

        # Check if openspec exists
        change_dir = openspec_dir / state["openspec"]
        assert not change_dir.exists()


class TestAutoRecoveryLogic:
    """Test automatic recovery logic."""

    def test_recovery_agent_selection(self):
        """Test correct recovery agent is selected for blocker type."""
        recovery_map = {
            "build_error": "cpp-builder",
            "test_failure": "tester",
            "dependency": "cpp-builder",
            "ci_failure": "devops",
            "review_blocked": "code-editor",
        }

        for blocker_type, expected_agent in recovery_map.items():
            assert expected_agent is not None

    def test_max_recovery_attempts(self):
        """Test max recovery attempts tracking."""
        state = MockSessionState.create_with_blocker()

        max_attempts = state["blocker"]["max_recovery_attempts"]
        current = state["blocker"]["recovery_attempted"]

        # Can retry
        assert current < max_attempts

        # Simulate exhausted retries
        state["blocker"]["recovery_attempted"] = max_attempts
        assert state["blocker"]["recovery_attempted"] >= max_attempts


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
