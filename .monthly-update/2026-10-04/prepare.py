from pathlib import Path
import re, shutil, json, hashlib

root = Path(__file__).parent / 'staged'
original = Path(r'C:\GitHubProjects\Context-Hub-Custom-Content')
packs = ['HTMX-GO', 'HTMX-GO-Beta', 'go-stdlib', 'fyne-go', 'postgres-go', 'sqlite-go']
date = '2026-10-04'

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + '\n', encoding='utf-8')

def replace(path, old, new):
    text = path.read_text(encoding='utf-8')
    assert old in text, (path, old)
    write(path, text.replace(old, new))

def doc(pack, name):
    return root / pack / 'mitchellbauer/docs' / name

def metadata(path, version):
    text = path.read_text(encoding='utf-8')
    text = re.sub(r'  versions: .*', f'  versions: "{version}"', text)
    text = re.sub(r'  revision: (\d+)', lambda m: f'  revision: {int(m[1])+1}', text)
    text = re.sub(r'  updated-on: .*', f'  updated-on: "{date}"', text)
    write(path, text)

# Retain the configured source directory and old lookup ID; add a stable ID.
h4 = doc('HTMX-GO-Beta', 'htmx-go-beta')
metadata(h4/'DOC.md', '4.0.0')
for path in [h4/'DOC.md', h4/'references/migration-from-v2.md', h4/'references/go-patterns.md', h4/'references/attributes-and-events.md', h4/'references/headers.md']:
    text = path.read_text(encoding='utf-8').replace('4.0.0-beta6', '4.0.0')
    text = text.replace('HTMX 4 Beta', 'HTMX 4').replace('## Install beta6', '## Install 4.0.0').replace('## Go-specific beta rules', '## Go-specific rules')
    text = text.replace('HTMX 4.0.0 pre-release guide', 'HTMX 4.0.0 stable guide')
    text = text.replace('htmx,go,beta,prerelease,', 'htmx,go,stable,')
    text = text.replace('HTMX 4 is under construction. Keep production HTMX 2.x applications on the\nstable `mitchellbauer/htmx` entry unless the project has intentionally opted\ninto the beta and tested its migration.', 'HTMX 4.0.0 was released on August 28, 2026. Existing HTMX 2 applications\nshould use `mitchellbauer/htmx` until their migration has been tested.\nThe stable HTMX 4 lookup is `mitchellbauer/htmx-go`; this older ID remains\navailable for compatibility with existing callers.')
    text = text.replace('sha384-6lyVbhrs13b9z7mLOpt/N6R76rtkEBWgCjAXRs/DSWyi2AMnQSs10ijWk+PI8n7W', 'sha384-BvJpBiO8Kh31EqtJe5DRIeWrHWnCGkwytKs9NKFi86Hhw96dEqdEMzZDeK9iEGTc')
    text = text.replace('into the beta', 'into HTMX 4').replace('## Beta isolation', '## Version isolation').replace('Keep beta templates', 'Keep HTMX 4 templates').replace('Do not infer beta adoption', 'Do not infer HTMX 4 adoption')
    text = text.replace('stable HTMX\n2 applications', 'HTMX\n2 applications')
    text = text.replace('`hx-prompt`: use `hx-confirm` with `js:`', '`hx-prompt`: load the `hx-prompt` extension to retain prompt input')
    text = text.replace('`HX-Prompt`: use `hx-confirm` with `js:`', '`HX-Prompt`: restored by the `hx-prompt` extension when needed')
    text = text.replace('`hx-encoding`', '`hx-encode`')
    text = text.replace('Beta6 specifically renamed', 'During the beta series, HTMX renamed').replace('`hx-multipart` beta6 extension', '`hx-multipart` extension').replace('In beta6, events', 'Events')
    text = text.replace('references/beta6-release-notes.md', 'references/htmx-4.0.0-release-notes.md')
    write(path, text)
