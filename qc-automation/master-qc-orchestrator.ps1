param([Parameter(Mandatory=$true)][string]$VideoFile, [Parameter(Mandatory=$true)][string]$AudioFile, [Parameter(Mandatory=$false)][string]$Platform = "youtube", [Parameter(Mandatory=$false)][string]$Title, [Parameter(Mandatory=$false)][string]$Artist, [Parameter(Mandatory=$false)][string]$ISRC)
$scriptRoot = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
$logDir = "$scriptRoot\qc_logs"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }
$logFile = "$logDir\master_qc_$(Get-Date -Format 'yyyy-MM-dd_HH-mm-ss').log"
function Write-Log { param($Message, $Level = "INFO")
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$output = "[$timestamp] [$Level] $Message"
$color = switch ($Level) {
    "SUCCESS" { "Green" }
    "ERROR" { "Red" }
    "WARNING" { "Yellow" }
    default { "White" }
}
Write-Host $output -ForegroundColor $color
Add-Content -Path $logFile -Value $output -Encoding UTF8 }
Write-Log "================================================" "INFO"
Write-Log "MASTER QC ORCHESTRATOR STARTED" "INFO"
Write-Log "================================================" "INFO"
Write-Log "Video File: $VideoFile" "INFO"
Write-Log "Audio File: $AudioFile" "INFO"
Write-Log "Target Platform: $Platform" "INFO"
Write-Log "Title: $Title" "INFO"
Write-Log "Artist: $Artist" "INFO"
Write-Log "ISRC: $ISRC" "INFO"
Write-Log "" "INFO"
$startTime = Get-Date
$qcResults = @{}
Write-Log "STAGE 1: AUDIO QC" "INFO"
Write-Log "Running audio quality check..." "INFO"
$audioQcStart = Get-Date
& "$scriptRoot\audio-qc-script.ps1" -AudioFile $AudioFile -TargetPlatform $Platform
$audioQcPassed = $LASTEXITCODE -eq 0
$audioQcDuration = (Get-Date) - $audioQcStart
$qcResults.audio = @{ passed = $audioQcPassed; duration_seconds = [math]::Round($audioQcDuration.TotalSeconds, 1) }
if ($audioQcPassed) {
    Write-Log "Audio QC: PASSED (Duration: $($qcResults.audio.duration_seconds)s)" "SUCCESS"
} else {
    Write-Log "Audio QC: FAILED" "ERROR"
}
Write-Log "" "INFO"
Write-Log "STAGE 2: VIDEO QC" "INFO"
Write-Log "Running video quality check..." "INFO"
$videoQcStart = Get-Date
& "$scriptRoot\video-qc-script.ps1" -VideoFile $VideoFile -TargetPlatform $Platform
$videoQcPassed = $LASTEXITCODE -eq 0
$videoQcDuration = (Get-Date) - $videoQcStart
$qcResults.video = @{ passed = $videoQcPassed; duration_seconds = [math]::Round($videoQcDuration.TotalSeconds, 1) }
if ($videoQcPassed) {
    Write-Log "Video QC: PASSED (Duration: $($qcResults.video.duration_seconds)s)" "SUCCESS"
} else {
    Write-Log "Video QC: FAILED" "ERROR"
}
Write-Log "" "INFO"
Write-Log "STAGE 3: SYNC QC" "INFO"
Write-Log "Running sync quality check..." "INFO"
$syncQcStart = Get-Date
& "$scriptRoot\sync-qc-script.ps1" -VideoFile $VideoFile -AudioFile $AudioFile
$syncQcPassed = $LASTEXITCODE -eq 0
$syncQcDuration = (Get-Date) - $syncQcStart
$qcResults.sync = @{ passed = $syncQcPassed; duration_seconds = [math]::Round($syncQcDuration.TotalSeconds, 1) }
if ($syncQcPassed) {
    Write-Log "Sync QC: PASSED (Duration: $($qcResults.sync.duration_seconds)s)" "SUCCESS"
} else {
    Write-Log "Sync QC: FAILED" "ERROR"
}
Write-Log "" "INFO"
Write-Log "STAGE 4: METADATA QC" "INFO"
Write-Log "Running metadata quality check..." "INFO"
$metadataQcStart = Get-Date
& "$scriptRoot\metadata-qc-script.ps1" -VideoFile $VideoFile -Title $Title -Artist $Artist -ISRC $ISRC
$metadataQcPassed = $LASTEXITCODE -eq 0
$metadataQcDuration = (Get-Date) - $metadataQcStart
$qcResults.metadata = @{ passed = $metadataQcPassed; duration_seconds = [math]::Round($metadataQcDuration.TotalSeconds, 1) }
if ($metadataQcPassed) {
    Write-Log "Metadata QC: PASSED (Duration: $($qcResults.metadata.duration_seconds)s)" "SUCCESS"
} else {
    Write-Log "Metadata QC: FAILED" "ERROR"
}
Write-Log "" "INFO"
$totalDuration = (Get-Date) - $startTime
$totalPassed = ($qcResults.audio.passed -eq $true) -and ($qcResults.video.passed -eq $true) -and ($qcResults.sync.passed -eq $true) -and ($qcResults.metadata.passed -eq $true)
$passedCount = 0
if ($qcResults.audio.passed) { $passedCount++ }
if ($qcResults.video.passed) { $passedCount++ }
if ($qcResults.sync.passed) { $passedCount++ }
if ($qcResults.metadata.passed) { $passedCount++ }
$overallScore = [math]::Round(($passedCount / 4) * 100, 1)
Write-Log "================================================" "INFO"
Write-Log "MASTER QC RESULTS" "INFO"
Write-Log "================================================" "INFO"
Write-Log "Audio QC: $(if ($qcResults.audio.passed) { 'PASS' } else { 'FAIL' })" "INFO"
Write-Log "Video QC: $(if ($qcResults.video.passed) { 'PASS' } else { 'FAIL' })" "INFO"
Write-Log "Sync QC: $(if ($qcResults.sync.passed) { 'PASS' } else { 'FAIL' })" "INFO"
Write-Log "Metadata QC: $(if ($qcResults.metadata.passed) { 'PASS' } else { 'FAIL' })" "INFO"
Write-Log "" "INFO"
Write-Log "Tests Passed: $passedCount / 4" "INFO"
Write-Log "Overall Quality Score: $overallScore%" "INFO"
Write-Log "Total Duration: $([math]::Round($totalDuration.TotalSeconds, 1))s" "INFO"
if ($totalPassed) {
    Write-Log "================================================" "SUCCESS"
    Write-Log "MASTER QC: PASSED - READY FOR DISTRIBUTION" "SUCCESS"
    Write-Log "================================================" "SUCCESS"
} else {
    Write-Log "================================================" "ERROR"
    Write-Log "MASTER QC: FAILED - CORRECTIONS REQUIRED" "ERROR"
    Write-Log "================================================" "ERROR"
}
$masterReport = @{
    timestamp = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    video_file = $VideoFile
    audio_file = $AudioFile
    platform = $Platform
    title = $Title
    artist = $Artist
    isrc = $ISRC
    overall_score = $overallScore
    passed = $totalPassed
    duration_seconds = [math]::Round($totalDuration.TotalSeconds, 1)
    results = $qcResults
} | ConvertTo-Json -Depth 10
$reportFile = "$logDir\master_qc_report_$(Get-Date -Format 'yyyy-MM-dd_HH-mm-ss').json"
$masterReport | Out-File -FilePath $reportFile -Encoding UTF8
Write-Log "Master report saved: $reportFile" "INFO"
Write-Log "Log saved: $logFile" "INFO"
Write-Log "MASTER QC COMPLETE" "SUCCESS"
if (-not $totalPassed) { exit 1 } else { exit 0 }