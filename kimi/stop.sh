#!/bin/sh
# Kimi Stop hook. Exit 2 blocks the turn and stderr is appended so the model continues.
# https://www.kimi.com/code/docs/kimi-code-cli/customization/hooks.html
[ -f /work/FLAG ] || [ -f /work/HELP.md ] && exit 0
n=$(cat /work/.stops 2>/dev/null || echo 0); [ "$n" -ge 30 ] && exit 0
echo $((n + 1)) > /work/.stops
echo "No correct flag yet (ilio submit has not returned correct). Keep working: check /work/notes.md, pick the next most promising lead, and continue." >&2
if [ -s /work/.nudge-msg ]; then cat /work/.nudge-msg >&2; rm -f /work/.nudge-msg; fi
exit 2
