# Shared CLI path resolution for dazi.ps1 and doctor-cli.ps1

function Get-DaziWorkspaceRoot {
  if ($env:DAZI_WORKSPACE_ROOT -and (Test-Path $env:DAZI_WORKSPACE_ROOT)) {
    return [System.IO.Path]::GetFullPath($env:DAZI_WORKSPACE_ROOT)
  }
  $root = Join-Path $PSScriptRoot ".."
  return (Resolve-Path $root).Path
}

function Get-DaziV3ExtensionPrefix {
  # 勿用 $script:：本文件被 dot-source 时 $script: 指向调用方，会导致前缀为空、-Filter 变成 *
  return "dazitech.dazi-vscode"
}

function Get-DaziExtensionSearchRoots {
  $roots = [System.Collections.Generic.List[object]]::new()
  $seen = @{}

  function Add-Root([string]$Label, [string]$Path) {
    if (-not $Path) { return }
    try {
      $abs = [System.IO.Path]::GetFullPath($Path)
    } catch { return }
    if ($seen.ContainsKey($abs)) { return }
    $seen[$abs] = $true
    $roots.Add([PSCustomObject]@{ Label = $Label; Path = $abs }) | Out-Null
  }

  if ($env:DAZI_EXTENSIONS_DIR) {
    Add-Root "env:DAZI_EXTENSIONS_DIR" $env:DAZI_EXTENSIONS_DIR
  }
  if ($env:VSCODE_EXTENSIONS) {
    Add-Root "env:VSCODE_EXTENSIONS" $env:VSCODE_EXTENSIONS
  }
  if ($env:CURSOR_EXTENSIONS) {
    Add-Root "env:CURSOR_EXTENSIONS" $env:CURSOR_EXTENSIONS
  }

  $profile = $env:USERPROFILE
  if ($profile) {
    Add-Root "trae-extension"      (Join-Path $profile ".trae\extensions")
    Add-Root "cursor-extension"    (Join-Path $profile ".cursor\extensions")
    Add-Root "vscode-extension"    (Join-Path $profile ".vscode\extensions")
  }

  return $roots
}

function Find-DaziV3ExtensionInstalls {
  param([string]$ExtensionsRoot)

  if (-not (Test-Path $ExtensionsRoot)) { return @() }

  # 必须用 -Filter：仅匹配 dazitech.dazi-vscode-*，避免其它扩展的 bundled/ 目录误入
  $prefix = Get-DaziV3ExtensionPrefix
  return @(Get-ChildItem -Path $ExtensionsRoot -Directory -Filter "$prefix*" -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending)
}

function Find-LegacyDaziExtensionInstalls {
  param([string]$ExtensionsRoot)

  if (-not (Test-Path $ExtensionsRoot)) { return @() }

  return @(Get-ChildItem -Path $ExtensionsRoot -Directory -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -like "dazi.dazi-agent-vscode*" -or $_.Name -like "dazitech.dazi-agent-vscode*" } |
    Sort-Object LastWriteTime -Descending)
}

function Get-DaziBundledCliCandidates {
  param([string]$WorkspaceRoot)

  $list = @()

  if ($env:DAZI_BUNDLED_DIR) {
    $p = [System.IO.Path]::GetFullPath($env:DAZI_BUNDLED_DIR)
    $list += [PSCustomObject]@{
      Source = "env:DAZI_BUNDLED_DIR"
      Path   = $p
      Ok     = (Test-Path (Join-Path $p "dazi.js"))
      Note   = ""
    }
  }

  $packaged = Join-Path $WorkspaceRoot "tools\dazi-clis"
  $packagedNote = ""
  if ((Test-Path $packaged) -and -not (Test-Path (Join-Path $packaged "dazi.js"))) {
    $packagedNote = "folder exists but dazi.js missing (copy 4 js files or run sync-clis-from-extension.ps1)"
  }
  $list += [PSCustomObject]@{
    Source = "tools/dazi-clis"
    Path   = $packaged
    Ok     = (Test-Path (Join-Path $packaged "dazi.js"))
    Note   = $packagedNote
  }

  foreach ($er in (Get-DaziExtensionSearchRoots)) {
    if (-not (Test-Path $er.Path)) {
      $list += [PSCustomObject]@{
        Source = $er.Label
        Path   = $er.Path
        Ok     = $false
        Note   = "dir missing"
      }
      continue
    }

    $v3Dirs = Find-DaziV3ExtensionInstalls -ExtensionsRoot $er.Path
    if (-not $v3Dirs) {
      $legacy = Find-LegacyDaziExtensionInstalls -ExtensionsRoot $er.Path
      $note = "no $(Get-DaziV3ExtensionPrefix)* under $($er.Path)"
      if ($legacy) {
        $note = "found v2 $($legacy[0].Name) only (v3 CLI needs dazitech.dazi-vscode + bundled/clis)"
      }
      $list += [PSCustomObject]@{
        Source = $er.Label
        Path   = $er.Path
        Ok     = $false
        Note   = $note
      }
      continue
    }

    foreach ($dir in $v3Dirs) {
      $clis = Join-Path $dir.FullName "bundled\clis"
      $daziJs = Join-Path $clis "dazi.js"
      $ver = $dir.Name.Substring((Get-DaziV3ExtensionPrefix).Length).TrimStart('-')
      $note = $dir.FullName
      if (-not (Test-Path $daziJs)) {
        $note = "$($dir.FullName) | bundled/clis/dazi.js missing (reinstall vsix built with pnpm run vsix)"
      }
      $list += [PSCustomObject]@{
        Source = "$($er.Label) v$ver"
        Path   = $clis
        Ok     = (Test-Path $daziJs)
        Note   = $note
      }
    }
  }

  return $list
}

