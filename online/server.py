import os
import sys
import uuid
import json
import subprocess
import logging
import shutil
import difflib
import unicodedata
import secrets
from datetime import datetime, timedelta
from urllib.parse import quote_plus

from fastapi import (
    FastAPI,
    File,
    UploadFile,
    Request,
    Response,
    HTTPException,
    Depends,
    status
)
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from passlib.hash import bcrypt
from jose import JWTError, jwt
import google.oauth2.id_token
import google.auth.transport.requests

# ─ Make project root importable ─
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

# ─ Pipeline imports ─
from online.stt.whisper_stt     import transcribe
from online.retrieval.retriever import get_relevant_chunks
from online.llm.inference       import generate_answer, llm
from online.tts.tts_service     import synthesize, detect_language

# ─ Logging ─
logger = logging.getLogger("uvicorn.error")

app = FastAPI(
    title="Voice Chatbot API",
    description="Voice-enabled RAG tutor with automatic bilingual support",
    version="1.0",
)

# ─ CORS (allow all origins for now) ─
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─ Ensure temp dirs exist ─
audio_dir   = os.path.join(project_root, "online", "temp", "audio")
history_dir = os.path.join(project_root, "online", "temp", "history")
os.makedirs(audio_dir,   exist_ok=True)
os.makedirs(history_dir, exist_ok=True)

# ─ Persist SECRET_KEY across restarts ─
SECRET_FILE = os.path.join(history_dir, "secret_key.txt")
if os.path.exists(SECRET_FILE):
    SECRET_KEY = open(SECRET_FILE, "r", encoding="utf-8").read().strip()
else:
    SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_urlsafe(32)
    with open(SECRET_FILE, "w", encoding="utf-8") as f:
        f.write(SECRET_KEY)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

# ─ Helpers for per-user storage ─
def user_dir(email: str) -> str:
    safe = quote_plus(email)
    path = os.path.join(history_dir, safe)
    os.makedirs(path, exist_ok=True)
    return path

def metadata_path(email: str) -> str:
    ud = user_dir(email)
    mf = os.path.join(ud, "metadata.json")
    if not os.path.exists(mf):
        with open(mf, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=2)
    return mf

def load_metadata(email: str) -> dict:
    with open(metadata_path(email), "r", encoding="utf-8") as f:
        return json.load(f)

