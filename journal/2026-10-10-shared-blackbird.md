# Shared Blackbird doctrine

2026-10-10 operator centralizes the working doctrine at ~/projects/BLACKBIRD.md.
Add Diction & style guidance: describe concrete components/actions, destinations
and failure behavior; prefer emit/write/read over abstractions about evidence
and custody. Replace this repository's BLACKBIRD.md copy with a relative symlink to that
workspace file. Verify the link resolves and reads identical bytes; leave quarantined references
and unrelated changes untouched.

2026-10-23: the committed link target `../../../projects/BLACKBIRD.md` stopped
resolving after the workspace move. Retargeted it to `../BLACKBIRD.md`, which
resolves from `~/projects/crolib`. Same fix in salib.
