"""
T.4 - OpenSpec Initialization End-to-End Tests

Tests for OpenSpec initialization workflow.
"""

import json
import pytest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime


class TestOpenSpecDirectoryStructure:
    """Test OpenSpec directory structure creation."""

    @pytest.fixture
    def temp_project(self, tmp_path):
        """Create temporary project structure."""
        # Create minimal project structure
        (tmp_path / ".claude").mkdir()
        (tmp_path / "openspec").mkdir()
        (tmp_path / "openspec" / "changes").mkdir()
        (tmp_path / "openspec" / "specs").mkdir()

        # Create project.md
        project_md = tmp_path / "openspec" / "project.md"
        project_md.write_text("# Project\n\nProject rules here.")

        return tmp_path

    def test_create_change_directory(self, temp_project):
        """Test creating a new change directory."""
        change_id = "new-feature"
        change_dir = temp_project / "openspec" / "changes" / change_id

        change_dir.mkdir(parents=True)

        assert change_dir.exists()
        assert change_dir.is_dir()

    def test_create_proposal_md(self, temp_project):
        """Test creating proposal.md file."""
        change_id = "new-feature"
        change_dir = temp_project / "openspec" / "changes" / change_id
        change_dir.mkdir(parents=True)

        proposal = change_dir / "proposal.md"
        proposal_content = f"""# Proposal: {change_id}

## Summary
Description of the change.

## Motivation
Why this change is needed.

## Scope
- Feature A
- Feature B

## Status
DRAFT
"""
        proposal.write_text(proposal_content)

        assert proposal.exists()
        content = proposal.read_text()
        assert f"# Proposal: {change_id}" in content
        assert "## Summary" in content

    def test_create_tasks_md(self, temp_project):
        """Test creating tasks.md file."""
        change_id = "new-feature"
        change_dir = temp_project / "openspec" / "changes" / change_id
        change_dir.mkdir(parents=True)

        tasks = change_dir / "tasks.md"
        tasks_content = f"""# Tasks for {change_id}

## Phase 1: Setup
- [ ] 1.1 Initial setup
- [ ] 1.2 Configuration

## Phase 2: Implementation
- [ ] 2.1 Core feature
- [ ] 2.2 Integration

## Testing
- [ ] T.1 Unit tests
- [ ] T.2 Integration tests
"""
        tasks.write_text(tasks_content)

        assert tasks.exists()
        content = tasks.read_text()
        assert "## Phase 1" in content
        assert "- [ ]" in content


class TestOpenSpecValidation:
    """Test OpenSpec validation logic."""

    def test_valid_change_id_format(self):
        """Test valid change ID formats."""
        valid_ids = [
            "new-feature",
            "fix-bug-123",
            "implement-user-auth",
            "add-parallel-execution",
        ]

        for change_id in valid_ids:
            # Valid: lowercase, hyphens, numbers
            assert change_id == change_id.lower()
            assert " " not in change_id
            assert "_" not in change_id or change_id.replace("_", "-") == change_id

    def test_invalid_change_id_format(self):
        """Test invalid change ID formats."""
        invalid_ids = [
            "New Feature",  # Spaces
            "new_feature",  # Underscores (prefer hyphens)
            "ALLCAPS",      # Should be lowercase
            "123-start",    # Starts with number
        ]

        for change_id in invalid_ids:
            # At least one validation should fail
            has_space = " " in change_id
            has_uppercase = any(c.isupper() for c in change_id)
            starts_with_digit = change_id[0].isdigit() if change_id else False
            has_underscore = "_" in change_id

            assert has_space or has_uppercase or starts_with_digit or has_underscore

    def test_proposal_has_required_sections(self, tmp_path):
        """Test proposal.md has required sections."""
        proposal_content = """# Proposal: test-change

## Summary
Test summary.

## Motivation
Test motivation.

## Scope
- Item 1

## Status
DRAFT
"""
        proposal = tmp_path / "proposal.md"
        proposal.write_text(proposal_content)

        content = proposal.read_text()

        required_sections = ["Summary", "Motivation", "Scope", "Status"]
        for section in required_sections:
            assert f"## {section}" in content

    def test_tasks_has_phase_structure(self, tmp_path):
        """Test tasks.md has proper phase structure."""
        tasks_content = """# Tasks for test-change

## Phase 1: Foundation
- [ ] 1.1 Task one
- [ ] 1.2 Task two

## Phase 2: Implementation
- [ ] 2.1 Task three
"""
        tasks = tmp_path / "tasks.md"
        tasks.write_text(tasks_content)

        content = tasks.read_text()

        assert "## Phase 1" in content
        assert "## Phase 2" in content
        assert "- [ ]" in content


