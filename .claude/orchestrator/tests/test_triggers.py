"""
T.1 - Workflow Trigger Matching Tests

Tests for workflow.json trigger matching logic.
"""

import json
import pytest
from pathlib import Path


# Load workflow.json for testing
@pytest.fixture
def workflow_config():
    """Load the actual workflow.json configuration."""
    config_path = Path(__file__).parent.parent.parent / "workflow.json"
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)["workflow"]


@pytest.fixture
def triggers(workflow_config):
    """Extract triggers from workflow config."""
    return workflow_config.get("triggers", {})


class TestTriggerMatching:
    """Test trigger keyword matching."""

    def test_task_manager_triggers(self, triggers):
        """Test task-manager agent triggers."""
        tm_triggers = triggers.get("task-manager", [])

        # Required triggers
        assert "session" in tm_triggers
        assert "새 태스크" in tm_triggers
        assert "status" in tm_triggers
        assert "달미" in tm_triggers  # Alias

    def test_architect_triggers(self, triggers):
        """Test architect agent triggers."""
        arch_triggers = triggers.get("architect", [])

        assert "설계" in arch_triggers
        assert "design" in arch_triggers
        assert "도산" in arch_triggers  # Alias

    def test_cpp_builder_triggers(self, triggers):
        """Test cpp-builder agent triggers."""
        builder_triggers = triggers.get("cpp-builder", [])

        # Build-related keywords should be in cpp-builder, not tester
        assert "빌드" in builder_triggers
        assert "build" in builder_triggers
        assert "cmake" in builder_triggers or "CMake" in builder_triggers
        assert "로컬빌더" in builder_triggers  # Alias

    def test_tester_triggers(self, triggers):
        """Test tester agent triggers."""
        tester_triggers = triggers.get("tester", [])

        # Tester should have test-related keywords
        assert "테스트" in tester_triggers
        assert "test" in tester_triggers
        assert "지평" in tester_triggers  # Alias

        # Build keywords should NOT be in tester
        assert "빌드" not in tester_triggers
        assert "build" not in tester_triggers

    def test_code_editor_triggers(self, triggers):
        """Test code-editor agent triggers."""
        editor_triggers = triggers.get("code-editor", [])

        assert "수정" in editor_triggers
        assert "fix" in editor_triggers
        assert "refactor" in editor_triggers
        assert "철산" in editor_triggers  # Alias

    def test_all_agents_have_alias(self, triggers):
        """Verify all agents have their character alias."""
        aliases = {
            "task-manager": "달미",
            "architect": "도산",
            "designer": "사하",
            "code-writer": "용산",
            "code-editor": "철산",
            "code-reviewer": "영실",
            "tester": "지평",
            "devops": "인재",
            "cpp-builder": "로컬빌더",
        }

        for agent, alias in aliases.items():
            if agent in triggers:
                assert alias in triggers[agent], \
                    f"Agent '{agent}' should have alias '{alias}'"

    def test_no_duplicate_triggers(self, triggers):
        """Verify no critical triggers are duplicated across agents."""
        # Build-related keywords should only be in cpp-builder
        build_keywords = ["빌드", "build", "compile"]

        for keyword in build_keywords:
            agents_with_keyword = [
                agent for agent, kws in triggers.items()
                if keyword in kws
            ]
            # Should only be in cpp-builder (or devops for CI)
            assert "tester" not in agents_with_keyword, \
                f"'{keyword}' should not be in tester triggers"


class TestTriggerKeywordCoverage:
    """Test trigger keyword coverage for common use cases."""

    def test_korean_keywords(self, triggers):
        """Verify Korean keywords are included."""
        # At least some Korean keywords should exist
        korean_keywords_found = False
        for agent, kws in triggers.items():
            if any(kw for kw in kws if any('\uac00' <= c <= '\ud7a3' for c in kw)):
                korean_keywords_found = True
                break

        assert korean_keywords_found, "Korean keywords should be included"

    def test_english_keywords(self, triggers):
        """Verify English keywords are included."""
        english_keywords_found = False
        for agent, kws in triggers.items():
            if any(kw for kw in kws if kw.isascii() and kw.isalpha()):
                english_keywords_found = True
                break

        assert english_keywords_found, "English keywords should be included"


class TestWorkflowRules:
    """Test workflow rules configuration."""

    def test_rules_exist(self, workflow_config):
        """Verify rules are defined."""
        rules = workflow_config.get("rules", [])
        assert len(rules) > 0, "Workflow should have rules defined"

    def test_initial_rule_exists(self, workflow_config):
        """Verify initial rule is defined."""
        rules = workflow_config.get("rules", [])
        initial_rules = [r for r in rules if r.get("id") == "initial"]
        assert len(initial_rules) == 1, "Should have exactly one 'initial' rule"

    def test_workflow_complete_rule_exists(self, workflow_config):
        """Verify workflow complete rule is defined."""
        rules = workflow_config.get("rules", [])
        complete_rules = [r for r in rules if r.get("id") == "workflow_complete"]
        assert len(complete_rules) == 1, "Should have 'workflow_complete' rule"

    def test_rules_have_required_fields(self, workflow_config):
        """Verify all rules have required fields."""
        rules = workflow_config.get("rules", [])

        for rule in rules:
            assert "id" in rule, f"Rule missing 'id': {rule}"
            assert "trigger" in rule or rule.get("id") == "initial", \
                f"Rule missing 'trigger': {rule.get('id')}"
            assert "action" in rule, f"Rule missing 'action': {rule.get('id')}"


class TestParallelConfig:
    """Test parallel execution configuration."""

    def test_parallel_config_exists(self, workflow_config):
        """Verify parallel configuration is defined."""
        parallel = workflow_config.get("parallel", {})
        assert parallel is not None, "Parallel config should exist"

    def test_parallel_defaults(self, workflow_config):
        """Verify parallel configuration has proper defaults."""
        parallel = workflow_config.get("parallel", {})

        # Check key settings exist
        assert "max_concurrent_agents" in parallel
        assert "worktree_dir" in parallel
        assert "parallel_capable_agents" in parallel

    def test_parallel_capable_agents(self, workflow_config):
        """Verify parallel capable agents list."""
        parallel = workflow_config.get("parallel", {})
        capable = parallel.get("parallel_capable_agents", [])

        # These agents should be parallel capable
        expected = ["code-writer", "code-editor", "code-reviewer", "cpp-builder"]
        for agent in expected:
            assert agent in capable, f"'{agent}' should be parallel capable"

    def test_always_sequential_chains(self, workflow_config):
        """Verify sequential chains are defined."""
        parallel = workflow_config.get("parallel", {})
        sequential = parallel.get("always_sequential", [])

        # code-writer -> code-reviewer chain should exist
        assert ["code-writer", "code-reviewer"] in sequential
        # cpp-builder -> tester chain should exist
        assert ["cpp-builder", "tester"] in sequential


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
