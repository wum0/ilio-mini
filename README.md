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
kimi login                                    # only for ./ilio -k; ~/.kimi-code credentials/oauth are mounted
cat > .env <<'EOF'                            # gitignored; also passed to the container
CTFD_TOKEN=ctfd_xxx
# or: CTFD_USER=me
# CTFD_PASS=secret
EOF
```

## Use
```bash
./ilio auto                   # Codex: wait for start -> solve next unsolved -> auto-submit -> next
./ilio auto -k                # same loop with Kimi Code
```
Results: `chals/results.tsv` (wall s, first-turn s, tokens, flag). Solves: `chals/SOLVES.md` (mounted as `/solves.md`;
prior flags are also tried as archive passwords).

## Layout
- `ilio` — CTFd client + docker launcher (host) and triage + codex loop + `ilio submit` (container).
- `codex/` — `config.toml` (gpt-5.6-sol, effort high, priority tier), `AGENTS.md` (the reverser's instructions), hooks: `stop.sh`
  (keep going until a correct flag) and `nudge.py` (at 10/30 min without a flag, tell the root agent to split into lanes).
- `kimi/` — Kimi Code config (`kimi-code/k3`, yolo), `AGENTS.md`, `stop.sh` (Stop, exit 2 continues the turn), `nudge.py` (SessionHeartbeat; the note is delivered on the next Stop).
  The image installs Kimi Code (`KIMI_INSTALL_DIR=/usr/local`). Host `~/.kimi-code` supplies only the login.
- `skills/` — `flareon` (playbook), `explore-alternatives`, `dotnet`, `python-re`, `windows-dynamic`; `kuna-decompiler` is installed from the kuna binary.

`-k` selects Kimi Code (`./ilio solve 6 -k`, `./ilio auto -k`). It uses the image binary, the host `~/.kimi-code` login (`kimi login`), `kimi/config.toml`, and model `kimi-code/k3`. Without `-k` the agent is Codex.

Env knobs: `ILIO_TIMEOUT_H` (24, hard stop), `ILIO_BUDGET_H` (8), `ILIO_RESUMES` (12), `ILIO_FALLBACK_MODEL` (gpt-daybreak-blue-latest, used after repeated cyber-filter blocks), `ILIO_MEM` (96g), `ILIO_KUNA_DEV=~/github/kuna` (mount a freshly
built kuna checkout instead of the image's release; `git pull && make binaries` first; can live in `.env`).
Kuna gaps hit by the agent are written to `chals/*/KUNA_NEED.md`.
