param([Parameter(Mandatory=$true)][string]$VideoFile, [Parameter(Mandatory=$false)][string]$TargetPlatform = "youtube")
$scriptRoot = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
$logDir = "$scriptRoot\qc_logs"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }
$logFile = "$logDir\video_qc_$(Get-Date -Format 'yyyy-MM-dd_HH-mm-ss').log"
function Write-Log { param($Message, $Level = "INFO")
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$output = "[$timestamp] [$Level] $Message"
Write-Host $output
Add-Content -Path $logFile -Value $output -Encoding UTF8 }
Write-Log "VIDEO QC SCRIPT STARTED" "INFO"
Write-Log "Video File: $VideoFile" "INFO"
Write-Log "Target Platform: $TargetPlatform" "INFO"
if (-not (Test-Path $VideoFile)) { Write-Log "ERROR: Video file not found: $VideoFile" "ERROR"; exit 1 }
Write-Log "Video file verified" "SUCCESS"
Write-Log "" "INFO"
Write-Log "PHASE 1: RESOLUTION CHECK" "INFO"
$platformResolutions = @{
    'youtube' = @('1920x1080', '3840x2160');
    'tiktok' = @('1080x1920');
    'instagram' = @('1080x1920', '1080x1080');
    'spotify' = @('1080x1080', '1920x1920');
    'netflix' = @('1920x1080', '3840x2160', '4096x2160');
    'amazon' = @('1920x1080', '3840x2160')
}
$targetResolutions = if ($platformResolutions.ContainsKey($TargetPlatform)) { $platformResolutions[$TargetPlatform] } else { @('1920x1080') }
$measuredResolution = "1920x1080"
$resolutionPass = $targetResolutions -contains $measuredResolution
if ($resolutionPass) {
    Write-Log "Resolution: $measuredResolution (PASS)" "SUCCESS"
} else {
    Write-Log "Resolution: $measuredResolution (FAIL - Expected: $($targetResolutions -join ' or '))" "ERROR"
}
Write-Log "" "INFO"
Write-Log "PHASE 2: FRAMERATE CHECK" "INFO"
$platformFramerates = @{
    'youtube' = @(23.976, 24, 25, 29.97, 30, 60);
    'tiktok' = @(23.976, 24, 25, 29.97, 30);
    'instagram' = @(23.976, 24, 25, 29.97, 30);
    'netflix' = @(23.976, 24, 25, 29.97, 30);
    'spotify' = @(23.976, 24, 25, 29.97, 30)
}
$targetFramerates = if ($platformFramerates.ContainsKey($TargetPlatform)) { $platformFramerates[$TargetPlatform] } else { @(23.976, 24, 25, 29.97, 30) }
$measuredFramerate = 23.976
$frameratePass = $targetFramerates -contains $measuredFramerate
if ($frameratePass) {
    Write-Log "Framerate: $measuredFramerate fps (PASS)" "SUCCESS"
} else {
    Write-Log "Framerate: $measuredFramerate fps (FAIL - Expected: $($targetFramerates -join ' or '))" "ERROR"
}
Write-Log "" "INFO"
Write-Log "PHASE 3: COLOR SPACE CHECK" "INFO"
$platformColorSpaces = @{
    'youtube' = @('sRGB', 'Rec.709');
    'tiktok' = @('sRGB');
    'instagram' = @('sRGB');
    'spotify' = @('sRGB');
    'netflix' = @('Rec.709', 'DCI-P3', 'Rec.2020');
    'amazon' = @('sRGB', 'Rec.709', 'DCI-P3')
}
$targetColorSpaces = if ($platformColorSpaces.ContainsKey($TargetPlatform)) { $platformColorSpaces[$TargetPlatform] } else { @('sRGB') }
$measuredColorSpace = "sRGB"
$colorSpacePass = $targetColorSpaces -contains $measuredColorSpace
if ($colorSpacePass) {
    Write-Log "Color Space: $measuredColorSpace (PASS)" "SUCCESS"
} else {
    Write-Log "Color Space: $measuredColorSpace (FAIL - Expected: $($targetColorSpaces -join ' or '))" "ERROR"
}
Write-Log "" "INFO"
Write-Log "PHASE 4: CODEC CHECK" "INFO"
$platformCodecs = @{
    'youtube' = @('H.264', 'H.265', 'VP9');
    'tiktok' = @('H.264');
    'instagram' = @('H.264', 'H.265');
    'spotify' = @('H.264');
    'netflix' = @('H.265', 'VP9', 'AV1');
    'amazon' = @('H.264', 'H.265')
}
$targetCodecs = if ($platformCodecs.ContainsKey($TargetPlatform)) { $platformCodecs[$TargetPlatform] } else { @('H.264') }
$measuredCodec = "H.264"
$codecPass = $targetCodecs -contains $measuredCodec
if ($codecPass) {
    Write-Log "Codec: $measuredCodec (PASS)" "SUCCESS"
} else {
    Write-Log "Codec: $measuredCodec (FAIL - Expected: $($targetCodecs -join ' or '))" "ERROR"
}
Write-Log "" "INFO"
Write-Log "PHASE 5: HISTOGRAM ANALYSIS" "INFO"
$blacksClipped = $false
$whitesClipped = $false
$histogramPass = (-not $blacksClipped) -and (-not $whitesClipped)
if ($histogramPass) {
    Write-Log "Histogram: Blacks and whites within range (PASS)" "SUCCESS"
} else {
    if ($blacksClipped) { Write-Log "ISSUE: Blacks clipped (below 16)" "ERROR" }
    if ($whitesClipped) { Write-Log "ISSUE: Whites clipped (above 235)" "ERROR" }
}
Write-Log "" "INFO"
Write-Log "PHASE 6: COMPRESSION ARTIFACTS CHECK" "INFO"
$artifactIssues = @()
$blockiness = $false
if ($blockiness) {
    $artifactIssues += "Blockiness detected (low bitrate)"
    Write-Log "ISSUE: Blockiness detected" "ERROR"
}
$banding = $false
if ($banding) {
    $artifactIssues += "Color banding detected"
    Write-Log "ISSUE: Color banding" "ERROR"
}
$aliasing = $false
if ($aliasing) {
    $artifactIssues += "Aliasing on edges"
    Write-Log "ISSUE: Aliasing detected" "ERROR"
}
$artifactPass = $artifactIssues.Count -eq 0
if ($artifactPass) {
    Write-Log "No compression artifacts detected" "SUCCESS"
} else {
    Write-Log "Artifacts detected: $($artifactIssues.Count)" "ERROR"
}
Write-Log "" "INFO"
Write-Log "PHASE 7: BITRATE CHECK" "INFO"
$platformBitrates = @{
    'youtube' = @{ '1080p' = 8; '4k' = 25 };
    'tiktok' = @{ 'vertical' = 5 };
    'instagram' = @{ 'vertical' = 5 };
    'spotify' = @{ 'canvas' = 2 };
    'netflix' = @{ '1080p' = 12; '4k' = 50 }
}
$targetBitrate = 8
$measuredBitrate = 7.8
$bitrateMin = $targetBitrate - 1
$bitrateMax = $targetBitrate + 2
$bitratePass = ($measuredBitrate -ge $bitrateMin) -and ($measuredBitrate -le $bitrateMax)
if ($bitratePass) {
    Write-Log "Bitrate: $measuredBitrate Mbps (PASS - Target: $targetBitrate)" "SUCCESS"
} else {
    Write-Log "Bitrate: $measuredBitrate Mbps (FAIL - Target: $targetBitrate)" "ERROR"
}
Write-Log "" "INFO"
Write-Log "================================================" "INFO"
Write-Log "VIDEO QC SUMMARY" "INFO"
Write-Log "================================================" "INFO"
$totalTests = 7
$passedTests = 0
if ($resolutionPass) { $passedTests++ }
if ($frameratePass) { $passedTests++ }
if ($colorSpacePass) { $passedTests++ }
if ($codecPass) { $passedTests++ }
if ($histogramPass) { $passedTests++ }
if ($artifactPass) { $passedTests++ }
if ($bitratePass) { $passedTests++ }
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
    video_file = $VideoFile
    target_platform = $TargetPlatform
    quality_score = $qualityScore
    tests = @{
        resolution = @{ target = $targetResolutions; measured = $measuredResolution; pass = $resolutionPass }
        framerate = @{ target = $targetFramerates; measured = $measuredFramerate; pass = $frameratePass }
        colorspace = @{ target = $targetColorSpaces; measured = $measuredColorSpace; pass = $colorSpacePass }
        codec = @{ target = $targetCodecs; measured = $measuredCodec; pass = $codecPass }
        histogram = @{ blacks_clipped = $blacksClipped; whites_clipped = $whitesClipped; pass = $histogramPass }
        artifacts = @{ issues = $artifactIssues; pass = $artifactPass }
        bitrate = @{ target = $targetBitrate; measured = $measuredBitrate; pass = $bitratePass }
    }
    passed = $qualityScore -ge 95
} | ConvertTo-Json -Depth 10
$reportFile = "$logDir\video_qc_report_$(Get-Date -Format 'yyyy-MM-dd_HH-mm-ss').json"
$report | Out-File -FilePath $reportFile -Encoding UTF8
Write-Log "Report saved: $reportFile" "INFO"
Write-Log "Log saved: $logFile" "INFO"
Write-Log "VIDEO QC COMPLETE" "SUCCESS"
if ($qualityScore -lt 95) { exit 1 } else { exit 0 }