# Context Hub custom documentation

This workspace is the home for the user's Context Hub documentation packs and
their maintenance records.

- Perform documentation maintenance from this workspace. The sibling
  `C:\GitHubProjects\Context` repository is an older application, not the
  workspace for Context Hub pack updates.
- Store update scripts, downloaded release evidence, staging files, backups,
  and verification records under `.monthly-update/YYYY-MM-DD/` here.
- Keep pack source material in each pack's `mitchellbauer/docs/` tree and build
  its installed registry into that pack's `dist/` directory.
- Preserve historical update records. The October 4, 2026 archive contains
  scripts and staged content for that specific past update; do not execute
  them to perform a new update.
- Check existing source versions and official release evidence before updating
  a pack. Keep historical release deltas and preserve existing local notes.
- Validate affected packs with `chub build <pack> --validate-only`, rebuild
  them with `chub build <pack> -o <pack>/dist`, and verify exact entry lookup
  and retrieval through the installed CLI.
- Documentation updates do not authorize changing application dependencies,
  installed toolchains, or database servers.