write(h4/'references/htmx-4.0.0-release-notes.md', '''
# HTMX 4.0.0 Release Notes

Released August 28, 2026; first stable HTMX 4 release. The npm `latest` tag
continues to select HTMX 2, so install `htmx.org@4.0.0` explicitly.

## Changes since beta6

- `hx-query` provides a core shorthand for QUERY requests.
- SSE, WebSocket, and multipart streaming behavior and event conventions were refined.
- Multipart streams gained resume cursors and connection details.
- `htmx.initialize()` supports asynchronous initialization.
- Requests made with `htmx.ajax()` support abort events.
- `<hx-partial>` accepts extended selectors.
- Array-valued custom elements submit repeated fields.

Go routes and middleware must explicitly allow QUERY if adopted; verify proxy
support before depending on it. Test reconnects, cancellation, and incomplete
streams before introducing streaming responses.

## Sources

- https://github.com/bigskysoftware/htmx/releases/tag/v4.0.0
- https://raw.githubusercontent.com/bigskysoftware/htmx/four/CHANGELOG.md
- https://four.htmx.org/announcements/2026-08-28-htmx-4.0.0-is-released
''')
with (h4/'references/migration-from-v2.md').open('a', encoding='utf-8') as f:
    f.write('''
## Additional migration checks

- DELETE no longer collects enclosing form inputs; add `hx-include="closest form"` when needed.
- Replace `hx-trigger` queuing modifiers with `hx-sync`.
- Quote selectors containing spaces or commas in `from:` and `target:` modifiers.
- Main swaps precede out-of-band swaps; check dependencies between targets.
- History restoration re-fetches pages instead of using a localStorage page cache.
- Rename `hx-encoding` to `hx-encode`.

Source: https://four.htmx.org/docs/whats-new-in-htmx-4
''')
# Beta release notes are historical, not the active release guidance.
replace(h4/'references/beta6-release-notes.md', '# HTMX 4.0.0-beta6 Release Notes', '# HTMX 4.0.0-beta6 Release Notes\n\nHistorical reference only. Current guidance targets 4.0.0; see\n`htmx-4.0.0-release-notes.md`.')
h4stable = doc('HTMX-GO-Beta', 'htmx-go')
shutil.copytree(h4, h4stable, dirs_exist_ok=True)
replace(h4stable/'DOC.md', 'name: htmx-go-beta', 'name: htmx-go')
replace(h4stable/'DOC.md', 'The stable HTMX 4 lookup is `mitchellbauer/htmx-go`; this older ID remains\navailable for compatibility with existing callers.', 'The older `mitchellbauer/htmx-go-beta` ID remains available as a compatibility\nlookup for this stable guidance.')
write(root/'HTMX-GO-Beta/README.md', '''
# HTMX 4 for Go BYOD Pack

Targets stable HTMX 4.0.0, released August 28, 2026.
Use `mitchellbauer/htmx-go` for HTMX 4 and `mitchellbauer/htmx` for HTMX 2.
The `mitchellbauer/htmx-go-beta` lookup remains compatible and returns 4.0.0 guidance.
The historical folder and source names are retained so installed configurations work.

## Validate and build

```powershell
chub build '.\\HTMX-GO-Beta\\' --validate-only
chub build '.\\HTMX-GO-Beta\\' -o '.\\HTMX-GO-Beta\\dist\\'
```

## Context Hub source

```yaml
sources:
  - name: local-htmx-go-beta
    path: C:/GitHubProjects/Context-Hub-Custom-Content/HTMX-GO-Beta/dist
```

## Use it

```powershell
chub get mitchellbauer/htmx-go --lang go
chub get mitchellbauer/htmx-go --lang go --full
chub get mitchellbauer/htmx-go --lang go --file references/migration-from-v2.md
```

Pin the exact JavaScript version and test the migration before upgrading an app.
''')

h2 = doc('HTMX-GO', 'htmx')
metadata(h2/'DOC.md', '2.0.11')
replace(root/'HTMX-GO/README.md', 'pinned to HTMX 2.0.9', 'pinned to HTMX 2.0.11')
write(h2/'references/version-notes.md', '''
# HTMX Version Notes

This entry targets HTMX 2.0.11 (September 22, 2026) for applications staying on 2.x.
HTMX 4.0.0 is stable, but has breaking changes; use `mitchellbauer/htmx-go`
for its separate migration and Go handler guidance.

HTMX 2.0.10 restored missing TypeScript declarations and improved selector
escaping. HTMX 2.0.11 backports `<hx-partial>` and fixes boosted history settings,
response header matching, and detached out-of-band targets.

Historical 2.0.9 notes remain in `release-deltas/htmx-2.0.9.md`.
Current delta: `release-deltas/htmx-2.0.11.md`.

Source: https://raw.githubusercontent.com/bigskysoftware/htmx/master/CHANGELOG.md
''')
write(h2/'release-deltas/htmx-2.0.11.md', '''
# HTMX 2.0.11 Delta

Released September 22, 2026. Updates the previous 2.0.9 pack through 2.0.10.

- `<hx-partial hx-target="...">` in a response can update additional targets.
- Ancestor `hx-push-url="false"` works correctly with boosted descendants.
- Response-header checks avoid substring matches that could cause TypeError.
- Out-of-band targets resolve when the originating element has been detached.
- The intervening 2.0.10 release restores TypeScript declarations and improves settle selector escaping.

Existing 2.x Go request detection and response conventions remain applicable.
Do not apply HTMX 4 inheritance or event conventions to 2.x templates.

Source: https://raw.githubusercontent.com/bigskysoftware/htmx/master/CHANGELOG.md
''')

