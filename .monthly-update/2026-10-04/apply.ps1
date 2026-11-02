$ErrorActionPreference = 'Stop'
$targetRoot = 'C:\GitHubProjects\Context-Hub-Custom-Content'
$stageRoot = Join-Path $PSScriptRoot 'staged'
$backupRoot = Join-Path $PSScriptRoot 'backup'
$manifest = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'manifest.json') -Raw | ConvertFrom-Json
$files = @($manifest | ForEach-Object { $_.path })
foreach ($pack in @('HTMX-GO', 'HTMX-GO-Beta', 'go-stdlib', 'fyne-go', 'postgres-go', 'sqlite-go')) {
    $files += Get-ChildItem -LiteralPath (Join-Path $stageRoot "$pack\dist") -File -Recurse | ForEach-Object { [IO.Path]::GetRelativePath($stageRoot, $_.FullName) }
}
foreach ($relative in $files) {
    $resolved = [IO.Path]::GetFullPath((Join-Path $targetRoot $relative))
    if (-not $resolved.StartsWith($targetRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw "Path outside BYOD folder: $relative" }
}
# Check every source fingerprint before modifying any installed file.
foreach ($entry in $manifest) {
    $target = Join-Path $targetRoot $entry.path
    if ($null -ne $entry.before_sha256) {
        if (-not (Test-Path -LiteralPath $target)) { throw "Source disappeared: $target" }
        if ((Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash.ToLowerInvariant() -ne $entry.before_sha256) { throw "Source changed since review: $target" }
    } elseif (Test-Path -LiteralPath $target) { throw "New target already exists: $target" }
}
foreach ($relative in $files) {
    $target = Join-Path $targetRoot $relative
    $source = Join-Path $stageRoot $relative
    if (Test-Path -LiteralPath $target) {
        $backup = Join-Path $backupRoot $relative
        New-Item -ItemType Directory -Path (Split-Path $backup -Parent) -Force | Out-Null
        Copy-Item -LiteralPath $target -Destination $backup
    }
    New-Item -ItemType Directory -Path (Split-Path $target -Parent) -Force | Out-Null
    Copy-Item -LiteralPath $source -Destination $target -Force
}
foreach ($relative in $files) {
    if ((Get-FileHash -LiteralPath (Join-Path $stageRoot $relative)).Hash -ne (Get-FileHash -LiteralPath (Join-Path $targetRoot $relative)).Hash) { throw "Installed content mismatch: $relative" }
}
Write-Output "Applied and verified $($files.Count) source and registry files. Originals backed up in $backupRoot."
