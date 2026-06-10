# Che-swarm — CLAUDE.md

## Project Overview

Che-swarm is a minimal AI agent automation system that generates daily sales and marketing content for **Woody's Tree Xperts**, a professional tree service company in North Carolina. A GitHub Actions workflow runs the agent every morning at 9 AM UTC, writes a Markdown sales kit to `output/`, and auto-commits the result back to the repository.

---

## Repository Structure

```
Che-swarm/
├── agents/
│   └── woodys_agent.py       # Single agent — generates daily sales content
├── output/
│   └── woodys_YYYY-MM-DD.md  # Auto-generated daily sales kits (committed by CI)
└── .github/
    └── workflows/
        └── swarm.yml         # Scheduled GitHub Actions workflow
```

---

## Tech Stack

| Layer | Choice |
|---|---|
| Language | Python 3.11 |
| AI SDK | `anthropic` (installed via pip in CI, no lockfile) |
| Model | `claude-sonnet-4-6` |
| CI/CD | GitHub Actions |
| Output format | Markdown |

No virtual environment, no `requirements.txt`, no `pyproject.toml`. The only Python dependency is the `anthropic` package, installed fresh on every CI run.

---

## How the Agent Works

**File:** `agents/woodys_agent.py`

1. Reads `ANTHROPIC_API_KEY` from the environment.
2. Calls `client.messages.create()` with a single user message that instructs the model to produce a daily sales kit including:
   - A door-knock cold-outreach script
   - A follow-up text/email after a quote
   - Three social media posts targeting homeowners
   - Responses to the top 3 homeowner objections
3. Writes the response to `output/woodys_{date.today()}.md` with a Markdown header.
4. Prints `"Content generated successfully"`.

Key implementation details:
- Synchronous call (no async/streaming).
- `max_tokens=1000`.
- Today's date is injected into the prompt via string concatenation.
- No error handling — failures surface as CI job failures.

---

## CI/CD Workflow

**File:** `.github/workflows/swarm.yml`

| Setting | Value |
|---|---|
| Trigger | Daily cron `0 9 * * *` (9 AM UTC) + manual `workflow_dispatch` |
| Runner | `ubuntu-latest` |
| Python | 3.11 |
| Permissions | `contents: write` (required for the auto-commit) |

**Pipeline steps:**
1. `actions/checkout@v3` — checks out the repo with `GITHUB_TOKEN`
2. `actions/setup-python@v4` — sets up Python 3.11
3. `pip install anthropic` — installs the SDK (unpinned)
4. Run `agents/woodys_agent.py` with `ANTHROPIC_API_KEY` injected as an env var
5. **Save Output** — configures git identity (`Che Swarm / swarm@che.com`), stages all changes, commits with `"Swarm output $(date)"`, and pushes to `origin`. The commit step uses `|| echo "Nothing to commit"` so it never fails when there is no new output.

**Required secrets (configured in GitHub repository settings):**
- `ANTHROPIC_API_KEY` — Anthropic API key with access to `claude-sonnet-4-6`
- `GITHUB_TOKEN` — provided automatically by GitHub Actions

---

## Development Conventions

### Naming
- Agent scripts: `{client_name}_agent.py` inside `agents/`
- Output files: `{client_name}_{date}.md` inside `output/`
- Git commit messages from CI: `"Swarm output $(date)"` (automated, do not change manually)

### Code style
- Standard library imports first, then third-party (`anthropic`), each on its own line.
- No classes or functions — agents are top-level procedural scripts executed once.
- Environment variables accessed via `os.environ.get(...)`.
- Output directory is always created with `os.makedirs(..., exist_ok=True)`.

### Adding a new agent
1. Create `agents/{client_name}_agent.py` following the same structure as `woodys_agent.py`.
2. Add a step to `.github/workflows/swarm.yml` that runs the new script (with any needed secrets).
3. Add a corresponding **Save Output** step or reuse the existing one (since `git add -A` picks up all changes).

---

## Running Locally

```bash
# Install the dependency
pip install anthropic

# Set your API key
export ANTHROPIC_API_KEY=sk-ant-...

# Run the agent
python agents/woodys_agent.py

# Output appears in output/woodys_<today>.md
```

---

## Output Format

Each generated file is a Markdown document structured as:

```markdown
# Woody's Daily Sales Kit — YYYY-MM-DD

## Door Knock Script
...

## Follow Up Message
...

## Social Media Posts
...

## Objection Responses
...
```

Output files are **committed automatically by CI** and are not meant to be edited manually.

---

## What This Repo Does NOT Have

- No tests or test framework
- No `requirements.txt` / `pyproject.toml` / lockfile (dependency is installed unpinned in CI)
- No virtual environment configuration
- No linter or formatter configuration
- No branching strategy beyond `main` (CI always pushes directly to `main`)
- No Docker or containerization
- No environment-specific configuration beyond the single `ANTHROPIC_API_KEY` secret

Keep new additions consistent with this minimal, single-purpose design.