function Find-DaziBundledCliDirDeep {
  foreach ($er in (Get-DaziExtensionSearchRoots)) {
    if (-not (Test-Path $er.Path)) { continue }
    $hit = Get-ChildItem -Path $er.Path -Recurse -Filter "dazi.js" -Depth 5 -ErrorAction SilentlyContinue |
      Where-Object {
        $_.DirectoryName -match '[\\/]bundled[\\/]clis$' -and
        $_.DirectoryName -match [regex]::Escape((Get-DaziV3ExtensionPrefix))
      } |
      Select-Object -First 1
    if ($hit) { return $hit.DirectoryName }
  }
  return $null
}

function Resolve-DaziBundledCliDir {
  param([string]$WorkspaceRoot)
  foreach ($c in (Get-DaziBundledCliCandidates -WorkspaceRoot $WorkspaceRoot)) {
    if ($c.Ok) { return $c.Path }
  }
  return Find-DaziBundledCliDirDeep
}

function Write-DaziCliNotFoundHelp {
  param([string]$WorkspaceRoot)

  Write-Host ""
  Write-Host "dazi.js not found (bundled CLI)." -ForegroundColor Red
  Write-Host "Workspace: $WorkspaceRoot"
  Write-Host ""
  Write-Host "Checked locations:" -ForegroundColor Yellow
  foreach ($c in (Get-DaziBundledCliCandidates -WorkspaceRoot $WorkspaceRoot)) {
    $mark = if ($c.Ok) { "[OK]" } else { "[--]" }
    $line = "  $mark $($c.Source): $($c.Path)"
    if ($c.Note) { $line += " | $($c.Note)" }
    Write-Host $line
  }
  Write-Host ""
  Write-Host "Fix (pick one):" -ForegroundColor Cyan
  Write-Host "  1. Install dazitech.dazi-vscode.vsix in Trae/Cursor, then:"
  Write-Host "     .\scripts\sync-clis-from-extension.ps1"
  Write-Host "  2. Copy bundled/clis/*.js (4 files) to:"
  Write-Host "     $WorkspaceRoot\tools\dazi-clis\"
  Write-Host "  3. Set env (current session):"
  Write-Host '     $env:DAZI_BUNDLED_DIR = "<path>\bundled\clis"'
  Write-Host "  4. Run: .\scripts\doctor-cli.ps1"
  Write-Host ""
}

function Get-DaziRuntimeAppsRoot {
  param([string]$WorkspaceRoot)

  $candidates = @()
  if ($env:DAZI_RUNTIME_APPS_ROOT) {
    $candidates += $env:DAZI_RUNTIME_APPS_ROOT
  }
  $candidates += (Join-Path $WorkspaceRoot "runtime-apps")

  foreach ($p in $candidates) {
    if (-not $p) { continue }
    $abs = [System.IO.Path]::GetFullPath($p)
    $t = Join-Path $abs "templates"
    $s = Join-Path $abs "sdk"
    if ((Test-Path $t) -and (Test-Path $s)) { return $abs }
  }
  return $null
}

function Resolve-DaziAppCliEntry {
  param(
    [string]$RuntimeAppsRoot,
    [string]$BundledCliDir
  )

  if ($BundledCliDir) {
    $p = Join-Path $BundledCliDir "dazi-app.js"
    if (Test-Path $p) {
      return [PSCustomObject]@{ Source = "bundled"; Path = $p; IsLauncher = $false }
    }
  }

  if ($RuntimeAppsRoot) {
    $wsTools = Join-Path (Split-Path $RuntimeAppsRoot -Parent) "tools\dazi-clis"
    $p2 = Join-Path $wsTools "dazi-app.js"
    if (Test-Path $p2) {
      return [PSCustomObject]@{ Source = "tools/dazi-clis"; Path = $p2; IsLauncher = $false }
    }
    $launcher = Join-Path $RuntimeAppsRoot "cli\bin\dazi-app.mjs"
    if (Test-Path $launcher) {
      return [PSCustomObject]@{ Source = "runtime-apps launcher"; Path = $launcher; IsLauncher = $true }
    }
  }

  return $null
}