go = doc('go-stdlib', 'go-stdlib')
metadata(go/'DOC.md', '1.27.1')
write(go/'release-deltas/go1.27.1.md', '''
# Go 1.27.1 Delta

Go 1.27.0 was released August 19, 2026; 1.27.1 followed September 1.
This is a documentation target, not a claim that the local toolchain was upgraded.
The maintained 1.26 branch is at 1.26.8. Its intervening releases include security
fixes; read the official release history when remaining on that branch.

## Application-facing changes

- `database/sql.ConvertAssign` exposes scanning conversions to drivers.
- Drivers can implement `database/sql/driver.RowsColumnScanner` for direct destination scanning.
- HTTP/1 response bodies drain a bounded amount on close to improve connection reuse.
- `http.Server.MaxHeaderValueCount` controls the number of accepted header values.
- `httptest.NewTestServer` works with an in-memory network and `testing/synctest`.
- `crypto/tls.Config.Rand` is deprecated; several old TLS GODEBUG compatibility switches were removed.
- Go 1.27 requires macOS 13 or newer.

1.27.1 fixes the compiler, runtime, cgo, go fix, and several packages including
database/sql, encoding/json, and net/http. Existing handler/template/repository
patterns remain useful; test driver conversions and HTTP client behavior when upgrading.

## Sources

- https://go.dev/doc/go1.27
- https://go.dev/doc/devel/release
''')
for ref, note in {
    'database-sql':'Go 1.27 adds `sql.ConvertAssign` and `driver.RowsColumnScanner`. With pgx\n5.11 on Go 1.27, arrays and ranges can scan directly into Go destinations.\nTest application-specific scanning conversions when upgrading.',
    'net-http':'Go 1.27 drains a bounded amount of unread HTTP/1 response content on Close\nfor connection reuse and adds `Server.MaxHeaderValueCount`. Continue closing\nresponse bodies promptly and explicitly configuring reusable transports.',
    'testing':'Go 1.27 adds `httptest.NewTestServer` for in-memory networking with\n`testing/synctest`. Ordinary `httptest.NewServer` remains appropriate for\nexisting handler tests.',
    'crypto-tls':'Go 1.27 deprecates `tls.Config.Rand` and removes older TLS compatibility\nGODEBUG settings, including tlsrsakex, tls3des, tls10server, and tlsunsafeekm.\nReview any deployment that explicitly sets those switches.'
}.items():
    with (go/f'references/{ref}.md').open('a', encoding='utf-8') as f:
        f.write(f'\n## Go 1.27 update\n\n{note}\n\nSee `release-deltas/go1.27.1.md` and https://go.dev/doc/go1.27.\n')
replace(root/'go-stdlib/README.md', 'Current delta: `release-deltas/go1.26.5.md`', 'Current delta: `release-deltas/go1.27.1.md`')
replace(root/'go-stdlib/README.md', '--file release-deltas\\go1.26.5.md', '--file release-deltas\\go1.27.1.md')

fyne = doc('fyne-go', 'fyne-go')
metadata(fyne/'DOC.md', '2.8.1')
replace(root/'fyne-go/README.md', 'covers Fyne v2.8.0', 'covers Fyne v2.8.1')
replace(fyne/'references/version-notes.md', '## Current version: v2.8.0 (July 2026)', '## Current version: v2.8.1 (August 26, 2026)\n\nSee `release-deltas/fyne-2.8.1.md` for fixes since 2.8.0.\nThe 2.8 migration notes below still apply.')
write(fyne/'release-deltas/fyne-2.8.1.md', '''
# Fyne 2.8.1 Delta

Released August 26, 2026. Keeps the Fyne v2 import path and 2.8 migration rules.

The update improves repaint performance and fixes Windows file URI handling,
menu refresh, popup dismissal, and forms whose widgets are replaced. It also
addresses Wayland keyboard/systray behavior, mobile input, and float binding
parse failures. File dialogs now use padded content; the large fyne.Do warning
is delayed unless hints are enabled.

Test file selection, dynamically replaced form widgets, menus, and background
GUI updates on the platforms the app actually supports.

Source: https://github.com/fyne-io/fyne/releases/tag/v2.8.1
''')

