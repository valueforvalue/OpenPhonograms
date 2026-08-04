# Windows Audio Generator for Phonogram Trainer
# Generates 75 WAV/MP3 files for games/phonogram-trainer.html
# Uses PowerShell + System.Speech (built into Windows 10/11)
#
# Usage: .\generate-audio.ps1          (generate all)
#        .\generate-audio.ps1 -Preview (dry run)

param([switch]$Preview = $false)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$audioDir = Join-Path $scriptDir "audio"

if (-not (Test-Path $audioDir)) {
    New-Item -ItemType Directory -Path $audioDir | Out-Null
}

Write-Host "Phonogram Audio Generator" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan
Write-Host ""

$ffmpeg = Get-Command ffmpeg -ErrorAction SilentlyContinue
if ($ffmpeg) {
    Write-Host "[OK] ffmpeg found - will output MP3" -ForegroundColor Green
} else {
    Write-Host "[!] ffmpeg not found - will output WAV (works fine, larger files)" -ForegroundColor Yellow
}

Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer

$voice = $synth.GetInstalledVoices() | Where-Object { $_.Enabled -and $_.VoiceInfo.Culture.Name -like "en-*" } | Select-Object -First 1
if (-not $voice) { Write-Host "ERROR: No English voice!" -ForegroundColor Red; exit 1 }

$synth.SelectVoice($voice.VoiceInfo.Name)
$synth.Rate = -2
$synth.Volume = 100
Write-Host "Voice: $($voice.VoiceInfo.Name)" -ForegroundColor Green
Write-Host ""

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
$i = 0

foreach ($pg in $phonograms) {
    $i++
    $wav = Join-Path $audioDir "$($pg.pg).wav"
    $mp3 = Join-Path $audioDir "$($pg.pg).mp3"
    $pct = [math]::Round(($i / $total) * 100)
    Write-Progress -Activity "Generating phonogram audio" -Status "$($pg.pg) - $($pg.speak)" -PercentComplete $pct

    if ($Preview) {
        Write-Host "[$i/$total] $($pg.pg) : $($pg.speak)" -ForegroundColor Gray
        continue
    }

    $synth.SetOutputToWaveFile($wav)
    $synth.Speak($pg.speak)
    $synth.SetOutputToNull()

    if ($ffmpeg) {
        & ffmpeg -hide_banner -loglevel error -i $wav -acodec libmp3lame -q:a 7 $mp3 -y
        if ($LASTEXITCODE -eq 0) {
            Remove-Item $wav -Force
            Write-Host "[$i/$total] $($pg.pg).mp3 OK" -ForegroundColor Green
        } else {
            Write-Host "[$i/$total] $($pg.pg).wav OK (MP3 failed)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "[$i/$total] $($pg.pg).wav OK" -ForegroundColor Green
    }
}

Write-Progress -Activity "Generating phonogram audio" -Completed
Write-Host ""
Write-Host "Done! $total files in $audioDir" -ForegroundColor Cyan
