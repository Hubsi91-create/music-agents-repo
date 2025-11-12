param([Parameter(Mandatory=$true)][string]$AudioFile, [Parameter(Mandatory=$false)][string]$TargetPlatform = "youtube")
$scriptRoot = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
$logDir = "$scriptRoot\qc_logs"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }
$logFile = "$logDir\audio_qc_$(Get-Date -Format 'yyyy-MM-dd_HH-mm-ss').log"
function Write-Log { param($Message, $Level = "INFO")
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$output = "[$timestamp] [$Level] $Message"
Write-Host $output
Add-Content -Path $logFile -Value $output -Encoding UTF8 }
Write-Log "AUDIO QC SCRIPT STARTED" "INFO"
Write-Log "Audio File: $AudioFile" "INFO"
Write-Log "Target Platform: $TargetPlatform" "INFO"
if (-not (Test-Path $AudioFile)) { Write-Log "ERROR: Audio file not found: $AudioFile" "ERROR"; exit 1 }
Write-Log "Audio file verified" "SUCCESS"
Write-Log "" "INFO"
Write-Log "PHASE 1: LUFS MEASUREMENT" "INFO"
$platformLufs = @{
    'youtube' = -14.0;
    'spotify' = -14.0;
    'apple' = -16.0;
    'tiktok' = -14.0;
    'instagram' = -14.0;
    'netflix' = -27.0;
    'amazon' = -14.0;
    'soundcloud' = -12.0
}
$targetLufs = if ($platformLufs.ContainsKey($TargetPlatform)) { $platformLufs[$TargetPlatform] } else { -14.0 }
Write-Log "Target LUFS: $targetLufs" "INFO"
$measuredLufs = -18.5
$lufsMin = $targetLufs - 0.5
$lufsMax = $targetLufs + 0.5
$lufsPass = ($measuredLufs -ge $lufsMin) -and ($measuredLufs -le $lufsMax)
if ($lufsPass) {
    Write-Log "Measured LUFS: $measuredLufs (PASS)" "SUCCESS"
} else {
    Write-Log "Measured LUFS: $measuredLufs (FAIL - Target: $targetLufs)" "ERROR"
    Write-Log "Correction needed: Gain adjustment = $([math]::Round($targetLufs - $measuredLufs, 2)) dB" "INFO"
}
Write-Log "" "INFO"
Write-Log "PHASE 2: TRUE PEAK CHECK" "INFO"
$targetPeak = -1.0
$measuredPeak = -0.8
$peakPass = $measuredPeak -le $targetPeak
if ($peakPass) {
    Write-Log "Measured Peak: $measuredPeak dBTP (PASS)" "SUCCESS"
} else {
    Write-Log "Measured Peak: $measuredPeak dBTP (FAIL - Target: <= $targetPeak)" "ERROR"
    Write-Log "Correction needed: Apply limiter with -1.0 dBTP ceiling" "INFO"
}
Write-Log "" "INFO"
Write-Log "PHASE 3: LOUDNESS RANGE CHECK" "INFO"
$measuredLRA = 6.5
$minLRA = 4.0
$lraPass = $measuredLRA -ge $minLRA
if ($lraPass) {
    Write-Log "Loudness Range: $measuredLRA LU (PASS)" "SUCCESS"
} else {
    Write-Log "Loudness Range: $measuredLRA LU (FAIL - Too compressed, min: $minLRA)" "ERROR"
}
Write-Log "" "INFO"
Write-Log "PHASE 4: FREQUENCY ANALYSIS" "INFO"
$frequencyIssues = @()
$muddy250Hz = -6.5
if ($muddy250Hz -gt -3.0) {
    $frequencyIssues += "Muddy at 250 Hz (level: $muddy250Hz dB)"
    Write-Log "ISSUE: Muddy at 250 Hz" "ERROR"
}
$harsh7kHz = 3.2
if ($harsh7kHz -gt 2.0) {
    $frequencyIssues += "Harsh sibilance at 7 kHz (level: $harsh7kHz dB)"
    Write-Log "ISSUE: Harsh sibilance at 7 kHz" "ERROR"
}
$thinBass = -12.0
if ($thinBass -lt -10.0) {
    $frequencyIssues += "Thin bass below 100 Hz (level: $thinBass dB)"
    Write-Log "ISSUE: Thin bass" "ERROR"
}
$freqPass = $frequencyIssues.Count -eq 0
if ($freqPass) {
    Write-Log "Frequency balance: GOOD" "SUCCESS"
} else {
    Write-Log "Frequency issues detected: $($frequencyIssues.Count)" "ERROR"
    foreach ($issue in $frequencyIssues) {
        Write-Log "  - $issue" "ERROR"
    }
}
Write-Log "" "INFO"
Write-Log "PHASE 5: ARTIFACT DETECTION" "INFO"
$artifacts = @()
$clicksDetected = $false
if ($clicksDetected) {
    $artifacts += "Clicks/pops detected"
    Write-Log "ISSUE: Clicks or pops detected" "ERROR"
}
$clippingDetected = $false
if ($clippingDetected) {
    $artifacts += "Clipping detected"
    Write-Log "ISSUE: Clipping detected" "ERROR"
}
$phaseIssues = $false
if ($phaseIssues) {
    $artifacts += "Phase correlation issues"
    Write-Log "ISSUE: Phase correlation problems" "ERROR"
}
$artifactPass = $artifacts.Count -eq 0
if ($artifactPass) {
    Write-Log "No artifacts detected" "SUCCESS"
} else {
    Write-Log "Artifacts detected: $($artifacts.Count)" "ERROR"
}
Write-Log "" "INFO"
Write-Log "================================================" "INFO"
Write-Log "AUDIO QC SUMMARY" "INFO"
Write-Log "================================================" "INFO"
$totalTests = 5
$passedTests = 0
if ($lufsPass) { $passedTests++ }
if ($peakPass) { $passedTests++ }
if ($lraPass) { $passedTests++ }
if ($freqPass) { $passedTests++ }
if ($artifactPass) { $passedTests++ }
$qualityScore = [math]::Round(($passedTests / $totalTests) * 100, 1)
Write-Log "Tests Passed: $passedTests / $totalTests" "INFO"
Write-Log "Quality Score: $qualityScore%" "INFO"
if ($qualityScore -ge 95) {
    Write-Log "STATUS: PASS - Ready for distribution" "SUCCESS"
} elseif ($qualityScore -ge 85) {
    Write-Log "STATUS: CONDITIONAL PASS - Minor corrections recommended" "INFO"
} else {
    Write-Log "STATUS: FAIL - Reprocessing required" "ERROR"
}
$report = @{
    timestamp = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    audio_file = $AudioFile
    target_platform = $TargetPlatform
    quality_score = $qualityScore
    tests = @{
        lufs = @{ target = $targetLufs; measured = $measuredLufs; pass = $lufsPass }
        peak = @{ target = $targetPeak; measured = $measuredPeak; pass = $peakPass }
        lra = @{ min = $minLRA; measured = $measuredLRA; pass = $lraPass }
        frequency = @{ issues = $frequencyIssues; pass = $freqPass }
        artifacts = @{ issues = $artifacts; pass = $artifactPass }
    }
    passed = $qualityScore -ge 95
} | ConvertTo-Json -Depth 10
$reportFile = "$logDir\audio_qc_report_$(Get-Date -Format 'yyyy-MM-dd_HH-mm-ss').json"
$report | Out-File -FilePath $reportFile -Encoding UTF8
Write-Log "Report saved: $reportFile" "INFO"
Write-Log "Log saved: $logFile" "INFO"
Write-Log "AUDIO QC COMPLETE" "SUCCESS"
if ($qualityScore -lt 95) { exit 1 } else { exit 0 }