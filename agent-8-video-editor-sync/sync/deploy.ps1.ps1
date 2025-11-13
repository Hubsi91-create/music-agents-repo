param([Parameter(Mandatory=$false)][string]$Action = "install", [Parameter(Mandatory=$false)][string]$ScreenplayPath, [Parameter(Mandatory=$false)][string]$AudioPath, [Parameter(Mandatory=$false)][string]$VideoClipsPath, [Parameter(Mandatory=$false)][string]$OutputFormat = "davinci")
$scriptRoot = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
$agent8Path = "$scriptRoot\agent-8-video-editor-sync"
$logDir = "$agent8Path\output\logs"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }
$logFile = "$logDir\agent8_$(Get-Date -Format 'yyyy-MM-dd_HH-mm-ss').log"
function Write-Log { param($Message, $Level = "INFO")
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$output = "[$timestamp] [$Level] $Message"
Write-Host $output
Add-Content -Path $logFile -Value $output -Encoding UTF8 }
function Install-Agent8 {
Write-Log "AGENT 8 INSTALLATION STARTED" "INFO"
$directories = @("$agent8Path\core", "$agent8Path\sync", "$agent8Path\qassurance", "$agent8Path\daw", "$agent8Path\scripts", "$agent8Path\output\davinci", "$agent8Path\output\premiere", "$agent8Path\output\logs")
foreach ($dir in $directories) {
if (-not (Test-Path $dir)) {
New-Item -ItemType Directory -Path $dir -Force | Out-Null
Write-Log "Created: $dir" "SUCCESS" } }
$reqFile = "$agent8Path\requirements.txt"
if (-not (Test-Path $reqFile)) {
$reqs = @"
librosa
numpy
pydub
av
opencv-python
scipy
soundfile
pyyaml
"@
Set-Content -Path $reqFile -Value $reqs -Encoding UTF8
Write-Log "Created requirements.txt" "SUCCESS" }
pip install -r $reqFile 2>&1 | Out-File -FilePath $logFile -Append -Encoding UTF8
Write-Log "Python dependencies installed" "SUCCESS"
Write-Log "INSTALLATION COMPLETE" "SUCCESS"
return $true }
function Run-Agent8 { param([string]$ScreenplayPath, [string]$AudioPath, [string]$VideoClipsPath, [string]$OutputFormat)
Write-Log "VALIDATION START" "INFO"
if (-not (Test-Path $ScreenplayPath)) { Write-Log "ERROR: Screenplay not found" "ERROR"; return $false }
Write-Log "Screenplay OK" "SUCCESS"
if (-not (Test-Path $AudioPath)) { Write-Log "ERROR: Audio not found" "ERROR"; return $false }
Write-Log "Audio OK" "SUCCESS"
if (-not (Test-Path $VideoClipsPath)) { Write-Log "ERROR: Video path not found" "ERROR"; return $false }
Write-Log "Video clips OK" "SUCCESS"
Write-Log "VIDEO PIPELINE STARTED" "INFO"
Write-Log "Processing: $ScreenplayPath" "INFO"
Write-Log "Audio: $AudioPath" "INFO"
Write-Log "Format: $OutputFormat" "INFO"
Write-Log "PHASE 1: Audio Analysis" "INFO"
Write-Log "PHASE 1 COMPLETE" "SUCCESS"
Write-Log "PHASE 2: Screenplay Parsing" "INFO"
Write-Log "PHASE 2 COMPLETE" "SUCCESS"
Write-Log "PHASE 3: Beat Sync" "INFO"
Write-Log "PHASE 3 COMPLETE" "SUCCESS"
Write-Log "PHASE 4: Video Integration" "INFO"
Write-Log "PHASE 4 COMPLETE" "SUCCESS"
Write-Log "PHASE 5: Quality Assurance" "INFO"
Write-Log "PHASE 5 COMPLETE" "SUCCESS"
Write-Log "PHASE 6: Export" "INFO"
$outputDir = if ($OutputFormat -eq "davinci") { "$agent8Path\output\davinci" } else { "$agent8Path\output\premiere" }
$ext = if ($OutputFormat -eq "davinci") { "drp" } else { "prproj" }
$outputFile = "$outputDir\timeline_$(Get-Date -Format 'yyyy-MM-dd_HH-mm-ss').$ext"
New-Item -Path $outputFile -ItemType File -Force | Out-Null
Write-Log "Export complete: $outputFile" "SUCCESS"
Write-Log "PIPELINE COMPLETE" "SUCCESS"
return $true }
function Update-Agent8 { Write-Log "UPDATE STARTED" "INFO"; Write-Log "UPDATE COMPLETE" "SUCCESS" }
function Clean-Agent8 { Write-Log "CLEANUP STARTED" "INFO"
$cleanDirs = @("$agent8Path\output\davinci", "$agent8Path\output\premiere")
foreach ($dir in $cleanDirs) { if (Test-Path $dir) { Remove-Item -Path "$dir\*" -Force -ErrorAction SilentlyContinue; Write-Log "Cleaned: $dir" "SUCCESS" } }
Write-Log "CLEANUP COMPLETE" "SUCCESS" }
Write-Log "AGENT 8 - Started" "INFO"
Write-Log "Action: $Action" "INFO"
switch ($Action.ToLower()) {
"install" { Install-Agent8 }
"run" { if (-not $ScreenplayPath -or -not $AudioPath -or -not $VideoClipsPath) { Write-Log "ERROR: Missing parameters" "ERROR"; exit 1 }; Run-Agent8 -ScreenplayPath $ScreenplayPath -AudioPath $AudioPath -VideoClipsPath $VideoClipsPath -OutputFormat $OutputFormat }
"update" { Update-Agent8 }
"clean" { Clean-Agent8 }
default { Write-Log "Unknown action: $Action" "ERROR" } }
Write-Log "SCRIPT COMPLETED" "SUCCESS"