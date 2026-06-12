# Che-swarm — CLAUDE.md

## Project Overview

Che-swarm is a minimal AI agent automation system that generates daily sales and marketing content for **Woody's Tree Xperts**, a professional tree service company in North Carolina. A GitHub Actions workflow runs every morning at 9 AM UTC, executes two Python agent scripts, writes Markdown output files to `output/`, and auto-commits the results back to the repository.

---

## Repository Structure

```
Che-swarm/
├── agents/
│   ├── woodys_agent.py       # Single-agent — generates a concise daily sales kit
│   └── woodys_swarm.py       # Multi-agent swarm — generates a full marketing kit
├── output/
│   ├── woodys_YYYY-MM-DD.md        # From woodys_agent.py  (single-agent output)
│   └── woodys_swarm_YYYY-MM-DD.md  # From woodys_swarm.py  (swarm output)
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

## Agent Scripts

### `agents/woodys_agent.py` — Single Agent

A single `client.messages.create()` call that produces a concise daily sales kit in one shot.

- **Model:** `claude-sonnet-4-6`
- **`max_tokens`:** `1000`
- **Output file:** `output/woodys_{date.today()}.md`
- **Content generated:**
  1. Door-knock cold-outreach script
  2. Follow-up text/email after a quote
  3. Three social media posts targeting homeowners
  4. Responses to the top 3 homeowner objections
- **Implementation:** Top-level procedural script, no functions or classes. Today's date injected via string concatenation. No error handling.

### `agents/woodys_swarm.py` — Multi-Agent Swarm

Five sequential `client.messages.create()` calls, each with a specialized agent role, assembled into a single comprehensive marketing kit.

- **Model:** `claude-sonnet-4-6`
- **`max_tokens`:** `1500` per agent call
- **Output file:** `output/woodys_swarm_{date.today()}.md`
- **Named constants at module top:** `TODAY`, `BUSINESS`, `LOCATION`, `SERVICE`
- **`run_agent(role, task) -> str` helper:** Wraps every API call; builds the prompt from the shared constants + caller-supplied role/task strings.

**Agents (run sequentially):**

| # | Agent Role | Content Produced |
|---|---|---|
| 1 | Social media copywriter | Platform-native posts for Instagram, Facebook, TikTok, LinkedIn, X/Twitter |
| 2 | Field sales trainer | Door-knock script + 60-second phone pitch script |
| 3 | Direct-response email copywriter | Cold outreach email + 24–48 h follow-up email |
| 4 | Sales coach | Responses to 5 homeowner objections (price, timing, DIY, competition, approval) |
| 5 | Social media strategist | 7-day content calendar (platform, theme, post time, format) |

The five outputs are assembled into a single Markdown document with `---` section dividers.

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
4. **Woodys Agent** — runs `agents/woodys_agent.py` with `ANTHROPIC_API_KEY`
5. **Woodys Swarm** — runs `agents/woodys_swarm.py` with `ANTHROPIC_API_KEY`
6. **Save Output** — configures git identity (`Che Swarm / swarm@che.com`), stages all changes (`git add -A`), commits with `"Swarm output $(date)"`, and pushes to `origin`. Uses `|| echo "Nothing to commit"` so it never fails on a no-op.

**Required secrets (configured in GitHub repository settings):**
- `ANTHROPIC_API_KEY` — Anthropic API key with access to `claude-sonnet-4-6`
- `GITHUB_TOKEN` — provided automatically by GitHub Actions

---

## Output Format

### Single-agent output (`woodys_YYYY-MM-DD.md`)

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

### Swarm output (`woodys_swarm_YYYY-MM-DD.md`)

```markdown
# Woody's Tree Xperts — Full Marketing Kit — YYYY-MM-DD

---

## Social Media Posts
...

---

## Sales Pitch Scripts
...

---

## Email Templates
...

---

## Objection Responses
...

---

## Weekly Content Calendar
...
```

Output files are **committed automatically by CI** and are not meant to be edited manually.

---

## Development Conventions

### Naming
- Agent scripts: `{client_name}_agent.py` (single-agent) or `{client_name}_swarm.py` (multi-agent) inside `agents/`
- Single-agent output: `output/{client_name}_{date}.md`
- Swarm output: `output/{client_name}_swarm_{date}.md`
- Git commit messages from CI: `"Swarm output $(date)"` (automated, do not change manually)

### Code style
- Standard library imports first, then third-party (`anthropic`), each on its own line.
- Single-agent scripts: no classes or functions — fully top-level and procedural.
- Multi-agent scripts: one `run_agent(role, task) -> str` helper at the top, shared named constants (`TODAY`, `BUSINESS`, etc.), then sequential agent calls as top-level statements.
- Environment variables accessed via `os.environ.get(...)`.
- Output directory always created with `os.makedirs(..., exist_ok=True)`.
- No error handling — failures surface as CI job failures.

### Adding a new single agent
1. Create `agents/{client_name}_agent.py` following the same structure as `woodys_agent.py`.
2. Add a step to `.github/workflows/swarm.yml` that runs the new script (with any needed secrets).
3. The existing **Save Output** step picks up the new file via `git add -A`.

### Adding a new swarm agent
1. Create `agents/{client_name}_swarm.py` following the same structure as `woodys_swarm.py` — define named constants, a `run_agent` helper, sequential agent calls, and an assembly block.
2. Add a step to `.github/workflows/swarm.yml` after the existing agent steps.
3. The existing **Save Output** step picks up the new file via `git add -A`.

---

## Running Locally

```bash
# Install the dependency
pip install anthropic

# Set your API key
export ANTHROPIC_API_KEY=sk-ant-...

# Run the single agent (quick, 1 API call)
python agents/woodys_agent.py
# → output/woodys_<today>.md

# Run the full swarm (5 sequential API calls, takes longer)
python agents/woodys_swarm.py
# → output/woodys_swarm_<today>.md
```

---

## What This Repo Does NOT Have

- No tests or test framework
- No `requirements.txt` / `pyproject.toml` / lockfile (dependency installed unpinned in CI)
- No virtual environment configuration
- No linter or formatter configuration
- No branching strategy beyond `main` (CI always pushes directly to `main`)
- No Docker or containerization
- No environment-specific configuration beyond the single `ANTHROPIC_API_KEY` secret

Keep new additions consistent with this minimal, single-purpose design.
