# pgx 5.12.0 Delta

Changelog dated October 30, 2026; tag timestamp October 31 UTC.
Minimum Go remains 1.25. Updates this pack from 5.11.0.

## Security fixes

- GHSA-j38q-h3ph-jjpq: simple-protocol batches could permit SQL injection when
  a queued query ends with an unterminated line comment and the following query
  contains attacker-controlled string input. Extended-protocol modes are unaffected.
- GHSA-95fj-3fxw-g62g: 5.9.0–5.11.0 could fail to enforce `require_auth` or
  `channel_binding=require` against an impersonating server when server identity
  was not verified. TLS certificate verification itself is not bypassed.

## Compatibility checks

- Custom `BatchResults` implementations and mocks must implement `Tx`.
- New batch transaction startup and client-certificate policy controls are available.
- On Windows, service-file lookup now prefers
  `%APPDATA%\postgresql\.pg_service.conf`.
- Pool cancellation, named arguments, and several PostgreSQL type codecs receive
  fixes. Exercise connection setup and repository tests before application adoption.

Read `release-deltas/pgx-5.11.0.md` as well when upgrading from an older baseline.

Sources:

- [Tagged changelog](https://raw.githubusercontent.com/jackc/pgx/v5.12.0/CHANGELOG.md)
- [Tagged module requirements](https://raw.githubusercontent.com/jackc/pgx/v5.12.0/go.mod)
- [Tag](https://github.com/jackc/pgx/releases/tag/v5.12.0)
