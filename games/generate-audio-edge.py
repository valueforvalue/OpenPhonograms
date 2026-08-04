#!/usr/bin/env python3
"""Generate phonogram audio using Microsoft Edge neural TTS (free, high quality)."""
import asyncio, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AUDIO = ROOT / "audio"
AUDIO.mkdir(exist_ok=True)

VOICE = "en-US-AriaNeural"  # Female, warm, clear — best for children's learning
RATE = "-15%"  # Slightly slower for clarity

PHONOGRAMS = [
    ("a", "at, nation, father"), ("b", "big"), ("c", "cat, cent"),
    ("d", "dog"), ("e", "end, even"), ("f", "fun"),
    ("g", "go, gem"), ("h", "hat"), ("i", "it, item, radio"),
    ("j", "jet"), ("k", "kit"), ("l", "leg"),
    ("m", "man"), ("n", "net"), ("o", "odd, go, to"),
    ("p", "pen"), ("qu", "queen"), ("r", "red"),
    ("s", "sit, has"), ("t", "top"), ("u", "up, unit, put"),
    ("v", "van"), ("w", "wet"), ("x", "box, xylophone"),
    ("y", "yes, gym, by, baby"), ("z", "zip"),
    ("sh", "ship"), ("th", "this, thin"), ("ck", "back"),
    ("ee", "see"), ("ng", "sing"), ("ar", "car"),
    ("or", "for"), ("er", "her"), ("oi", "coin"),
    ("oy", "boy"), ("ai", "rain"), ("ay", "day"),
    ("ch", "chin, school, chef"), ("wh", "when"),
    ("ea", "eat, head, great"), ("ow", "cow, snow"),
    ("ou", "out, soul, you, touch"), ("oo", "book, food, floor"),
    ("ed", "wanted, played, fished"), ("igh", "light"),
    ("aw", "saw"), ("au", "cause"), ("ir", "girl"),
    ("ur", "hurt"), ("oa", "boat"), ("ear", "learn"),
    ("dge", "bridge"), ("tch", "catch"), ("kn", "know"),
    ("gn", "sign"), ("wr", "write"), ("eigh", "eight"),
    ("ei", "ceiling, vein, feisty"), ("ey", "they, key"),
    ("ph", "phone"), ("gh", "ghost"),
    ("ough", "though, through, cough, rough, bought"),
    ("augh", "caught, laugh"), ("ew", "few, sew"),
    ("ui", "fruit"), ("eu", "neutral"),
    ("wor", "work"), ("ie", "field, pie"),
    ("ti", "nation"), ("ci", "special"),
    ("si", "session, vision"), ("bu", "buy"),
    ("gu", "guide"),
]

async def generate_one(pg, text):
    mp3 = AUDIO / f"{pg}.mp3"
    if mp3.exists():
        print(f"  {pg}.mp3 — already exists, skipping")
        return
    cmd = [
        "edge-tts", "--voice", VOICE, "--rate", RATE,
        "--text", text, "--write-media", str(mp3),
    ]
    proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    await proc.communicate()
    if mp3.exists():
        size = mp3.stat().st_size
        print(f"  {pg}.mp3 — {size} bytes")
    else:
        print(f"  {pg}.mp3 — FAILED")

async def main():
    print(f"Voice: {VOICE} | Rate: {RATE}")
    print(f"Generating {len(PHONOGRAMS)} phonogram audio files...\n")
    for pg, text in PHONOGRAMS:
        await generate_one(pg, text)
    # Stats
    files = list(AUDIO.glob("*.mp3"))
    total = sum(f.stat().st_size for f in files)
    print(f"\nDone! {len(files)} files, {total//1024} KB total")

if __name__ == "__main__":
    asyncio.run(main())
