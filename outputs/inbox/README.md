# Remote agent inbox

Judgment and owner-file proposals from remote agent hosts land here. Bookkeeping writes that are
already on a skill write licence use `scripts/agent-mutate` (required `--patch`) and skip this
inbox.

Remote hosts write the stamp directory and stop. They never run `scripts/agent-apply-inbox`.

## Layout

```
outputs/inbox/<bot>/<UTC-stamp>/
  PROPOSAL.md      intent, owner files, rationale
  MANIFEST.json    bot, skill, mode, paths, message
  patch.diff       required unified diff (paths must match MANIFEST)
  APPROVED         operator-written; one line: bundle_sha256: <64-hex>
```

`bundle_sha256` covers `PROPOSAL.md`, `MANIFEST.json` and `patch.diff`. Print it with
`--print-hash` after inspecting the bundle. Changing any of those three files after approval is a
hash mismatch.

## Apply

From a real terminal, after inspecting:

```
scripts/agent-apply-inbox outputs/inbox/<bot>/<UTC-stamp> --print-hash
scripts/agent-apply-inbox outputs/inbox/<bot>/<UTC-stamp>
```

No TTY, no `APPROVED`, or a hash mismatch refuses. Owner-file paths are allowed on this path. Env
deny, the protected-path doctor and restore on failure still apply. Owner:
`knowledge/ops/remote-agent-hosts.md`.
