# ilio-mini
A tiny, fast harness that runs Codex in Docker to solve Flare-On (reverse engineering) challenges.
It is built around the agent-based decompiler [Kuna](https://github.com/noelo-lab/kuna), made for speed. 
The idea of ilio-mini is to simply be fast. 

🥉 ilio-mini got 3rd in [FlareOn 13](https://flare-on13.ctfd.io/users/209). 
An analysis of tool use during the competition can be found on this [page](https://mahaloz.github.io/ilio-mini/flareon13_results/), also found [here](./flareon13_results).

## Results
- Costs: $21.3
- Total Time: 80.5 min
- Kuna: used on 6/9 challenges.

## Setup
```bash
docker build -t ilio-mini .                   # ubuntu:24.04 + kuna + RE tooling + codex + kimi
codex login                                   # on the host; ~/.codex/auth.json is bind-mounted rw (never copied)
kimi login                                    # only for ILIO_AGENT=kimi; ~/.kimi-code credentials/oauth are mounted
cat > .env <<'EOF'                            # gitignored; also passed to the container
CTFD_TOKEN=ctfd_xxx
# or: CTFD_USER=me
# CTFD_PASS=secret
EOF
```

## Use
```bash
./ilio auto                   # wait for start -> solve next unsolved -> auto-submit -> next (headless)
```
Results: `chals/results.tsv` (wall s, first-turn s, tokens, flag). Solves: `chals/SOLVES.md` (mounted as `/solves.md`;
prior flags are also tried as archive passwords).

## Layout
- `ilio` — CTFd client + docker launcher (host) and triage + codex loop + `ilio submit` (container).
- `codex/` — `config.toml` (gpt-5.6-sol, effort high, priority tier), `AGENTS.md` (the reverser's instructions), hooks: `stop.sh`
  (keep going until a correct flag) and `nudge.py` (at 10/30 min without a flag, tell the root agent to split into lanes).
- `kimi/` — the same role for Kimi Code: `config.toml` (kimi-code/k3, yolo, stop + nudge hooks), `AGENTS.md`, `stop.sh`, `nudge.py`.
  The image installs Kimi Code (`KIMI_INSTALL_DIR=/usr/local`). Host `~/.kimi-code` supplies only the login.
- `skills/` — `flareon` (playbook), `explore-alternatives`, `dotnet`, `python-re`, `windows-dynamic`; `kuna-decompiler` is installed from the kuna binary.

`ILIO_AGENT=codex` (default) or `kimi`. Kimi is installed in the image and uses the host `~/.kimi-code` login (`kimi login`) plus `kimi/config.toml`. Model `ILIO_KIMI_MODEL` (default `kimi-code/k3`). Put `ILIO_AGENT=kimi` in `.env` or the shell that runs `./ilio`. Codex is unchanged when the variable is unset.

Env knobs: `ILIO_TIMEOUT_H` (24, hard stop), `ILIO_BUDGET_H` (8), `ILIO_RESUMES` (12), `ILIO_FALLBACK_MODEL` (gpt-daybreak-blue-latest, used after repeated cyber-filter blocks), `ILIO_MEM` (96g), `ILIO_KUNA_DEV=~/github/kuna` (mount a freshly
built kuna checkout instead of the image's release; `git pull && make binaries` first; can live in `.env`).
Kuna gaps hit by the agent are written to `chals/*/KUNA_NEED.md`.
