#!/usr/bin/env python3
"""
UserPromptSubmit hook - 에이전트 트리거 감지 및 디스패치

실행 시점: 사용자 프롬프트가 Claude에게 전달되기 전
동작: workflow.json의 트리거 키워드를 감지하고 에이전트 디스패치 컨텍스트 주입

사용법:
    Claude Code settings.json의 UserPromptSubmit 훅으로 자동 실행
"""

import json
import sys
import re
from pathlib import Path


def load_triggers() -> dict:
    """workflow.json에서 트리거 로드"""
    script_dir = Path(__file__).parent.parent  # .claude/
    workflow_path = script_dir / "workflow.json"

    if not workflow_path.exists():
        return {}

    try:
        with open(workflow_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("workflow", {}).get("triggers", {})
    except (json.JSONDecodeError, IOError):
        return {}


def build_trigger_list(triggers_dict: dict) -> list:
    """트리거 목록 생성 (다중 단어 우선)"""
    multi_word = []
    single_word = []

    for agent, trigger_list in triggers_dict.items():
        if agent.startswith("_"):
            continue
        for trigger in trigger_list:
            if " " in trigger:
                multi_word.append((trigger, agent))
            else:
                single_word.append((trigger, agent))

    return multi_word + single_word


def find_triggers(prompt: str, triggers: list) -> list:
    """프롬프트에서 트리거 찾기"""
    found = []
    prompt_lower = prompt.lower()

    for trigger, agent in triggers:
        trigger_lower = trigger.lower()

        if " " in trigger:
            if trigger_lower in prompt_lower:
                found.append((trigger, agent))
        else:
            pattern = rf"\b{re.escape(trigger)}\b"
            if re.search(pattern, prompt, re.IGNORECASE):
                found.append((trigger, agent))

    # 에이전트별 중복 제거
    seen = set()
    unique = []
    for trigger, agent in found:
        if agent not in seen:
            seen.add(agent)
            unique.append((trigger, agent))

    return unique


# 자동 액션 패턴
AUTO_ACTION_PATTERNS = {
    "auto_commit": [
        r"테스트\s*(수동\s*)?OK",
        r"테스트\s*통과",
        r"빌드\s*OK",
        r"확인\s*완료",
        r"괜찮아",
        r"좋아",
        r"승인",
        r"LGTM",
        r"looks\s+good",
        r"approved",
    ],
    "auto_save_session": [
        r"세션\s*종료",
        r"저장\s*하고\s*끝",
        r"오늘\s*끝",
        r"end\s+session",
    ],
}


def detect_auto_actions(prompt: str) -> list:
    """자동 액션 패턴 감지"""
    detected = []

    for action, patterns in AUTO_ACTION_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                detected.append(action)
                break

    return detected


def main():
    """메인 엔트리포인트"""
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    prompt = input_data.get("prompt", "")
    if not prompt:
        sys.exit(0)

    # /workflow 명령은 스킵
    if prompt.strip().startswith("/workflow"):
        sys.exit(0)

    # 트리거 로드
    triggers_dict = load_triggers()
    if not triggers_dict:
        sys.exit(0)

    triggers = build_trigger_list(triggers_dict)
    found = find_triggers(prompt, triggers)
    auto_actions = detect_auto_actions(prompt)

    if auto_actions or found:
        lines = []

        if auto_actions:
            lines.append("[AUTO-ACTION DETECTED]")
            if "auto_commit" in auto_actions:
                lines.append("User confirmed. AUTO-COMMIT without asking.")
            if "auto_save_session" in auto_actions:
                lines.append("User requested session end. Run /session:save.")
            lines.append("")

        if found:
            lines.append("[AGENT DISPATCH REQUIRED]")
            for trigger, agent in found:
                lines.append(f"  Trigger: '{trigger}' -> Agent: {agent}")
            lines.append("")
            lines.append("IMPORTANT: You are the main orchestrator (달미).")
            lines.append("DO NOT become the agent yourself.")
            lines.append("DO NOT respond as the agent directly.")
            lines.append(f"MUST use Task tool with subagent_type='{found[0][1]}' to delegate.")
            lines.append("After receiving the result, summarize it to the user in Korean.")

        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": "\n".join(lines)
            }
        }
        print(json.dumps(output))

    sys.exit(0)


if __name__ == "__main__":
    main()