sqlite = doc('sqlite-go', 'sqlite-go')
metadata(sqlite/'DOC.md', '1.60.1')
replace(root/'sqlite-go/README.md', 'targets `modernc.org/sqlite` v1.54.0', 'targets `modernc.org/sqlite` v1.60.1 (Go 1.26 or newer)')
replace(sqlite/'references/modernc-driver.md', 'driver version `1.54.0`, which embeds SQLite `3.53.3`', 'driver version `1.60.1`, which embeds SQLite `3.53.4`')
replace(sqlite/'references/modernc-driver.md', 'sqlite@v1.54.0', 'sqlite@v1.60.1')
with (sqlite/'references/modernc-driver.md').open('a', encoding='utf-8') as f:
    f.write('\n## Current upgrade requirements\n\nVersion 1.60.1 requires Go 1.26 and pins modernc.org/libc v1.77.1.\nUse `file:` URIs for SQLite URI options such as `mode=ro`; a plain\nfilename with `?mode=ro` does not enforce read-only access.\nSee `release-deltas/modernc-sqlite-1.60.1.md` before upgrading.\n')
write(sqlite/'references/version-notes.md', '''
# SQLite Driver Version Notes

Target: modernc.org/sqlite 1.60.1, released September 29, 2026.
Bundled engine: SQLite 3.53.4. Requires Go 1.26 or newer and the driver's
matching modernc.org/libc version, v1.77.1.

The blank import and `database/sql` pattern remain applicable. This pack's target
does not upgrade any application's go.mod. Check each app's declared version
and database tests before adopting it.

Read `release-deltas/modernc-sqlite-1.60.1.md` for upgrade-sensitive behavior.
The earlier 1.54.0 delta remains a historical reference.

Sources:

- https://pkg.go.dev/modernc.org/sqlite@v1.60.1
- https://proxy.golang.org/modernc.org/sqlite/@v/v1.60.1.mod
- https://gitlab.com/cznic/sqlite/-/raw/v1.60.1/CHANGELOG.md
''')
write(sqlite/'release-deltas/modernc-sqlite-1.60.1.md', '''
# modernc.org/sqlite 1.60.1 Delta

Updated from 1.54.0 through September 29, 2026.

- Requires Go 1.26; match modernc.org/libc v1.77.1 from the driver's go.mod.
- Bundles SQLite 3.53.4, including the upstream multi-database journal recovery fix.
- 1.60.1 improves argument binding for statements with many parameters.
- 1.60.0 converts memory-mapped WAL shared-memory faults into an I/O error.
- VFS close rejects active databases: close database connections before the VFS.
- Some invalid exported lib constants were removed; audit direct lib imports.
- Invalid custom page-cache implementations now panic; callbacks have stricter lifetime requirements.
- Driver-specific virtual-table registration honors the supplied database's driver.
- Optional StrictPragmas rejects multi-statement `_pragma` values. It is off by default.
- Linux OFD locking and `_defensive` mode are opt-in, not automatic defaults.

Check migration, rollback/recovery, pooled connections, and bulk inserts on each
app. Preserve the chosen driver/libc pairing; do not independently bump libc.

Sources:

- https://gitlab.com/cznic/sqlite/-/raw/v1.60.1/CHANGELOG.md
- https://proxy.golang.org/modernc.org/sqlite/@v/v1.60.1.mod
''')

