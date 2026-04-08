# GitHub Issue Triage Environment (OpenEnv RL Challenge)

> A compact, evaluator-friendly RL environment that simulates a maintainer’s triage workflow: label clear issues (`bug` / `enhancement`) and request more info for vague reports.

## Why This Project Stands Out

- **Directly aligned with real maintainer work**: converts noisy issue text into actionable triage decisions.
- **Reward-driven behavior**: encourages high-signal decisions, especially on ambiguous issues.
- **Simple, inspectable design**: easy to verify quickly during hackathon evaluation.
- **Fast to run**: lightweight Python-only core suitable for constrained environments.

## Project Snapshot

This repository currently includes:

- `environment.py` — core issue triage environment and reward logic
- `models.py` — Pydantic models for observations/actions
- `dataset.json` — benchmark issue samples with expected actions/labels
- `q_table.json` / `dqn_issue_triage.zip` — learned artifacts from prior experiments
- `output.txt` / `batch_predictions.*` — run outputs and prediction exports

## Triage Task Definition

For each issue, the agent must choose:

1. `AddLabel("bug")`
2. `AddLabel("enhancement")`
3. `RequestMoreInfo`

### Reward Function

- **+1**: correct `AddLabel` with correct label
- **+2**: correct `RequestMoreInfo` on vague/incomplete issue
- **-1**: wrong action or wrong label

This reward shape intentionally prioritizes safe handling of low-information reports.

## Core Data Models

`IssueObservation`:
- `issue_id`
- `title`
- `body`

`AgentAction`:
- `action_type`: `AddLabel | RequestMoreInfo`
- `label` (optional): `bug | enhancement`
- `comment` (optional)

## Quick Start

### 1) Install dependencies

```bash
pip install pydantic
```

### 2) Run a minimal loop

```python
from environment import IssueEnvironment
from models import AgentAction

env = IssueEnvironment("dataset.json")
obs = env.reset()

done = False
total = 0
while not done:
    # naive baseline for demo only
    action = AgentAction(action_type="RequestMoreInfo")
    obs, reward, done, info = env.step(action)
    total += reward

print("Total reward:", total)
```

## Evaluator Notes

If you are evaluating this project for the OpenEnv challenge:

- The environment API is intentionally minimal and deterministic.
- Reward behavior is transparent in `environment.py`.
- Ground truth for checks is in `dataset.json`.
- The code is small enough for quick manual audit.

## OpenEnv Submission Checklist

- [x] Root-level RL environment logic present
- [x] Deterministic, auditable reward function
- [x] Dataset with expected action metadata
- [ ] `inference.py` at repository root (required by final validator)
- [ ] Required OpenEnv stdout contract (`[START] / [STEP] / [END]`) in active submission entrypoint

> If you want, I can generate a fully validator-compliant `inference.py` in this repo state and wire it to this environment.

## Repository

- GitHub: [rishilpasunuri2005/github-issue-triage-env](https://github.com/rishilpasunuri2005/github-issue-triage-env)
