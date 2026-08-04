# Windows Audio Generator for Phonogram Trainer
# Generates 75 MP3 files for games/phonogram-trainer.html
# Uses PowerShell + System.Speech (built into Windows, no install needed)

param(
    [switch]$Preview = $false  # Preview only, don't generate
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$audioDir = Join-Path $scriptDir "audio"

if (-not (Test-Path $audioDir)) {
    New-Item -ItemType Directory -Path $audioDir | Out-Null
}

Write-Host "Phonogram Audio Generator for Windows" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if ffmpeg is available (optional, for MP3 conversion)
$ffmpeg = Get-Command ffmpeg -ErrorAction SilentlyContinue
if ($ffmpeg) {
    Write-Host "[OK] ffmpeg found — will output MP3 files" -ForegroundColor Green
} else {
    Write-Host "[!] ffmpeg not found — will output WAV files (larger but work fine)" -ForegroundColor Yellow
    Write-Host "    Download ffmpeg from https://ffmpeg.org/download.html for MP3 support" -ForegroundColor Yellow
}

# Load speech assembly
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer

# List available voices
Write-Host "Available voices:" -ForegroundColor Gray
$synth.GetInstalledVoices() | ForEach-Object {
    $info = $_.VoiceInfo
    $marker = if ($_.Enabled) { "*" } else { " " }
    Write-Host "  $marker $($info.Name) — $($info.Culture) ($($info.Gender))"
}
Write-Host ""

# Pick best voice — prefer Microsoft female English voices
$voice = $synth.GetInstalledVoices() | 
    Where-Object { $_.Enabled -and $_.VoiceInfo.Culture.Name -like "en-*" } |
    Sort-Object { if ($_.VoiceInfo.Name -like "*Zira*") { 0 } elseif ($_.VoiceInfo.Name -like "*Microsoft*") { 1 } else { 2 } } |
    Select-Object -First 1

if (-not $voice) {
    Write-Host "ERROR: No English voice found!" -ForegroundColor Red
    exit 1
}

$synth.SelectVoice($voice.VoiceInfo.Name)
$synth.Rate = -2  # Slightly slower for clarity
$synth.Volume = 100

Write-Host "Using voice: $($voice.VoiceInfo.Name)" -ForegroundColor Green
Write-Host "Rate: -2 (slightly slow for clarity)" -ForegroundColor Gray
Write-Host ""

# Phonogram data: pg = phonogram, speak = words to say
$phonograms = @(
    @{pg="a"; speak="at, nation, father"}, @{pg="b"; speak="big"}, @{pg="c"; speak="cat, cent"},
    @{pg="d"; speak="dog"}, @{pg="e"; speak="end, even"}, @{pg="f"; speak="fun"},
    @{pg="g"; speak="go, gem"}, @{pg="h"; speak="hat"}, @{pg="i"; speak="it, item, radio"},
    @{pg="j"; speak="jet"}, @{pg="k"; speak="kit"}, @{pg="l"; speak="leg"},
    @{pg="m"; speak="man"}, @{pg="n"; speak="net"}, @{pg="o"; speak="odd, go, to"},
    @{pg="p"; speak="pen"}, @{pg="qu"; speak="queen"}, @{pg="r"; speak="red"},
    @{pg="s"; speak="sit, has"}, @{pg="t"; speak="top"}, @{pg="u"; speak="up, unit, put"},
    @{pg="v"; speak="van"}, @{pg="w"; speak="wet"}, @{pg="x"; speak="box, xylophone"},
    @{pg="y"; speak="yes, gym, by, baby"}, @{pg="z"; speak="zip"},
    @{pg="sh"; speak="ship"}, @{pg="th"; speak="this, thin"}, @{pg="ck"; speak="back"},
    @{pg="ee"; speak="see"}, @{pg="ng"; speak="sing"}, @{pg="ar"; speak="car"},
    @{pg="or"; speak="for"}, @{pg="er"; speak="her"}, @{pg="oi"; speak="coin"},
    @{pg="oy"; speak="boy"}, @{pg="ai"; speak="rain"}, @{pg="ay"; speak="day"},
    @{pg="ch"; speak="chin, school, chef"}, @{pg="wh"; speak="when"},
    @{pg="ea"; speak="eat, head, great"}, @{pg="ow"; speak="cow, snow"},
    @{pg="ou"; speak="out, soul, you, touch"}, @{pg="oo"; speak="book, food, floor"},
    @{pg="ed"; speak="wanted, played, fished"}, @{pg="igh"; speak="light"},
    @{pg="aw"; speak="saw"}, @{pg="au"; speak="cause"}, @{pg="ir"; speak="girl"},
    @{pg="ur"; speak="hurt"}, @{pg="oa"; speak="boat"}, @{pg="ear"; speak="learn"},
    @{pg="dge"; speak="bridge"}, @{pg="tch"; speak="catch"}, @{pg="kn"; speak="know"},
    @{pg="gn"; speak="sign"}, @{pg="wr"; speak="write"}, @{pg="eigh"; speak="eight"},
    @{pg="ei"; speak="ceiling, vein, feisty"}, @{pg="ey"; speak="they, key"},
    @{pg="ph"; speak="phone"}, @{pg="gh"; speak="ghost"},
    @{pg="ough"; speak="though, through, cough, rough, bought"},
    @{pg="augh"; speak="caught, laugh"}, @{pg="ew"; speak="few, sew"},
    @{pg="ui"; speak="fruit"}, @{pg="eu"; speak="neutral"},
    @{pg="wor"; speak="work"}, @{pg="ie"; speak="field, pie"},
    @{pg="ti"; speak="nation"}, @{pg="ci"; speak="special"},
    @{pg="si"; speak="session, vision"}, @{pg="bu"; speak="buy"},
    @{pg="gu"; speak="guide"}
)

$total = $phonograms.Count
$current = 0

foreach ($pg in $phonograms) {
    $current++
    $wavPath = Join-Path $audioDir "$($pg.pg).wav"
    $mp3Path = Join-Path $audioDir "$($pg.pg).mp3"
    
    $percent = [math]::Round(($current / $total) * 100)
    Write-Progress -Activity "Generating phonogram audio" -Status "$($pg.pg) — $($pg.speak)" -PercentComplete $percent
    
    if ($Preview) {
        Write-Host "[$current/$total] $($pg.pg) — `"$($pg.speak)`"" -ForegroundColor Gray
        continue
    }
    
    # Generate WAV using System.Speech
    $synth.SetOutputToWaveFile($wavPath)
    $synth.Speak($pg.speak)
    $synth.SetOutputToDefault()
    
    Write-Host "[$current/$total] $($pg.pg).wav — $((Get-Item $wavPath).Length) bytes" -ForegroundColor Green
    
    # Convert to MP3 if ffmpeg available
    if ($ffmpeg) {
        & ffmpeg -i $wavPath -acodec libmp3lame -q:a 7 $mp3Path -y 2>$null
        if ($LASTEXITCODE -eq 0) {
            Remove-Item $wavPath -Force
            $size = (Get-Item $mp3Path).Length
            Write-Host "           $($pg.pg).mp3 — $size bytes" -ForegroundColor Green
        } else {
            Write-Host "           MP3 conversion failed, keeping WAV" -ForegroundColor Yellow
        }
    }
}

Write-Progress -Activity "Generating phonogram audio" -Completed
Write-Host ""
Write-Host "Done! Generated $total audio files in $audioDir" -ForegroundColor Cyan

if ($ffmpeg) {
    $totalSize = (Get-ChildItem $audioDir -Filter *.mp3 | Measure-Object -Property Length -Sum).Sum
    Write-Host "Total size: $([math]::Round($totalSize / 1KB)) KB ($total MP3 files)" -ForegroundColor Gray
} else {
    $totalSize = (Get-ChildItem $audioDir -Filter *.wav | Measure-Object -Property Length -Sum).Sum
    Write-Host "Total size: $([math]::Round($totalSize / 1KB)) KB ($total WAV files)" -ForegroundColor Gray
    Write-Host "Install ffmpeg and re-run for smaller MP3 files." -ForegroundColor Yellow
}