pg = doc('postgres-go', 'postgres-go')
metadata(pg/'DOC.md', '5.11.0')
replace(root/'postgres-go/README.md', 'pgx v5.10.0', 'pgx v5.11.0')
replace(pg/'references/pgx-stdlib.md', '5.10.0', '5.11.0')
write(pg/'references/version-notes.md', '''
# PostgreSQL and pgx Version Notes

Verified October 4, 2026:

- pgx 5.11.0, released September 7, 2026; minimum Go 1.25.
- PostgreSQL 16.15, 17.11, and 18.6, released August 13, 2026.
- PostgreSQL 18.5 was skipped. PostgreSQL 19 remains beta and is outside this pack.

pgx's stdlib import path remains `github.com/jackc/pgx/v5/stdlib`.
Go 1.27 enables direct PostgreSQL array/range scans through database/sql.
Read `release-deltas/pgx-5.11.0.md` for connection-string and date/time changes.

Same-major PostgreSQL updates do not require dump/restore, but the August
release notes include follow-up configuration and data cleanup steps. Review
logical-decoding plugin allowlists, affected pgcrypto data, and extension indexes
before declaring an upgrade complete. Read all intervening notes for older baselines.

Sources:

- https://github.com/jackc/pgx/blob/v5.11.0/CHANGELOG.md
- https://www.postgresql.org/docs/16/release-16-15.html
- https://www.postgresql.org/docs/release/17.11/
- https://www.postgresql.org/docs/release/18.6/
''')
write(pg/'release-deltas/pgx-5.11.0.md', '''
# pgx 5.11.0 Delta

Released September 7, 2026. Minimum Go remains 1.25.

- Go 1.27's RowsColumnScanner lets stdlib scan arrays/ranges directly.
- Custom pgx.Rows implementations and mocks must add TypeMap.
- PostgreSQL date/time parsing rejects impossible dates and out-of-range values.
- Text timestamptz scans now use time.Local or configured ScanLocation, matching binary scans. The instant stays the same, but rendered offsets and JSON can change.
- Connection URI parsing follows libpq more closely: literal plus signs, repeated keys, malformed escapes, and multi-host ports can behave differently.
- Protocol message limits and additional decoder hardening were added.

Test real connection strings, scanner destinations, time zones, and JSON dates.
Configure ScanLocation explicitly when stable date/time rendering is required.

Source: https://github.com/jackc/pgx/blob/v5.11.0/CHANGELOG.md
''')
with (pg/'references/pgx-stdlib.md').open('a', encoding='utf-8') as f:
    f.write('\n## 5.11 upgrade notes\n\nSee `release-deltas/pgx-5.11.0.md`. Direct array/range scanning requires\nGo 1.27; pgx 5.11 itself still supports Go 1.25. Check text timestamptz\nlocations and production connection URI parsing when upgrading.\n')

# Make new release references discoverable from base entries and READMEs.
for pack, name, delta in [('HTMX-GO','htmx','htmx-2.0.11'), ('go-stdlib','go-stdlib','go1.27.1'), ('fyne-go','fyne-go','fyne-2.8.1'), ('sqlite-go','sqlite-go','modernc-sqlite-1.60.1'), ('postgres-go','postgres-go','pgx-5.11.0')]:
    for path in [doc(pack,name)/'DOC.md', root/pack/'README.md']:
        with path.open('a', encoding='utf-8') as f:
            f.write(f'\n## Latest release guidance\n\n- `release-deltas/{delta}.md`\n')

write(root/'UPDATE-2026-10-04.md', '''
# BYOD update — October 4, 2026

| Pack | Previous target | Updated target |
| --- | --- | --- |
| HTMX 4 for Go | 4.0.0-beta6 | 4.0.0 |
| HTMX 2 for Go | 2.0.9 | 2.0.11 |
| Go standard library | 1.26.5 | 1.27.1 |
| Fyne | 2.8.0 | 2.8.1 |
| modernc.org/sqlite | 1.54.0 | 1.60.1 |
| pgx | 5.10.0 | 5.11.0 |
| PostgreSQL | 16.14 / 17.10 / 18.4 | 16.15 / 17.11 / 18.6 |

Release sources and upgrade notes are included in each pack. The new stable
HTMX 4 lookup is `mitchellbauer/htmx-go`. Existing `htmx-go-beta` callers and
the configured source path continue to work. HTMX 2 remains a separate entry.

Clipboard guidance covers operating-system APIs and tools rather than a
versioned application library; its existing content is retained.

These changes update documentation and local registries. App dependencies,
installed Go toolchains, and database servers require their own upgrades.
''')

changes = []
for path in root.rglob('*.md'):
    relative = path.relative_to(root)
    source = original/relative
    old = source.read_bytes() if source.exists() else None
    if old != path.read_bytes():
        changes.append({'path':str(relative), 'before_sha256':hashlib.sha256(old).hexdigest() if old else None})
write(Path(__file__).parent/'manifest.json', json.dumps(changes, indent=2))
print(f'Prepared {len(changes)} updated/new documentation files.')
