# NOTICE

Linket Agent is a fork of **Hermes Agent**, originally created and
maintained by [Nous Research](https://nousresearch.com).

- Upstream project: <https://github.com/NousResearch/hermes-agent>
- Upstream license: MIT
- Fork point: 2026-05-09 (Nous Research, copyright 2025)
- This fork: <https://github.com/robertbr123/Linket-Agent>

Both projects are MIT-licensed. The original copyright notice is
preserved in the [`LICENSE`](LICENSE) file alongside the Linket Agent
fork copyright, as required by the MIT license terms.

## What changed in the fork

The fork is a rebrand and rehost — the Linket name, install URL
(`linket.com.br`), repo location (`robertbr123/Linket-Agent`), and
home directory (`~/.linket`) replace their upstream counterparts.
Everything substantive — the agent runtime, skills system, gateway,
cron scheduler, terminal backends, RL environments, and tool-calling
infrastructure — is from upstream and continues to evolve there.

Specifically, the fork modifies:

- Brand identity (`assets/banner.svg`, `assets/logo-mark.svg`)
- Package metadata (`pyproject.toml`, `package.json`, `flake.nix`)
- Public install URL (`linket.com.br/install.{sh,ps1,cmd}` redirector
  in `infra/redirect-worker.js`) and `scripts/install.{sh,ps1,cmd}`
  contents
- CLI entry points: `linket` / `linket-agent` / `linket-acp` are
  canonical, with `hermes` / `hermes-agent` / `hermes-acp` retained
  as deprecated aliases
- Default home directory: `~/.linket` (with one-shot auto-migration
  from `~/.hermes` on first launch)
- User-facing path renames in `skills/`, `plugins/`,
  `optional-skills/`, `packaging/`, `nix/`, and `website/docs/`
- Documentation surface (READMEs, AGENTS.md, CONTRIBUTING.md,
  SECURITY.md, `website/docs/`)

The fork does **not** modify (in this rebrand pass):

- The agent's behaviour, prompt assembly, model routing, or learning loop
- The skills authoring contract (skills built for Hermes work on Linket)
- The gateway protocol or bot identities
- The plugin API
- Internal Python module names (`hermes_cli`, `hermes_state`,
  `hermes_constants`, `hermes_logging`, `hermes_time`,
  `hermes_bootstrap`) — these are scheduled for a separate rename
  that requires a coordinated test sweep

## Acknowledgements

This project is built on the work of the Hermes Agent team and its
contributors. The full upstream contribution history is preserved in
the original repository's `git log`. Notable upstream components
incorporated unchanged include:

- The agent core (`run_agent.py`, `agent/`, `model_tools.py`)
- The CLI framework (`hermes_cli/`)
- The messaging gateway (`gateway/`, `tui_gateway/`)
- The cron scheduler (`cron/`)
- The skills system (`skills/`, `optional-skills/`)
- The plugins framework (`plugins/`)
- The terminal backends in `agent/`
- The Atropos RL integration (`tinker-atropos/`, `environments/`)
- The Honcho dialectic user model integration

## Trademarks

"Hermes Agent" and the Hermes/caduceus mark belong to Nous Research.
This fork uses the name "Linket Agent" and a chain-link mark to
clearly distinguish itself; it does not claim or endorse the Hermes
trademarks. Where the Hermes name remains in this codebase (in
historical release notes, attribution lines, and module identifiers
yet to be renamed), it appears in attribution context only.

## Reporting

For issues with the upstream Hermes Agent codebase, file at
<https://github.com/NousResearch/hermes-agent/issues>. For issues
specific to the Linket Agent fork (install URLs, branding, fork-only
behaviour), file at
<https://github.com/robertbr123/Linket-Agent/issues>.