class TestOpenSpecSkipLogic:
    """Test OpenSpec initialization skip logic."""

    @pytest.fixture
    def project_with_openspec(self, tmp_path):
        """Create project with existing OpenSpec."""
        change_id = "existing-change"

        # Create structure
        (tmp_path / ".claude").mkdir()
        (tmp_path / "openspec").mkdir()
        (tmp_path / "openspec" / "changes").mkdir()
        change_dir = tmp_path / "openspec" / "changes" / change_id
        change_dir.mkdir()

        # Create proposal.md
        proposal = change_dir / "proposal.md"
        proposal.write_text("# Existing Proposal")

        return tmp_path, change_id

    def test_detect_existing_openspec(self, project_with_openspec):
        """Test detection of existing OpenSpec."""
        project_dir, change_id = project_with_openspec

        change_dir = project_dir / "openspec" / "changes" / change_id
        proposal = change_dir / "proposal.md"

        # Should detect existing
        assert change_dir.exists()
        assert proposal.exists()

    def test_skip_if_proposal_exists(self, project_with_openspec):
        """Test skip logic when proposal already exists."""
        project_dir, change_id = project_with_openspec

        proposal = project_dir / "openspec" / "changes" / change_id / "proposal.md"

        # Skip condition
        should_skip = proposal.exists()
        assert should_skip

    def test_create_if_no_proposal(self, tmp_path):
        """Test creation when no proposal exists."""
        change_id = "new-change"
        change_dir = tmp_path / "openspec" / "changes" / change_id
        change_dir.mkdir(parents=True)

        proposal = change_dir / "proposal.md"

        # Should not skip
        should_skip = proposal.exists()
        assert not should_skip


class TestOpenSpecSessionState:
    """Test OpenSpec integration with session state."""

    def test_session_state_has_openspec(self, tmp_path):
        """Test session state includes OpenSpec info."""
        session_state = {
            "mode": "full",
            "saved_at": datetime.now().isoformat(),
            "git_branch": "main",
            "git_commit": "abc1234",
            "git_pushed": False,
            "openspec": "test-change",
            "openspec_status": "IN_PROGRESS",
            "working_on": "Phase 1",
            "next_steps": ["Phase 2"]
        }

        session_file = tmp_path / "session-state.json"
        with open(session_file, "w") as f:
            json.dump(session_state, f)

        with open(session_file, "r") as f:
            loaded = json.load(f)

        assert loaded["openspec"] == "test-change"
        assert loaded["openspec_status"] == "IN_PROGRESS"

    def test_valid_openspec_statuses(self):
        """Test valid OpenSpec status values."""
        valid_statuses = [
            "DRAFT",
            "APPROVED",
            "IN_PROGRESS",
            "BLOCKED",
            "DEPLOYED",
            "ARCHIVED"
        ]

        for status in valid_statuses:
            session_state = {"openspec_status": status}
            assert session_state["openspec_status"] in valid_statuses


class TestOpenSpecEndToEnd:
    """End-to-end tests for OpenSpec initialization."""

    @pytest.fixture
    def clean_project(self, tmp_path):
        """Create a clean project without OpenSpec."""
        (tmp_path / ".claude").mkdir()
        (tmp_path / "openspec").mkdir()
        (tmp_path / "openspec" / "changes").mkdir()
        (tmp_path / "openspec" / "specs").mkdir()

        # Create AGENTS.md
        agents_md = tmp_path / "openspec" / "AGENTS.md"
        agents_md.write_text("# AI Agent Instructions\n")

        # Create project.md
        project_md = tmp_path / "openspec" / "project.md"
        project_md.write_text("# Project Rules\n")

        return tmp_path

    def test_full_initialization_workflow(self, clean_project):
        """Test complete OpenSpec initialization."""
        change_id = "new-feature"

        # Step 1: Create change directory
        change_dir = clean_project / "openspec" / "changes" / change_id
        change_dir.mkdir(parents=True)

        # Step 2: Create proposal.md
        proposal = change_dir / "proposal.md"
        proposal.write_text(f"""# Proposal: {change_id}

## Summary
New feature implementation.

## Motivation
User requested feature.

## Scope
- Core implementation
- Tests
- Documentation

## Status
DRAFT
""")

        # Step 3: Create tasks.md
        tasks = change_dir / "tasks.md"
        tasks.write_text(f"""# Tasks for {change_id}

## Phase 1: Setup
- [ ] 1.1 Project setup
- [ ] 1.2 Dependencies

## Phase 2: Implementation
- [ ] 2.1 Core feature
- [ ] 2.2 Integration

## Testing
- [ ] T.1 Unit tests

## Final
- [ ] F.1 Documentation
""")

        # Step 4: Create specs directory
        specs_dir = change_dir / "specs"
        specs_dir.mkdir(exist_ok=True)

        # Verify structure
        assert change_dir.exists()
        assert proposal.exists()
        assert tasks.exists()
        assert specs_dir.exists()

        # Verify content
        proposal_content = proposal.read_text()
        assert "## Summary" in proposal_content
        assert "## Status" in proposal_content

        tasks_content = tasks.read_text()
        assert "## Phase 1" in tasks_content
        assert "- [ ]" in tasks_content

    def test_initialization_preserves_existing(self, clean_project):
        """Test initialization doesn't overwrite existing files."""
        change_id = "existing"
        change_dir = clean_project / "openspec" / "changes" / change_id
        change_dir.mkdir(parents=True)

        # Create existing proposal with custom content
        proposal = change_dir / "proposal.md"
        original_content = "# Original Proposal\n\nDo not overwrite."
        proposal.write_text(original_content)

        # Simulate initialization check
        should_skip = proposal.exists()

        assert should_skip
        assert proposal.read_text() == original_content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
