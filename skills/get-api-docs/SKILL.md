---
name: get-api-docs
description: >
  Retrieve documentation for libraries, frameworks, SDKs, and APIs through Context
  Hub (chub), including configured local packs. Use when implementation or debugging
  needs API reference, when checking documented behavior, or when the user requests
  Context Hub documentation. Match the project's actual versions and supplement
  missing or outdated coverage with official documentation.
---

# Get API Docs with Context Hub

Use chub to discover and selectively read documentation before relying on an
unverified API shape. Treat a pack's version and coverage as claims to check;
retrieving a pack does not establish that it is complete or current.

## Establish the target and available commands

- Identify the language and actual dependency versions from the project. For Go,
  distinguish the active toolchain and resolved modules from the minimum Go
  version declared in `go.mod`; account for replacements or vendoring.
- Run `chub --help` once when starting this workflow in a session. Use subcommand
  help to confirm flags supported by the installed CLI. Remote bootstrap help
  may change independently of the installed package.
- If chub is unavailable, use official documentation and explain the fallback.
  Install or upgrade the CLI only when that setup is within the requested task.
- When an environment supplies a dedicated official OpenAI documentation
  workflow, follow it for OpenAI topics; chub material can supplement it.

## Find and retrieve relevant material

```sh
chub search "<library or framework>" --json
chub search <confirmed-id> --json
chub get <confirmed-id> --lang <language>
```

Search results identify entries, not passages from every reference file. Inspect
the entry's source, language, available versions, and companion files. Never
invent an entry ID or assume a similarly named library is the intended one.

For this user's Go, HTMX, Fyne, SQLite, PostgreSQL, or clipboard packs, read
[local-context-hub.md](references/local-context-hub.md) for configured sources
and local entry IDs. Prefer a relevant configured local pack for the user's
project guidance, then verify its fit to the target version.

Always pass the intended language for documentation, including `--lang go` for
the custom packs. Use `--version` only for a version listed by that entry. If the
project's version is absent, label any nearby-version guidance and check exact
API behavior against the corresponding official docs or installed source.

Fetch the entry point first, then the files needed for the task:

```sh
chub get <confirmed-id> --lang <language> --file references/<listed-file>.md
```

Use `--full` when the task needs the entire pack. If IDs collide across sources,
use the configured `source-name:author/entry` form. Broaden an unsuccessful search
once; if coverage is still absent or unsuitable, retrieve official documentation
instead of repeating searches or guessing.

## Apply and verify

- Read the retrieved content before coding. For exact Go APIs, supplement the
  guide with `go doc <package> <symbol>` or the project's selected module source.
- For missing, disputed, or newly changed behavior, consult the official docs,
  tagged source, or release notes for the relevant version. Identify unresolved
  version differences in the answer.
- Keep project guidance distinct from upstream API facts. Do not upgrade an
  application's dependencies merely to match a documentation pack.

## Preserve useful findings

Read existing notes with `chub annotate <confirmed-id>` before saving a verified,
reusable finding with `chub annotate <confirmed-id> "<note>"`. Preserve existing
useful notes when merging: this CLI can replace an entry's whole annotation.
Include the affected version when relevant and keep secrets out of annotations.
Keep detailed project-specific guidance in the project's own documentation.

Annotation display differs by CLI version. Check supported options before using
`--with-annotations`; the installed 0.1.4 CLI includes notes automatically and
does not support that flag. Verify old observations against current evidence.

Submit `chub feedback` only when the user has requested or already authorized
external feedback. Exclude private code, credentials, and project details.

Upstream skill: https://github.com/andrewyng/context-hub/blob/main/cli/skills/get-api-docs/SKILL.md
