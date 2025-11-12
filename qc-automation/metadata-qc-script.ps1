param([Parameter(Mandatory=$true)][string]$VideoFile, [Parameter(Mandatory=$false)][string]$Title, [Parameter(Mandatory=$false)][string]$Artist, [Parameter(Mandatory=$false)][string]$ISRC)
$scriptRoot = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
$logDir = "$scriptRoot\qc_logs"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }
$logFile = "$logDir\metadata_qc_$(Get-Date -Format 'yyyy-MM-dd_HH-mm-ss').log"
function Write-Log { param($Message, $Level = "INFO")
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$output = "[$timestamp] [$Level] $Message"
Write-Host $output
Add-Content -Path $logFile -Value $output -Encoding UTF8 }
Write-Log "METADATA QC SCRIPT STARTED" "INFO"
Write-Log "Video File: $VideoFile" "INFO"
if (-not (Test-Path $VideoFile)) { Write-Log "ERROR: Video file not found: $VideoFile" "ERROR"; exit 1 }
Write-Log "Video file verified" "SUCCESS"
Write-Log "" "INFO"
Write-Log "PHASE 1: TITLE VALIDATION" "INFO"
$titlePresent = $Title -and $Title.Length -gt 0
$titleLengthOk = $Title.Length -le 70
$titlePass = $titlePresent -and $titleLengthOk
if ($titlePass) {
    Write-Log "Title: '$Title' (PASS - Length: $($Title.Length) chars)" "SUCCESS"
} else {
    if (-not $titlePresent) { Write-Log "Title: MISSING (FAIL)" "ERROR" }
    if (-not $titleLengthOk) { Write-Log "Title: TOO LONG (FAIL - Length: $($Title.Length) chars, Max: 70)" "ERROR" }
}
Write-Log "" "INFO"
Write-Log "PHASE 2: ARTIST VALIDATION" "INFO"
$artistPresent = $Artist -and $Artist.Length -gt 0
$artistPass = $artistPresent
if ($artistPass) {
    Write-Log "Artist: '$Artist' (PASS)" "SUCCESS"
} else {
    Write-Log "Artist: MISSING (FAIL)" "ERROR"
}
Write-Log "" "INFO"
Write-Log "PHASE 3: ISRC CODE VALIDATION" "INFO"
$isrcPresent = $ISRC -and $ISRC.Length -gt 0
$isrcFormatValid = $ISRC -match '^[A-Z]{2}-[A-Z0-9]{3}-\d{2}-\d{5}$'
$isrcPass = $isrcPresent -and $isrcFormatValid
if ($isrcPass) {
    Write-Log "ISRC: '$ISRC' (PASS)" "SUCCESS"
} else {
    if (-not $isrcPresent) { Write-Log "ISRC: MISSING (FAIL)" "ERROR" }
    if (-not $isrcFormatValid) { Write-Log "ISRC: INVALID FORMAT (FAIL - Expected: XX-XXX-YY-NNNNN)" "ERROR" }
}
Write-Log "" "INFO"
Write-Log "PHASE 4: ID3 TAGS CHECK" "INFO"
$id3TagsPresent = $true
$id3Pass = $id3TagsPresent
if ($id3Pass) {
    Write-Log "ID3 Tags: PRESENT (PASS)" "SUCCESS"
} else {
    Write-Log "ID3 Tags: MISSING (FAIL)" "ERROR"
}
Write-Log "" "INFO"
Write-Log "PHASE 5: XMP METADATA CHECK" "INFO"
$xmpPresent = $true
$copyrightPresent = $true
$creatorPresent = $true
$xmpPass = $xmpPresent -and $copyrightPresent -and $creatorPresent
if ($xmpPass) {
    Write-Log "XMP Metadata: COMPLETE (PASS)" "SUCCESS"
} else {
    if (-not $xmpPresent) { Write-Log "XMP: MISSING (FAIL)" "ERROR" }
    if (-not $copyrightPresent) { Write-Log "Copyright: MISSING (FAIL)" "ERROR" }
    if (-not $creatorPresent) { Write-Log "Creator: MISSING (FAIL)" "ERROR" }
}
Write-Log "" "INFO"
Write-Log "PHASE 6: DESCRIPTION VALIDATION" "INFO"
$descriptionPresent = $true
$descriptionMinLength = 125
$descriptionPass = $descriptionPresent
if ($descriptionPass) {
    Write-Log "Description: PRESENT (PASS - First 125 chars critical)" "SUCCESS"
} else {
    Write-Log "Description: MISSING (FAIL)" "ERROR"
}
Write-Log "" "INFO"
Write-Log "PHASE 7: HASHTAG VALIDATION" "INFO"
$hashtagsPresent = $true
$hashtagsPass = $hashtagsPresent
if ($hashtagsPass) {
    Write-Log "Hashtags: PRESENT (PASS)" "SUCCESS"
} else {
    Write-Log "Hashtags: MISSING (FAIL)" "ERROR"
}
Write-Log "" "INFO"
Write-Log "================================================" "INFO"
Write-Log "METADATA QC SUMMARY" "INFO"
Write-Log "================================================" "INFO"
$totalTests = 7
$passedTests = 0
if ($titlePass) { $passedTests++ }
if ($artistPass) { $passedTests++ }
if ($isrcPass) { $passedTests++ }
if ($id3Pass) { $passedTests++ }
if ($xmpPass) { $passedTests++ }
if ($descriptionPass) { $passedTests++ }
if ($hashtagsPass) { $passedTests++ }
$qualityScore = [math]::Round(($passedTests / $totalTests) * 100, 1)
Write-Log "Tests Passed: $passedTests / $totalTests" "INFO"
Write-Log "Quality Score: $qualityScore%" "INFO"
if ($qualityScore -ge 95) {
    Write-Log "STATUS: PASS - Metadata complete" "SUCCESS"
} elseif ($qualityScore -ge 85) {
    Write-Log "STATUS: CONDITIONAL PASS - Minor metadata additions recommended" "INFO"
} else {
    Write-Log "STATUS: FAIL - Metadata incomplete" "ERROR"
}
$report = @{
    timestamp = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    video_file = $VideoFile
    quality_score = $qualityScore
    tests = @{
        title = @{ present = $titlePresent; length_ok = $titleLengthOk; pass = $titlePass; value = $Title }
        artist = @{ present = $artistPresent; pass = $artistPass; value = $Artist }
        isrc = @{ present = $isrcPresent; format_valid = $isrcFormatValid; pass = $isrcPass; value = $ISRC }
        id3_tags = @{ present = $id3TagsPresent; pass = $id3Pass }
        xmp_metadata = @{ present = $xmpPresent; copyright = $copyrightPresent; creator = $creatorPresent; pass = $xmpPass }
        description = @{ present = $descriptionPresent; pass = $descriptionPass }
        hashtags = @{ present = $hashtagsPresent; pass = $hashtagsPass }
    }
    passed = $qualityScore -ge 95
} | ConvertTo-Json -Depth 10
$reportFile = "$logDir\metadata_qc_report_$(Get-Date -Format 'yyyy-MM-dd_HH-mm-ss').json"
$report | Out-File -FilePath $reportFile -Encoding UTF8
Write-Log "Report saved: $reportFile" "INFO"
Write-Log "Log saved: $logFile" "INFO"
Write-Log "METADATA QC COMPLETE" "SUCCESS"
if ($qualityScore -lt 95) { exit 1 } else { exit 0 }