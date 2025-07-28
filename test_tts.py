# test_tts.py

import os
import shutil
import re
import asyncio
import tempfile
from pathlib import Path

# —————————————————————————————————————————————————————————————————————————————
# 1) POINT PYDUB TO YOUR LOCAL FFMPEG BEFORE ANY pydub IMPORTS
ffmpeg_bin  = shutil.which("ffmpeg") or r"C:\Users\eissa.abbas\Desktop\work\work projects\FFmpeg\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe"
ffprobe_bin = shutil.which("ffprobe") or ffmpeg_bin.replace("ffmpeg.exe", "ffprobe.exe")

# Prepend the ffmpeg folder to PATH
ffmpeg_dir = os.path.dirname(ffmpeg_bin)
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
os.environ["FFMPEG_BINARY"]  = ffmpeg_bin
os.environ["FFPROBE_BINARY"] = ffprobe_bin

# Now it’s safe to import pydub
from pydub import AudioSegment
from edge_tts import Communicate
# —————————————————————————————————————————————————————————————————————————————

EN_VOICE = "en-US-AvaNeural"
AR_VOICE = "ar-EG-SalmaNeural"
CROSSFADE_MS = 300  # length of overlap between segments

async def synth_mixed(text: str, outpath: str):
    # Split on Arabic script runs
    runs = re.split(r'([\u0600-\u06FF]+)', text)

    tmp_files = []
    for run in runs:
        run = run.strip()
        if not run:
            continue

        # pick the voice by detecting Arabic characters
        voice = AR_VOICE if re.search(r'[\u0600-\u06FF]', run) else EN_VOICE

        # temporary file for this run
        tf = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        tf.close()
        tmp_files.append(tf.name)

        # generate
        comm = Communicate(text=run, voice=voice)
        await comm.save(tf.name)
        # no manual close — Communicate handles it

    if not tmp_files:
        raise RuntimeError("No text segments to synthesize!")

    # stitch them together with crossfade
    combined = AudioSegment.from_file(tmp_files[0], format="mp3")
    for fn in tmp_files[1:]:
        seg = AudioSegment.from_file(fn, format="mp3")
        combined = combined.append(seg, crossfade=CROSSFADE_MS)

    # export final
    combined.export(outpath, format="mp3")
    print(f"✅ Saved mixed TTS to {outpath}")

    # clean up
    for fn in tmp_files:
        Path(fn).unlink(missing_ok=True)

def _ignore_connreset(loop, context):
    # swallow WinError 10054 at shutdown
    ex = context.get("exception")
    if isinstance(ex, ConnectionResetError):
        return
    loop.default_exception_handler(context)

async def main():
    loop = asyncio.get_running_loop()
    loop.set_exception_handler(_ignore_connreset)

    sample = "Hello مرحبا, this is a mixed English و عربي test."
    await synth_mixed(sample, "out.mp3")

if __name__ == "__main__":
    asyncio.run(main())
