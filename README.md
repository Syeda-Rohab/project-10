# Project 10: The Secrets Drill

Fail the `.env` way once, on purpose. Uses GitHub Actions Secrets as
the free stand-in for Claude Code's "environment-variables panel"
(same real Claude Code Routines caveat as Project 9 — this needs a
paid plan for the real thing; the mechanism taught here is identical).

- **Time:** 30–45 min
- **Difficulty:** easy to medium
- **Concepts used:** A2 (the environment), A4 (secrets)

## Files
| File | Role |
|---|---|
| `token_task.py` | The task — tries an env var, then a `.env` file, reports exactly what it found |
| `.gitignore` | Excludes `.env` — the whole point of the drill |
| `.env` | **Local only.** Has a dummy token. Never gets pushed. |
| `.github/workflows/secrets-drill.yml` | Manual-run workflow with two modes |

## The core fact this drill teaches
`.env` is in `.gitignore`, so `git status` never shows it, `git add -A`
never stages it, and a fresh clone (which is exactly what a GitHub
Actions runner is — a brand-new checkout) **never contains it.** Your
local machine has the file; GitHub's copy of your repo does not.

Confirmed directly:
```
git ls-files | grep .env  →  (nothing — .env is not tracked)
```

## Run 1: the `.env` way (fails on GitHub, works locally)
**Locally**, this works fine — the file is right there:
```
$ python token_task.py
API_TOKEN not found in the environment. Trying a .env file next...
Found API_TOKEN in .env: 'dummy-token-local-12345' (.env file found and read)
TASK SUCCEEDED (via .env): Hello, authenticated with dummy-token-local-12345.
```

**On GitHub** (a fresh clone, no local files carried over):
1. Push this repo to GitHub (`.env` will simply not be part of the push).
2. Actions tab → "Secrets Drill" → **Run workflow** → mode: `dotenv`.
3. Read the transcript (expand the "Run 1" step):
   ```
   API_TOKEN not found in the environment. Trying a .env file next...
   Could not find .env either (no .env file found in this working directory).
   TASK FAILED: no API_TOKEN available anywhere in this environment.
   ```
   This is what Claude tried instead: it looked for an environment
   variable, didn't find one, then looked for a `.env` file — and on
   the fresh clone, neither exists.

## Fix: move the token to the environment-variables panel
1. On GitHub: repo → **Settings** → **Secrets and variables** →
   **Actions** → **New repository secret**.
   - Name: `API_TOKEN`
   - Value: `dummy-token-cloud-67890` (any dummy value)
2. This secret is GitHub's real equivalent of Claude Code's
   environment-variables panel — a value stored outside the repo,
   injected into the run at execution time.
3. The workflow already includes the one line the appendix
   recommends, as a comment plus the actual mechanism:
   *"credentials are available as environment variables; do not look
   for a `.env` file."* — implemented here as `env: API_TOKEN:
   ${{ secrets.API_TOKEN }}` on the job step, so the script finds it
   on the very first check.

## Run 2: the environment-variable way (works)
1. Actions tab → **Run workflow** → mode: `env_var`.
2. Read the transcript:
   ```
   Found API_TOKEN in the environment: 'dummy-token-cloud-67890'
   TASK SUCCEEDED: Hello, authenticated with dummy-token-cloud-67890.
   ```
   Found on the **first** check — no `.env` lookup needed at all.

## Done-when checklist
- [x] Second run reads the token from the environment (not `.env`).
- [x] Can explain the mechanical reason the first run failed: `.env`
      is gitignored, so it never gets pushed to GitHub; a fresh clone
      (what a GitHub Actions runner is) starts with exactly what's in
      the repo — which does not include gitignored files, by design.

## The one-sentence answer (A4)
**A gitignored `.env` file only ever exists on the machine that
created it; anywhere the code is freshly cloned — cloud sandbox, CI
runner, a teammate's laptop — that file simply isn't there, so
secrets meant to travel with the run have to live in an actual
environment-variable store, not in a file that git was told to ignore.**
