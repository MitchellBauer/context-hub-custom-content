---
name: windows-service-go
description: "golang.org/x/sys/windows/svc guide: run a Go program as a Windows service, install it, event log"
metadata:
  languages: "go"
  versions: "0.48.0"
  revision: 1
  updated-on: "2026-11-01"
  source: community
  tags: "windows,service,svc,golang-x-sys,eventlog,mgr,go"
---

# Windows services in Go

`golang.org/x/sys/windows/svc` runs a Go program under the Windows Service
Control Manager (SCM). Related packages:

- `svc`: the handler interface, `svc.Run`, `svc.IsWindowsService`.
- `svc/mgr`: install, configure, start, stop and delete services.
- `svc/eventlog`: write to the Windows Application event log.

Put this code in files ending `_windows.go` (or with `//go:build windows`) so
the rest of the module still builds on other systems.

## One binary, console or service

```go
func main() {
    if ok, err := svc.IsWindowsService(); err == nil && ok {
        _ = svc.Run("MyService", &handler{}) // blocks until the service stops
        return
    }
    // otherwise run in the console with the same server code
}
```

`svc.IsWindowsService()` is the supported way to detect it (the older
`IsAnInteractiveSession` is deprecated).

## The handler

```go
type handler struct{}

func (h *handler) Execute(args []string, req <-chan svc.ChangeRequest, status chan<- svc.Status) (svcSpecificEC bool, exitCode uint32) {
    status <- svc.Status{State: svc.StartPending}
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()
    done := make(chan error, 1)
    go func() { done <- serve(ctx) }()

    status <- svc.Status{State: svc.Running, Accepts: svc.AcceptStop | svc.AcceptShutdown}
    for {
        select {
        case <-done: // server died by itself
            return true, 1 // non-zero so recovery actions restart it
        case c := <-req:
            switch c.Cmd {
            case svc.Interrogate:
                status <- c.CurrentStatus
            case svc.Stop, svc.Shutdown:
                status <- svc.Status{State: svc.StopPending}
                cancel()
                select { case <-done: case <-time.After(15 * time.Second): }
                return false, 0
            }
        }
    }
}
```

Rules:

- Report `Running` quickly. The SCM gives startup about 30 seconds; do slow
  work (network, DB) in the goroutine, not before `Running`.
- Always handle `Interrogate`, `Stop` and `Shutdown`.
- A graceful stop cancels a context; give it a bounded wait.
- Return `true, nonZero` when the server stops on its own, so failure actions
  can restart it.
- The working directory is `C:\Windows\System32`. Resolve every path from the
  executable or from an absolute config path passed at install time.

## Installing with mgr

Needs an **elevated** (administrator) process. `mgr.Connect` returns
`windows.ERROR_ACCESS_DENIED` otherwise; turn that into a clear message.

```go
m, err := mgr.Connect()
defer m.Disconnect()

s, err := m.CreateService("MyService", exePath, mgr.Config{
    DisplayName:      "My Service",
    Description:      "What it does and where its logs are.",
    StartType:        mgr.StartAutomatic,
    DelayedAutoStart: true, // after boot settles, network up
    ServiceStartName: "LocalSystem",
}, "-config", `C:\app\config.json`) // arguments after the config become the command line
defer s.Close()

_ = s.SetRecoveryActions([]mgr.RecoveryAction{
    {Type: mgr.ServiceRestart, Delay: 5 * time.Second},
    {Type: mgr.ServiceRestart, Delay: 5 * time.Second},
    {Type: mgr.ServiceRestart, Delay: 30 * time.Second},
}, uint32((24 * time.Hour).Seconds())) // reset failure count after a day
_ = s.SetRecoveryActionsOnNonCrashFailures(true) // also restart on exit code != 0

_ = eventlog.InstallAsEventCreate("MyService", eventlog.Error|eventlog.Warning|eventlog.Info)
```

- Pass absolute paths in the arguments; the service does not start where you
  installed it from.
- `CreateService` fails if the name exists. Check `m.OpenService(name)` first.
- `LocalSystem` is powerful; use a dedicated account (set `ServiceStartName`
  and `Password`) when the service does not need it.

## Control and status

```go
s, _ := m.OpenService("MyService")
_ = s.Start()
st, _ := s.Control(svc.Stop)          // returns current status
st, _ = s.Query()                     // poll until st.State == svc.Stopped
_ = s.Delete()                        // marks for deletion; goes away when stopped
_ = eventlog.Remove("MyService")
```

Poll `Query()` with a short sleep and a limit rather than assuming the state
changed. A service that returns to `svc.Stopped` right after `Start` crashed
at startup: check the log file and the Application event log.

## Event log

```go
elog, err := eventlog.Open("MyService")
defer elog.Close()
_ = elog.Info(1, "started")
_ = elog.Error(1, "stopped unexpectedly")
```

The source must be registered once (`InstallAsEventCreate`, done at install).
Treat logging failures as non-fatal. Also keep a plain log file next to the
config for field debugging.

## Gotchas

- `svc.Run` only works when started by the SCM. Run the same code in the
  console for development.
- Do not write to a console in service mode; there is none.
- Replacing the `.exe` while the service runs fails on Windows. Update by
  stop, replace, start (a watcher script can do this).
- Do not call `os.Exit` from the server: it skips the `Stopped` status report.
