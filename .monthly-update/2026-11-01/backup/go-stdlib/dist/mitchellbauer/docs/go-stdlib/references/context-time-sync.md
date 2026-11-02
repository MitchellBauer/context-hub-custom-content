# context, time, and sync

## `context`

Use `context.Context` to carry cancellation, deadlines, and request-scoped values
through handlers, DB queries, and downstream calls.

## `time`

Use `time` for durations, deadlines, timestamps, TTL behavior, and periodic cleanup work.

## `sync`

Use `sync.Mutex` or `sync.RWMutex` when shared in-memory state truly needs locking.

## Practical pattern

These packages often work together in application infrastructure:

- request comes in with context
- DB query uses that context
- cache/session cleanup uses `time.Ticker`
- shared state uses `sync` safely
