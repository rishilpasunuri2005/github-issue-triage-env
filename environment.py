from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from models import AgentAction, IssueObservation


def _compute_reward(action: AgentAction, expected_action: str, expected_label: str | None) -> int:
    if expected_action == "RequestMoreInfo":
        return 2 if action.action_type == "RequestMoreInfo" else -1
    if action.action_type == "AddLabel" and action.label == expected_label:
        return 1
    return -1


class IssueEnvironment:
    def __init__(self, dataset_path: str | Path = "dataset.json") -> None:
        self.dataset_path = Path(dataset_path)
        self._issues: list[dict[str, Any]] = []
        self._index = 0

    def reset(self) -> IssueObservation:
        with open(self.dataset_path, encoding="utf-8") as fh:
            self._issues = json.load(fh)
        if not self._issues:
            raise ValueError("dataset.json is empty.")
        self._index = 0
        return self._current_observation()

    def step(self, action: AgentAction) -> tuple[IssueObservation | None, int, bool, dict[str, Any]]:
        current = self._issues[self._index]
        reward = _compute_reward(
            action=action,
            expected_action=current["expected_action"],
            expected_label=current.get("expected_label"),
        )

        info: dict[str, Any] = {
            "issue_id": current["issue_id"],
            "expected_action": current["expected_action"],
            "expected_label": current.get("expected_label"),
            "agent_action": action.action_type,
            "agent_label": action.label,
            "reward": reward,
        }

        self._index += 1
        done = self._index >= len(self._issues)
        next_obs = None if done else self._current_observation()
        return next_obs, reward, done, info

    def close(self) -> None:
        return None

    def _current_observation(self) -> IssueObservation:
        issue = self._issues[self._index]
        return IssueObservation(
            issue_id=issue["issue_id"],
            title=issue["title"],
            body=issue["body"],
        )
