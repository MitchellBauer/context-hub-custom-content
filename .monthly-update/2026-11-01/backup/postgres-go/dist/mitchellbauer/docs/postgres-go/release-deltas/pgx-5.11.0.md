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
