# Z-08 build shell: dot-source this in a PowerShell session to use the Q-00 toolchain pins in that session only.
#   . .\z08_build_shell.ps1
# It prepends the per-user Node 26.12.1 and pnpm 12.14.0 (fetched by z08_toolchain.py) to PATH for the current
# process. Nothing global changes: the system Node and the npm-installed pnpm stay as they are in other shells.
$tools = if ($env:ZAIN_TOOLS) { $env:ZAIN_TOOLS } else { 'D:\zain-build\tools' }
$node = Join-Path $tools 'node-v26.12.1-win-x64\node-v26.12.1-win-x64'
$pnpm = Join-Path $tools 'pnpm-12.14.0'
foreach ($p in $node, $pnpm) { if (-not (Test-Path $p)) { throw "missing $p; run z08_toolchain.py first" } }
$env:PATH = "$node;$pnpm;" + $env:PATH
"build shell: node $(& node --version), pnpm $(& pnpm --version)"
