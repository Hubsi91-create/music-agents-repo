param([Parameter(Mandatory=$false)][string]$Action = "install")
$agent8Path = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
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
foreach ($dir in $directories) { if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null; Write-Log "Created: $dir" "SUCCESS" } else { Write-Log "Already exists: $dir" "INFO" } }
$reqFile = "$agent8Path\requirements.txt"
if (-not (Test-Path $reqFile)) { $reqs = "librosa`nnumpy`npydub`nav`nopencv-python`nscipy`nsoundfile`npyyaml"; $reqs | Out-File -FilePath $reqFile -Encoding UTF8; Write-Log "Created requirements.txt" "SUCCESS" }
Write-Log "Installing Python packages..." "INFO"
pip install -r $reqFile 2>&1 | Out-File -FilePath $logFile -Append -Encoding UTF8
Write-Log "Python dependencies installed" "SUCCESS"
Write-Log "INSTALLATION COMPLETE" "SUCCESS"
return $true }
Write-Log "AGENT 8 STARTED" "INFO"
Write-Log "Agent Path: $agent8Path" "INFO"
Write-Log "Action: $Action" "INFO"
if ($Action -eq "install") { Install-Agent8 }
Write-Log "SCRIPT COMPLETED" "SUCCESS"