def save_metadata(email: str, meta: dict):
    with open(metadata_path(email), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

# ─ User DB (email/password) ─
user_db_file = os.path.join(history_dir, "users.json")
if not os.path.exists(user_db_file):
    with open(user_db_file, "w", encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False, indent=2)

def load_users() -> dict:
    with open(user_db_file, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users: dict):
    with open(user_db_file, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

# ─ Auth / JWT helpers ─
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return email
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

async def get_current_user(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        auth: str = request.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            token = auth[7:]
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return verify_token(token)

# ─ Google OAuth config ─
GOOGLE_CLIENT_ID = os.getenv(
    "GOOGLE_CLIENT_ID",
    "179290570443-m7j4913a76t2j1g1o3rdgpv05od2q2ng.apps.googleusercontent.com"
)
google_request_adapter = google.auth.transport.requests.Request()

# ─ Locate FFmpeg ─
ffmpeg_bin = (
    shutil.which("ffmpeg")
    or r"C:\Users\eissa.abbas\Desktop\work\work projects\FFmpeg\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe"
)

# ─ Typing simulation helper ─
def make_typing_simulation(answer_text: str):
    sim, cur = [], ""
    for c in answer_text:
        cur += c
        sim.append(cur)
    return sim

# ─ Text normalization & greetings ─
def normalize_text(text: str) -> str:
    text = text.lower()
    mapping = str.maketrans({"أ":"ا","إ":"ا","آ":"ا","ى":"ي","ؤ":"و","ئ":"ي","ة":"ه"})
    text = text.translate(mapping)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return text.strip()

GREETINGS = [
    "hello","hi","hey","good morning","good evening","good afternoon","how are you",
    "السلام عليكم","مرحبا","صباح الخير","مساء الخير","أهلا","أهلا وسهلا","كيف حالك","كيف حالكم"
]
G_LOWER_NORM = [normalize_text(g) for g in GREETINGS]
GREETINGS_RESPONSES_EN = [
    "Hello! How can I help you today?",
    "Hi there! What would you like to learn?",
    "Hey! Ask me anything from your material.",
    "Welcome! How can I assist you?"
]
GREETINGS_RESPONSES_AR = [
    "مرحباً! كيف يمكنني مساعدتك اليوم؟",
    "أهلاً! ماذا تحب أن تتعلم؟",
    "مرحباً! اسألني أي شيء من موادك.",
    "أهلاً وسهلاً! كيف أستطيع مساعدتك؟"
]

def is_greeting(text: str) -> bool:
    tnorm = normalize_text(text)
    if any(tnorm == g or tnorm.startswith(g) for g in G_LOWER_NORM): return True
    if difflib.get_close_matches(tnorm, G_LOWER_NORM, n=1, cutoff=0.8): return True
    first = tnorm.split()[0] if tnorm else ""
    if difflib.get_close_matches(first, G_LOWER_NORM, n=1, cutoff=0.8): return True
    if any(difflib.SequenceMatcher(None, tnorm, g).ratio() >= 0.75 for g in G_LOWER_NORM): return True
    if any(
        difflib.SequenceMatcher(None, w, g).ratio() >= 0.75
        for w in tnorm.split() for g in G_LOWER_NORM
    ): return True
    return False

@app.on_event("startup")
def verify_ffmpeg():
    if not ffmpeg_bin or not os.path.isfile(ffmpeg_bin):
        logger.error(f"FFmpeg not found at: {ffmpeg_bin}")
        return
    try:
        proc = subprocess.run(
            [ffmpeg_bin, "-version"],
            capture_output=True, text=True, check=True
        )
        logger.info(f"FFmpeg found: {proc.stdout.splitlines()[0]}")
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg test failed:\n{e.stderr}")

# ─ Serve index.html ─
@app.get("/", response_class=FileResponse)
async def serve_index():
    path = os.path.join(project_root, "index.html")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"index.html not found at {path}")
    return FileResponse(path)

# ─── AUTH: Signup & Login ───
class AuthPayload(BaseModel):
    email: str
    password: str

COOKIE_NAME = "access_token"

def set_token_cookie(response: Response, token: str):
    response.set_cookie(
        COOKIE_NAME,
        token,
        httponly=True,
        samesite="lax",
        secure=False,    # <- set True if you run under HTTPS
        path="/",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

@app.post("/auth/signup")
async def signup(payload: AuthPayload, response: Response):
    users = load_users()
    if payload.email in users:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = bcrypt.hash(payload.password)
    users[payload.email] = {"password": hashed}
    save_users(users)
    token = create_access_token({"sub": payload.email})
    set_token_cookie(response, token)
    return {"message": "signed up"}

@app.post("/auth/login")
async def login(payload: AuthPayload, response: Response):
    users = load_users()
    user = users.get(payload.email)
    if not user or not bcrypt.verify(payload.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": payload.email})
    set_token_cookie(response, token)
    return {"message": "logged in"}

@app.post("/auth/google")
async def auth_google(req: Request, response: Response):
    body = await req.json()
    cred = body.get("id_token")
    if not cred:
        raise HTTPException(status_code=400, detail="Missing Google credential")
    try:
        id_info = google.oauth2.id_token.verify_oauth2_token(
            cred, google_request_adapter, GOOGLE_CLIENT_ID
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Google token")
    email = id_info.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Google token has no email")
    users = load_users()
    if email not in users:
        users[email] = {"password": None}
        save_users(users)
    token = create_access_token({"sub": email})
    set_token_cookie(response, token)
    return {"message": "google auth successful"}

@app.post("/auth/logout")
async def logout(response: Response):
    response.delete_cookie(COOKIE_NAME, path="/")
    return {"message": "logged out"}

# ─── /chat/ endpoint ───
@app.post("/chat/")
async def chat(request: Request, user: str = Depends(get_current_user)):
    form        = await request.form()
    question    = form.get("question", "").strip()
    history_raw = form.get("history", "[]")
    session_id  = form.get("session_id") or uuid.uuid4().hex

    ud = user_dir(user)
    hist_path = os.path.join(ud, f"{session_id}.json")
    try:
        chat_history = json.loads(history_raw)
    except json.JSONDecodeError:
        chat_history = []

    lang = detect_language(question)
    if is_greeting(question):
        import random
        answer   = random.choice(GREETINGS_RESPONSES_AR if lang=="ar" else GREETINGS_RESPONSES_EN)
        citation = ""
    else:
        chunks = get_relevant_chunks(question, top_k=3)
        if chunks:
            result = generate_answer(chunks, question, chat_history, target_lang=lang)
            answer, citation = result if isinstance(result, tuple) else (result, "")
        else:
            answer, citation = (
                ("Sorry, I don’t know.", "") if lang=="en"
                else ("عذراً، لا أعرف.", "")
            )

    uid     = uuid.uuid4().hex
    out_wav = os.path.join(audio_dir, f"{uid}_out.wav")
    await synthesize(answer, out_wav)
    audio_url = f"/audio/{uid}_out.wav"

    entry = [
        {"role": "user",      "text": question},
        {"role": "assistant", "text": answer, "citation": citation, "audio_url": audio_url}
    ]
    existing = []
    if os.path.exists(hist_path):
        with open(hist_path, "r", encoding="utf-8") as f:
            existing = json.load(f)
    existing.extend(entry)
    with open(hist_path, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    return {
        "session_id":        session_id,
        "transcript":        question,
        "answer":            answer,
        "citation":          citation,
        "audio_url":         audio_url,
        "avatar_waiting":    "/static/avatar waiting.mp4",
        "avatar_speaking":   "/static/avatar talking.mp4",
        "typing_simulation": make_typing_simulation(answer),
    }

# ─── /transcribe/ endpoint ───
@app.post("/transcribe/")
async def transcribe_audio(
    audio: UploadFile = File(...),
    user: str = Depends(get_current_user)
):
    uid     = uuid.uuid4().hex
    in_webm = os.path.join(audio_dir, f"{uid}_in.webm")
    in_wav  = os.path.join(audio_dir, f"{uid}_in.wav")

    with open(in_webm, "wb") as f:
        f.write(await audio.read())

    audio_path = in_webm
    if ffmpeg_bin and os.path.isfile(ffmpeg_bin):
        try:
            subprocess.run(
                [ffmpeg_bin, "-y", "-i", in_webm, "-ac", "1", "-ar", "16000", in_wav],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
            )
            if os.path.getsize(in_wav) > 0:
                audio_path = in_wav
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg STT conversion failed:\n{e.stderr}")

    try:
        transcript = transcribe(audio_path)
    except Exception as e:
        logger.error(f"STT failed: {e}")
        transcript = ""

    return {"transcript": transcript}

# ─── /ask/ endpoint ───
@app.post("/ask/")
async def ask(
    request: Request,
    audio: UploadFile = File(...),
    user: str = Depends(get_current_user)
):
    form        = await request.form()
    history_raw = form.get("history", "[]")
    session_id  = form.get("session_id") or uuid.uuid4().hex

    ud = user_dir(user)
    hist_path = os.path.join(ud, f"{session_id}.json")
    try:
        chat_history = json.loads(history_raw)
    except json.JSONDecodeError:
        chat_history = []

    uid     = uuid.uuid4().hex
    in_webm = os.path.join(audio_dir, f"{uid}_in.webm")
    in_wav  = os.path.join(audio_dir, f"{uid}_in.wav")
    out_wav = os.path.join(audio_dir, f"{uid}_out.wav")

    with open(in_webm, "wb") as f:
        f.write(await audio.read())

    audio_path = in_webm
    if ffmpeg_bin and os.path.isfile(ffmpeg_bin):
        try:
            subprocess.run(
                [ffmpeg_bin, "-y", "-i", in_webm, "-ac", "1", "-ar", "16000", in_wav],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
            )
            if os.path.getsize(in_wav) > 0:
                audio_path = in_wav
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg conversion failed:\n{e.stderr}")

    try:
        question = transcribe(audio_path)
    except Exception as e:
        logger.error(f"STT failed: {e}")
        question = ""
    logger.info(f"[STT] Transcript: {question!r}")

    lang = detect_language(question)

    if not question.strip():
        answer, citation = (
            ("Sorry, I couldn't understand the question.", "")
            if lang=="en" else ("عذراً، لم أتمكن من الفهم.", "")
        )
    elif is_greeting(question):
        import random
        answer = random.choice(
            GREETINGS_RESPONSES_EN if lang=="en" else GREETINGS_RESPONSES_AR
        )
        citation = ""
    else:
        chunks = get_relevant_chunks(question, top_k=3)
        if chunks:
            result = generate_answer(chunks, question, chat_history, target_lang=lang)
            answer, citation = result if isinstance(result, tuple) else (result, "")
        else:
            answer, citation = (
                ("Sorry, I don’t know.", "") if lang=="en"
                else ("عذراً، لا أعرف.", "")
            )

    await synthesize(answer, out_wav)
    audio_url = f"/audio/{uid}_out.wav"

    existing = []
    if os.path.exists(hist_path):
        with open(hist_path, "r", encoding="utf-8") as f:
            existing = json.load(f)
    existing.extend([
        {"role": "user",      "text": question},
        {"role": "assistant", "text": answer, "citation": citation, "audio_url": audio_url}
    ])
    with open(hist_path, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    return {
        "session_id":        session_id,
        "transcript":        question,
        "answer":            answer,
        "citation":          citation,
        "audio_url":         audio_url,
        "avatar_waiting":    "/static/avatar waiting.mp4",
        "avatar_speaking":   "/static/avatar talking.mp4",
        "typing_simulation": make_typing_simulation(answer),
    }

# ─── /translate/ endpoint ───
@app.post("/translate/")
async def translate_text(
    request: Request,
    user: str = Depends(get_current_user)
):
    body = await request.json()
    text = body.get("text", "")

    orig   = detect_language(text)
    target = "ar" if orig=="en" else "en"
    prompt = (
        f"{'Translate the following English text into Arabic. Only return the translated text' if target=='ar' else 'Translate the following text into English. Only return the translated text'}:\n\n"
        f"{text}\n\n"
        f"{'الترجمة:' if target=='ar' else 'Translation:'}"
    )

    try:
        resp = llm.generate([prompt])
        translation = resp.generations[0][0].text.strip()
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        translation = text

    uid     = uuid.uuid4().hex
    out_wav = os.path.join(audio_dir, f"{uid}_trans.wav")
    audio_url = None
    try:
        await synthesize(translation, out_wav)
        audio_url = f"/audio/{uid}_trans.wav"
    except Exception as e:
        logger.error(f"TTS for translation failed: {e}")

    return {"translation": translation, "citation": "- Translated by AI", "audio_url": audio_url}

# ─── Session management ───
@app.post("/sessions/new")
async def create_session(user: str = Depends(get_current_user)):
    session_id = uuid.uuid4().hex
    ud = user_dir(user)
    hist_path = os.path.join(ud, f"{session_id}.json")
    with open(hist_path, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)
    meta = load_metadata(user)
    meta[session_id] = session_id[:8]
    save_metadata(user, meta)
    return {"session_id": session_id}

@app.get("/sessions/")
async def list_sessions(user: str = Depends(get_current_user)):
    ud = user_dir(user)
    sessions, meta = [], load_metadata(user)
    for fname in os.listdir(ud):
        if not fname.endswith(".json") or fname == "metadata.json":
            continue
        sid   = fname[:-5]
        fpath = os.path.join(ud, fname)
        mtime = os.path.getmtime(fpath)
        name  = meta.get(sid, sid[:8])
        sessions.append({"session_id": sid, "name": name, "last_modified": mtime})
    sessions.sort(key=lambda x: x["last_modified"], reverse=True)
    return {"sessions": sessions}

@app.get("/sessions/{session_id}/history")
async def get_history(
    session_id: str,
    user: str = Depends(get_current_user)
):
    ud = user_dir(user)
    hist_path = os.path.join(ud, f"{session_id}.json")
    data = []
    if os.path.exists(hist_path):
        with open(hist_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    return {"session_id": session_id, "history": data}

@app.post("/sessions/{session_id}/rename")
async def rename_session_endpoint(
    session_id: str,
    request: Request,
    user: str = Depends(get_current_user)
):
    body     = await request.json()
    new_name = body.get("name", "").strip()
    if not new_name:
        raise HTTPException(status_code=400, detail="Name cannot be empty.")
    meta = load_metadata(user)
    if session_id not in meta:
        raise HTTPException(status_code=404, detail="Session not found.")
    meta[session_id] = new_name
    save_metadata(user, meta)
    return {"session_id": session_id, "name": new_name}

@app.delete("/sessions/{session_id}/delete")
async def delete_session_endpoint(
    session_id: str,
    user: str = Depends(get_current_user)
):
    ud = user_dir(user)
    hist_path = os.path.join(ud, f"{session_id}.json")
    if os.path.exists(hist_path):
        os.remove(hist_path)
    meta = load_metadata(user)
    if session_id in meta:
        del meta[session_id]
        save_metadata(user, meta)
    return {"status": "deleted"}

@app.post("/sessions/{session_id}/autosummary")
async def autosummarize_session(
    session_id: str,
    user: str = Depends(get_current_user),
):
    ud = user_dir(user)
    hist_path = os.path.join(ud, f"{session_id}.json")
    if not os.path.exists(hist_path):
        raise HTTPException(status_code=404, detail="Session not found")
    with open(hist_path, "r", encoding="utf-8") as f:
        conv = json.load(f)
    transcript = "\n".join(f"{m['role'].title()}: {m['text']}" for m in conv)
    prompt = (
        "Please provide a very short, descriptive title (5 words or fewer) "
        "for the following conversation:\n\n"
        f"{transcript}\n\nTitle:"
    )
    try:
        resp = llm.generate([prompt])
        title = resp.generations[0][0].text.strip()
    except Exception:
        title = session_id[:8]
    meta = load_metadata(user)
    meta[session_id] = title
    save_metadata(user, meta)
    return {"session_id": session_id, "name": title}

# ─── Static mounts ───
app.mount("/static",
          StaticFiles(directory=os.path.join(project_root, "Avatar")),
          name="static")
app.mount("/audio",
          StaticFiles(directory=audio_dir),
          name="audio")
