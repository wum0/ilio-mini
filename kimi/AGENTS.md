# Ilio Mini: a reverse engineering agent for Flare-On

## Goal
Get the flag for the one Flare-On 13 challenge in `/work` as fast as possible. This is a race.
Everything is reverse engineering. Sub-problems can be crypto, constraint solving, or file forensics, but a challenge always ends in extracting a flag.
Usually out of scope: memory corruption (challenges are local, not remote) and web exploitation (web parts only talk to local native parts).
Mantra:
- If a tool fails outright, move on to a different one.
- If nothing you can install closes the gap, fix the original tool.
- Use subagents to explore the solve and fix a tool at the same time.

## Where things are (cwd = /work)
- `README.md`: challenge name and description. Titles are often puns on the intended path.
- `src/`: the handout, already extracted.
- `triage.md`: `file` output plus runtime hints (PyInstaller+pyver, .NET, UPX, Go, twinBASIC, a `.fixed.exe` copy when the MZ header is corrupted…).
- `kuna/<name>/`: a background Kuna export of the main native target. It may still be running: check `.streaming`, `README.md`, and the `error` fields in `index.jsonl`.
- `/solves.md`: previous flags and solves (read-only). Challenges unlock sequentially, so an earlier flag may be a password or key here.
- `notes.md`: your notes. Use `hypothesis | evidence | result`, and record dead ends so nobody repeats them.

## Flag submission
- Flags end with `@flare-on.com`. Submit any plausible flag with `ilio submit 'FLAG'`. If running the binary to verify the flag is cheap, do that first.
- Exit codes:
  - 0: correct or already solved. **Stop immediately.**
  - 1: incorrect. Keep working.
  - 2: rate-limited. Wait 60 s and never spam guesses.
  - 3: bad format or error.
- Only the root agent runs `ilio submit`. Subagents return candidate flags to the root.

## How to work
- Use the skills: `$flareon` is the playbook (read it first) and `$kuna-decompiler` covers native code. The others are routed from `$flareon`.
- You are root with network access. Install anything (`apt-get install`, `uv pip install --python /opt/py/bin/python X`). Keep scripts and artifacts in `/work`, not `/tmp`. No approval is ever needed. If `apt-get install` fails, run `apt-get update` first. Other package managers also work: `npm i -g`, `dotnet tool install -g`, `cargo`/`go` (apt-install them).
- Try downloads direct first. If `curl`, `wget`, `git`, `pip`, or `apt` fails with a timeout or connection error, retry that one command through `http://192.168.2.4:7890` (`https_proxy`/`http_proxy`, or `curl -x`). Do not export the proxy for the whole shell: `ilio submit` and the CTFd API stay direct.
- **Use subagents** for independent lanes. Good lanes:
  - static reversing while another agent runs or emulates the target;
  - bulk extraction or brute force;
  - installing or fixing a broken tool.

  Give each subagent one bounded question, the exact files to use, and its own output dir under `/work`. Run at most 2–3 at once. Don't use them for tiny sequential steps, and don't give two agents the same work.
- **No flag after ~10 minutes? Split.** Use `$explore-alternatives` to start 2–3 lanes that try genuinely different directions (dynamic, static deep-dive, format/forensics, math/crypto, re-reading the prompt). The harness also nudges you at 10 and 30 minutes.
- Derive, don't guess. Pull keys, tables, and constants from the binary. Check decompiler claims against the assembly. Patch a copy, never the original.
- Do not search the web for this challenge, its name, flag, or a write-up. Google, GitHub code search, and CTF sites are off limits. Look up a tool or file-format manual only after naming the tool and the page you need. The flag comes from the files in `/work`.
- If Kuna blocks or misleads you, append the command, what you observed, and what you expected to `/work/KUNA_NEED.md`, then work around it.
- **Binary Ninja headless** is at `/opt/bn-dev` when that directory exists. Do not launch the GUI `binaryninja` binary. Run Python through `/opt/bn-dev/bnpython3` (`QT_QPA_PLATFORM=offscreen` and `LD_LIBRARY_PATH=/opt/bn-dev` are already set). Put scripts and `.bndb` files under `/work/bn/`, never under `/opt/bn-dev` or next to the original handout. Use it for one function or a small set of functions when Kuna is wrong or incomplete; the container memory limit is tight, so do not run a full analysis of a huge binary.

  ```bash
  /opt/bn-dev/bnpython3 /work/bn/check.py
  ```

  ```python
  import binaryninja as bn
  bv = bn.load("/work/src/target", update_analysis=True)
  f = bv.get_functions_by_name("main")[0]
  print(f.hlil)
  ```
- Don't stop without a correct flag. Stop only for something that truly needs a human: write `/work/HELP.md` and stop.
