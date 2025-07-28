import os
import shutil
import re
import tempfile
import logging
import unicodedata

from pydub import AudioSegment
from edge_tts import Communicate
from edge_tts.exceptions import NoAudioReceived

log = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────
# Point pydub at your ffmpeg
ffmpeg_bin = (
    shutil.which("ffmpeg")
    or r"C:\Users\eissa.abbas\Desktop\work\work projects\FFmpeg\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe"
)
ffmpeg_dir = os.path.dirname(ffmpeg_bin)
os.environ["PATH"] = f"{ffmpeg_dir}{os.pathsep}{os.environ.get('PATH','')}"
os.environ["FFMPEG_BINARY"]  = ffmpeg_bin
os.environ["FFPROBE_BINARY"] = shutil.which("ffprobe") or ffmpeg_bin

EN_VOICE = "en-US-AvaNeural"
AR_VOICE = "ar-EG-SalmaNeural"

# Unicode range for Arabic script detection
ARABIC_RANGE = (
    r"\u0600-\u06FF"
    r"\u0750-\u077F"
    r"\u08A0-\u08FF"
    r"\uFB50-\uFDFF"
    r"\uFE70-\uFEFF"
)
RE_ARABIC = re.compile(f"[{ARABIC_RANGE}]")

# keep only English letters, Arabic letters, and whitespace
CLEAN_RE = re.compile(r"[^A-Za-z\u0600-\u06FF\s]+")


def detect_language(text: str) -> str:
    return "ar" if re.search(r'[\u0600-\u06FF]', text) else "en"

def _mp3_to_wav(mp3_path: str, wav_path: str):
    """Convert mp3 → wav and delete the temporary mp3."""
    wav = AudioSegment.from_file(mp3_path, format="mp3")
    os.makedirs(os.path.dirname(wav_path), exist_ok=True)
    wav.export(wav_path, format="wav")
    os.unlink(mp3_path)

async def _synth_mixed(text: str, outpath: str):
    # 1) strip out ALL ASCII punctuation & digits
    text = CLEAN_RE.sub("", text).strip()
    if not text:
        raise RuntimeError("Empty text for TTS after cleaning!")

    # 2) detect Arabic presence
    has_ar = bool(RE_ARABIC.search(text))

    # 3) choose voice
    if has_ar:
        # Arabic voice will read both Arabic & English
        tf = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        tf.close()
        try:
            await Communicate(text=text, voice=AR_VOICE, rate="+10%").save(tf.name)
            _mp3_to_wav(tf.name, outpath)
            return
        except Exception as e:
            log.error(f"Arabic-voice mixed TTS failed ({e}), falling back to English.")
            try: os.unlink(tf.name)
            except: pass

    # 4) fallback to pure English
    tf = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    tf.close()
    try:
        await Communicate(text=text, voice=EN_VOICE, rate="+0%").save(tf.name)
        _mp3_to_wav(tf.name, outpath)
    except NoAudioReceived:
        log.error("English TTS produced no audio!")
        raise
    except Exception as e:
        log.error(f"English TTS failed ({e})")
        try: os.unlink(tf.name)
        except: pass
        raise

async def synthesize(text: str, output_path: str):
    await _synth_mixed(text, output_path)
