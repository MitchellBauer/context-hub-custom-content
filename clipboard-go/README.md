# clipboard-go BYOD Pack

This directory is a Bring Your Own Docs pack for the clipboard dependencies used by the Context project.

## What this gives you

After you build this pack and add it to Context Hub, `chub` can search and fetch the clipboard dependency docs locally instead of you pasting them into chat by hand.

## Folder structure

```text
clipboard-go/
  mitchellbauer/
    docs/
      clipboard-dependencies/
        DOC.md
        references/
          windows-win32.md
          macos-pbcopy.md
          linux-clipboard-tools.md
```

This matches the BYOD structure from the Context Hub docs:

- `author/docs/<entry>/DOC.md`
- optional `references/` files for deeper detail

## Step 1: Validate the content pack

```powershell
chub build '.\clipboard-go\' --validate-only
```

## Step 2: Build the local registry output

```powershell
chub build '.\clipboard-go\' -o '.\clipboard-go\dist\'
```

## Step 3: Add it to Context Hub config

Add the built output as a local source in `~/.chub/config.yaml`:

```yaml
sources:
  - name: community
    url: https://cdn.aichub.org/v1
  - name: local-clipboard-go
    path: C:/GitHubProjects/Context-Hub-Custom-Content/clipboard-go/dist
```

## Step 4: Use it from Context Hub

```powershell
chub search "clipboard"
chub get mitchellbauer/clipboard-dependencies
chub get mitchellbauer/clipboard-dependencies --full
```

## BYOD summary

The Context Hub BYOD flow is:

1. Create a local content repo with `author/docs/<entry>/DOC.md`
2. Run `chub build` to produce `dist/`
3. Add `dist/` as a `path:` source in `~/.chub/config.yaml`
4. Use `chub search` and `chub get` against that local source

This folder is already set up for that workflow.

The pack remains version `1.0.0` because the covered operating-system APIs and
tools do not share a release version. Revision 2 refreshes platform-selection
guidance and removes machine-specific source links.


