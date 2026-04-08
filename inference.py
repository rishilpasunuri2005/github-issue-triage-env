from __future__ import annotations

from environment import IssueEnvironment
from models import AgentAction, IssueObservation


def dummy_agent_logic(observation: IssueObservation) -> AgentAction:
    text = f"{observation.title} {observation.body}".lower()

    if "dark mode" in text or "theme" in text:
        return AgentAction(action_type="AddLabel", label="enhancement")

    if "steps to reproduce" in text:
        return AgentAction(action_type="AddLabel", label="bug")

    return AgentAction(
        action_type="RequestMoreInfo",
        comment="Please share more details and reproducible steps.",
    )


def main() -> None:
    env = IssueEnvironment(dataset_path="dataset.json")
    observation = env.reset()

    total_score = 0
    step = 0

    print("[START] Episode started")

    while observation is not None:
        step += 1
        action = dummy_agent_logic(observation)
        observation, reward, done, _info = env.step(action)

        total_score += reward
        print(
            f"[STEP] Action: {action.action_type}"
            f"{f'({action.label})' if action.label else ''} "
            f"Reward: {reward}"
        )

        if done:
            break

    env.close()
    print(f"[END] Total Score: {total_score}")


if __name__ == "__main__":
    main()
