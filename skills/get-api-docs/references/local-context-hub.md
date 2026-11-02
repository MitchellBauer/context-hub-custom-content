# This user's local Context Hub sources

Configuration: `C:\Users\Mitchell Bauer\.chub\config.yaml`.
Documentation workspace: `C:\GitHubProjects\Context-Hub-Custom-Content`.

Read the current configuration if a source is unavailable or its location is
uncertain. Chub reads configured local `path:` sources directly; GitHub hosting
does not make it pull or synchronize a repository automatically.

## Entry lookup

Confirm these entries with `chub search <id> --json` before fetching. Determine
the version from the current registry rather than this reference.

| Subject | Entry ID | Configured local source |
| --- | --- | --- |
| Go standard library | `mitchellbauer/go-stdlib` | `local-go-stdlib` |
| HTMX 2 | `mitchellbauer/htmx` | `local-htmx-go` |
| HTMX 4 | `mitchellbauer/htmx-go` | `local-htmx-go-beta` |
| Fyne | `mitchellbauer/fyne-go` | `local-fyne-go` |
| modernc.org/sqlite | `mitchellbauer/sqlite-go` | `local-sqlite-go` |
| PostgreSQL / pgx | `mitchellbauer/postgres-go` | `local-postgres-go` |
| Clipboard APIs and tools | `mitchellbauer/clipboard-dependencies` | `local-clipboard-go` |

`mitchellbauer/htmx-go-beta` is a compatibility entry for the stable HTMX 4
guidance. The historical source/folder name does not establish prerelease
status. Confirm the app's actual HTMX major version before choosing a pack.

Example:

```sh
chub search mitchellbauer/go-stdlib --json
chub get mitchellbauer/go-stdlib --lang go
chub get mitchellbauer/go-stdlib --lang go --file references/net-http.md
```

## When documentation maintenance is requested

Work from the documentation workspace and follow its `AGENTS.md`. Store update
scripts, evidence, staging files, and backups under `.monthly-update/YYYY-MM-DD/`
there. The sibling `C:\GitHubProjects\Context` is an older application and is
not the documentation maintenance workspace.

Edit pack sources, then validate and rebuild the affected pack into its `dist/`
directory. Check exact search and retrieval after rebuilding. `chub update`
refreshes remote registries; it does not rebuild or pull local packs.
