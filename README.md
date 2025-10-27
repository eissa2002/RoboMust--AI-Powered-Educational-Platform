# 🤖 RoboMust - AI-Powered Educational Platform

<div align="center">

**An intelligent voice-enabled learning assistant combining RAG, document intelligence, and interactive study materials**

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Ollama](https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white)](https://ollama.ai/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6F00?style=for-the-badge)](https://www.trychroma.com/)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://www.langchain.com/)
[![Whisper](https://img.shields.io/badge/Whisper-412991?style=for-the-badge&logo=openai&logoColor=white)](https://github.com/openai/whisper)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/)
[![Edge TTS](https://img.shields.io/badge/Edge_TTS-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)](https://github.com/rany2/edge-tts)

[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Jinja2](https://img.shields.io/badge/Jinja2-B41717?style=for-the-badge&logo=jinja&logoColor=white)](https://jinja.palletsprojects.com/)

[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)](https://prometheus.io/)

</div>

---

## 📋 Overview

**RoboMust** is an intelligent AI-powered educational platform that revolutionizes how students interact with course materials. By combining **Retrieval-Augmented Generation (RAG)**, **voice interaction**, and **advanced document processing**, it provides an immersive learning experience for academic institutions.

The platform features a comprehensive **Materials Reading Interface** where students can read, study, and listen to course documents with AI-powered text-to-speech, alongside an **intelligent chatbot** that answers questions based on uploaded course materials. Built with **multilingual support** (English/Arabic), **role-based access control**, and **course management** capabilities.

> **⚠️ Important Note:**  
> This repository represents an **earlier version** of RoboMust for demonstration purposes. The **current production version** includes significantly enhanced features, advanced AI capabilities, and proprietary integrations that are confidential. Key new features in the production version include the **Materials Reading Interface**, **advanced document extraction**, **bulk upload**, **comprehensive analytics dashboards**, and many performance optimizations. If you need screenshots or additional information about the production system, please reach out.

---


<div align="center">


<p align="center">
  <img src="https://github.com/user-attachments/assets/1d29af40-c48f-4d6c-a2be-f2f89356e08c" alt="Animated avatar with waiting and talking states" width="300"/>
</p>

</div>

---

## 🚀 Quick Feature Overview

| Feature | Description | Status |
|---------|-------------|--------|
| 📖 **Materials Reader** | Interactive document viewer with TTS read-aloud | ✅ Production |
| 💬 **AI Chat** | RAG-powered Q&A from course materials | ✅ Production |
| 🎤 **Voice Interface** | Speech-to-text and text-to-speech | ✅ Production |
| 📚 **Course Management** | Multi-course platform with enrollments | ✅ Production |
| 🔐 **Authentication** | Email/Google OAuth with JWT + RBAC | ✅ Production |
| 📊 **Analytics Dashboard** | Course stats, student insights, exports | ✅ Production |
| 🌍 **Multilingual** | Native Arabic + English support | ✅ Production |
| 📄 **Smart Upload** | Bulk upload with AI extraction (Docling) | ✅ Production |
| 🎨 **Modern UI** | Dark/light themes, responsive design | ✅ Production |
| 🔔 **Notifications** | Real-time document alerts | ✅ Production |

---

## ✨ Key Features

### 🔐 **Authentication & Authorization**
- **Multi-provider Authentication**
  - Email/password signup with bcrypt password hashing
  - Google OAuth 2.0 integration for single sign-on
  - JWT-based session management with secure HTTP-only cookies
  
- **Role-Based Access Control (RBAC)**
  - Three role types: `student`, `professor`, `admin`
  - Professor invitation code verification system
  - Dynamic role assignment on first signup
  - Admin privileges via environment configuration
  - Auth state persistence with `/auth/me` endpoint

---

### 📚 **Course Management System**
- **Full CRUD Operations**
  - Course creation (admin-only) with unique course identifiers
  - Course listing (all courses + enrolled courses)
  - Course update (name, description)
  - Course deletion with cascade cleanup
  
- **User-Course Relationships**
  - Professor assignment to courses
  - Bulk student enrollment
  - Student self-enrollment/unenrollment
  - Course-scoped document isolation

---

### 📄 **Intelligent Document Management**
- **Document Upload & Processing**
  - Course-scoped document uploads (professors/admins only)
  - Automatic vector embedding with **ChromaDB** integration
  - Support for multiple formats: PDF, PPTX, DOCX, XLSX
  - Advanced PDF extraction using **Docling** (Granite AI)
  - Drag-and-drop file upload interface
  - File type validation and size limits
  - Bulk document upload with progress tracking
  
- **Document Operations**
  - Document listing by course
  - Document preview modal
  - Document download
  - Document deletion with ChromaDB cleanup
  - Client-side search and filtering
  
---

### 📖 **Materials Reading & Study Interface** ⭐ *NEW FEATURE*

The **Materials page** is a comprehensive document reader designed for immersive studying, featuring advanced text extraction and voice synthesis capabilities.

- **Smart Document Viewer**
  - Clean, distraction-free reading interface optimized for studying
  - Enhanced typography with proper font sizing and line spacing
  - Course-scoped document access (students can only view documents from enrolled courses)
  - Support for multiple formats: **PDF, PPTX, DOCX, XLSX**
  - Real-time document availability checking
  
- **Advanced Text Extraction**
  - **Docling Integration** - IBM Granite AI for superior PDF extraction
    - Handles complex layouts (multi-column, tables, headers/footers)
    - Preserves document structure and formatting
    - Extracts text from images using OCR
    - Support for Arabic and English mixed documents
  - **Asynchronous Processing** - Background extraction with progress tracking
  - **Smart Caching** - Extracted content cached for instant loading
  - **Fallback Systems** - PyMuPDF, python-docx, python-pptx for various formats
  - Cache management with manual clear option
  
- **Read-Aloud (Text-to-Speech) Feature** 🔊
  - **One-Click Audio Generation** - "Read Aloud" button for instant voice narration
  - **High-Quality TTS** - Edge TTS engine with natural-sounding voices
  - **Automatic Language Detection** - Detects Arabic/English and selects appropriate voice
  - **Section-Based Reading** - Read specific sections or entire documents
  - **Audio Streaming** - Progressive audio playback without waiting for full generation
  - **Pause/Resume Controls** - Full audio player with playback controls
  - **Speed Adjustment** - Control reading speed for optimal comprehension
  - **Background Processing** - Non-blocking audio generation
  
- **Study Tools**
  - Section navigation with jump-to-section functionality
  - Progress tracking (current section indicator)
  - Scroll position preservation
  - Responsive design for mobile studying
  - Dark mode support for comfortable reading
  
- **Performance Optimizations**
  - Lazy loading for large documents
  - Incremental text rendering
  - Cached extraction results stored in `data/extracted_cache/`
  - Task-based extraction status tracking
  - Automatic cleanup of stale cache entries

**Materials Router Endpoints:**
- `GET /materials/{course_id}/{filename}` - Document reader interface
- `POST /materials/api/content/{course_id}/{filename}/start` - Start async extraction
- `GET /materials/api/content/{course_id}/{filename}/status/{task_id}` - Check extraction progress
- `GET /materials/api/content/{course_id}/{filename}` - Get extracted content
- `POST /materials/api/read-aloud` - Generate TTS audio for text
- `POST /materials/api/clear-cache` - Clear extraction cache

---

### 💬 **RAG-Powered Chat System**
- **Intelligent Question Answering**
  - Course-scoped RAG retrieval from uploaded documents
  - Context-aware responses with source citations
  - Page reference extraction for accurate attribution
  - Greeting detection (English/Arabic)
  - Multilingual support with automatic language detection
  
- **Conversation Management**
  - Session-based chat history
  - Create, list, rename, and delete sessions
  - Auto-summary generation for past conversations
  - Persistent message history per session
  
- **Retrieval Engine**
  - **ChromaDB** vector database for semantic search
  - **FAISS** alternative for fast similarity search
  - Hybrid search capabilities (keyword + semantic)
  - Custom embedding models via sentence-transformers
  - LangChain integration for flexible retrieval chains

---

### 🎤 **Voice Features**
- **Speech-to-Text (STT)**
  - **Whisper** integration with automatic language detection
  - **Vosk** for offline multilingual recognition
  - **SpeechRecognition** library for fast, accurate transcription
  - Support for Arabic and English
  - Audio format conversion (webm → wav via ffmpeg)
  
- **Text-to-Speech (TTS)**
  - **Edge TTS** for high-quality voice synthesis
  - Automatic language detection for Arabic/English
  - Multiple voice options
  - Streaming audio playback
  
- **Audio Processing**
  - Real-time voice recording in browser
  - Audio playback controls
  - Format conversion and optimization
  - Secure audio file handling

---

### 📊 **Statistics & Analytics**
- **Overview Dashboard**
  - System-wide statistics (total users, courses, documents)
  - Activity summaries and trends
  
- **Course Analytics**
  - Enrolled student count per course
  - Document count by course
  - Recent upload activity
  - Course engagement metrics
  
- **Student Insights**
  - Individual student activity tracking
  - Course participation metrics
  
- **Search Analytics**
  - Query pattern analysis
  - Popular search terms
  
- **System Health Monitoring**
  - Model status tracking
  - Performance metrics
  - Alert system for anomalies
  
- **Data Export**
  - CSV/JSON export capabilities
  - Custom date ranges and filters

---

### 🎨 **Modern User Interface**
- **Responsive Design**
  - Mobile-friendly responsive layout
  - Clean, intuitive navigation
  - Modal-based workflows
  
- **Theme System**
  - Dark/light theme toggle
  - CSS variable-based theming
  - Theme persistence via localStorage
  - Theme-aware Google Sign-In button
  
- **Enhanced UX**
  - Loading states with skeleton loaders
  - Button loading spinners
  - Smooth fade-in animations
  - Toast notifications (theme-aware)
  - Upload progress indicators
  - Animated avatar with waiting/talking states
  - Typing simulation for AI responses
  - Role toggle UI (student/professor pills)

---

### 🛠️ **Technical Infrastructure**

#### **Backend Architecture**
- **FastAPI** RESTful API with modular router design
- **Modular Structure:**
  ```
  /routers
    ├── auth.py          # Authentication & authorization
    ├── courses.py       # Course management
    ├── docs.py          # Document operations
    ├── materials.py     # Document reading & read-aloud
    ├── chat.py          # Chat interface
    ├── ask.py           # Question answering
    ├── transcribe.py    # Speech-to-text
    ├── translate.py     # Translation services
    ├── sessions.py      # Chat session management
    ├── statistics.py    # Analytics & reporting
    └── admin.py         # Admin operations
  ```

#### **AI & ML Stack**
- **LLM Integration:** OpenAI GPT models, Ollama for local inference
- **Embeddings:** Sentence-Transformers, HuggingFace models
- **Document AI:** Docling (IBM Granite) for advanced PDF extraction
- **Vector Databases:** ChromaDB (primary), FAISS (alternative)
- **Framework:** LangChain for RAG pipelines and conversation chains

#### **Data Persistence**
- **Vector Storage:** ChromaDB for semantic search
- **File Storage:** Course-scoped file system (`data/raw/<course_id>/`)
- **User Data:** JSON-based storage for users, courses, enrollments
- **Session Data:** Persistent chat history in JSON format
- **Cache:** Extracted content caching for performance optimization

#### **Security Features**
- **Password Hashing:** bcrypt for secure password storage
- **JWT Tokens:** HTTP-only cookies for session management
- **CORS Configuration:** Configurable cross-origin policies
- **Environment Variables:** Secrets management via `.env`
- **Role-Based Access:** Fine-grained permission controls
- **OAuth 2.0:** Google authentication integration

#### **Performance Optimizations**
- **Model Preloading:** Parallel model loading on startup for optimal performance
- **Health Check Endpoint:** `/health` with model status reporting
- **Caching:** Document extraction caching to reduce processing time
- **Async Operations:** FastAPI async endpoints for concurrent requests
- **Streaming Responses:** Efficient large file handling

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (HTML/JS)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Chat UI     │  │ Documents UI │  │  Admin UI    │      │
│  │  + Voice     │  │  + Materials │  │  + Analytics │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↓ REST API
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Auth Router  │  │ Docs Router  │  │ Chat Router  │      │
│  │ STT Router   │  │ TTS Router   │  │ Stats Router │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                      AI/ML Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Whisper    │  │   OpenAI     │  │   Docling    │      │
│  │   (STT)      │  │   (LLM)      │  │   (Extract)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  ChromaDB    │  │  File System │  │  JSON Store  │      │
│  │  (Vectors)   │  │  (Documents) │  │  (Metadata)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Technology Stack

### Currently Implemented (Demo Version)

| Category | Technologies |
|----------|-------------|
| **Backend** | FastAPI, Python 3.8+, Uvicorn |
| **AI/LLM** | Ollama (local inference), LangChain, HuggingFace Transformers |
| **Vector DB** | ChromaDB, FAISS |
| **Document AI** | Docling (IBM Granite), PyMuPDF, python-docx, python-pptx |
| **Speech** | Whisper (OpenAI), Vosk, SpeechRecognition, Edge TTS |
| **Authentication** | JWT (python-jose), Google OAuth 2.0, Bcrypt (passlib) |
| **Audio Processing** | FFmpeg, pydub |
| **Embeddings** | sentence-transformers, HuggingFace embeddings |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla), Jinja2 Templates |
| **Data Storage** | JSON-based storage, File system |

### Planned for Future Implementation

| Category | Technologies | Purpose |
|----------|-------------|---------|
| **Database** | PostgreSQL | Relational data storage for users, courses, and metadata |
| **Containerization** | Docker, Docker Compose | Application containerization and deployment |
| **Monitoring** | Prometheus | Metrics collection and performance monitoring |
| **Visualization** | Grafana | Real-time dashboards and analytics visualization |
| **Cloud Services** | OpenAI GPT API | Enhanced LLM capabilities for production |

---

## 📦 Installation

> **Note:** This is a demonstration version. The full production system includes additional dependencies and configuration not shown here.

### Prerequisites
- Python 3.8 or higher
- FFmpeg (for audio processing)
- Ollama (for local LLM inference) - [Download here](https://ollama.ai/)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/eissa2002/Voice-Enabled-RAG-Tutor.git
   cd voice-chatbot-v5
   ```

2. **Create virtual environment**
   ```bash
   python -m venv chatbot
   # Windows
   chatbot\Scripts\activate
   # Linux/Mac
   source chatbot/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install and configure Ollama**
   ```bash
   # Pull the model used in this demo
   ollama pull qwen2.5:1.5b
   ```

5. **Configure environment variables** (Optional)
   Create a `.env` file in the project root for optional features:
   ```env
   # JWT Secret (generate with: openssl rand -hex 32)
   JWT_SECRET=your_secret_key_here
   
   # Admin Configuration (optional)
   ADMIN_EMAILS=admin@example.com
   
   # Google OAuth (optional - not included in demo)
   # GOOGLE_CLIENT_ID=your_google_client_id
   # GOOGLE_CLIENT_SECRET=your_google_client_secret
   
   # Professor Invitation Code (optional)
   PROFESSOR_INVITE_CODE=demo123
   ```

6. **Run the server**
   ```bash
   # Development
   uvicorn online.server:app --reload --host 0.0.0.0 --port 8000
   
   # Or use the provided script (Windows)
   start_server.bat
   ```

7. **Access the application**
   ```
   http://localhost:8000
   ```

### First-Time Setup

1. **Create an account** - Sign up with email/password
2. **Create a course** (admin role required for demo)
3. **Upload documents** - Add PDFs, DOCX, or PPTX files
4. **Start chatting** - Ask questions about your uploaded materials

---

## �📖 Usage

### For Students
1. **Sign up** with email/password or Google account
2. **Enroll** in available courses
3. **Upload** documents to course libraries (if permitted)
4. **Chat** with the AI tutor about course materials
5. **Use voice** for hands-free interaction
6. **Read materials** with text-to-speech support

### For Professors
1. **Create courses** (if admin) or get assigned by admin
2. **Upload** course materials (PDFs, PPTX, DOCX, XLSX)
3. **Manage** student enrollments
4. **Monitor** course analytics and document usage
5. **Review** student chat interactions (if enabled)

### For Administrators
1. **Create and manage** all courses
2. **Assign** professors to courses
3. **Manage** user roles and permissions
4. **View analytics** across all courses and users
5. **Export** data for reporting
6. **Monitor** system health and performance

---

## 🗂️ API Endpoints

<details>
<summary><b>Authentication</b></summary>

- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login with credentials
- `POST /auth/google` - Google OAuth login
- `GET /auth/me` - Get current user info
- `POST /auth/logout` - Logout user

</details>

<details>
<summary><b>Courses</b></summary>

- `GET /courses` - List all courses
- `GET /courses/my` - List enrolled courses
- `POST /courses` - Create course (admin)
- `PUT /courses/{id}` - Update course
- `DELETE /courses/{id}` - Delete course (admin)
- `POST /courses/{id}/enroll` - Enroll in course
- `POST /courses/{id}/unenroll` - Unenroll from course
- `POST /courses/{id}/assign-professor` - Assign professor (admin)
- `POST /courses/{id}/assign-students` - Bulk assign students (admin)

</details>

<details>
<summary><b>Documents</b></summary>

- `GET /documents` - Document management page
- `GET /documents/list?course_id=X` - List course documents
- `POST /documents/upload` - Upload document
- `POST /documents/bulk-upload` - Upload multiple documents
- `DELETE /documents/delete?path=X` - Delete document
- `GET /docs/raw/{path}` - Download document

</details>

<details>
<summary><b>Materials (Reading Interface)</b></summary>

- `GET /materials/{course_id}/{filename}` - View document reader
- `GET /materials/api/content/{course_id}/{filename}` - Get document content
- `POST /materials/api/content/{course_id}/{filename}/start` - Start extraction
- `GET /materials/api/content/{course_id}/{filename}/status/{task_id}` - Check extraction status
- `POST /materials/api/read-aloud` - Generate TTS audio
- `POST /materials/api/clear-cache` - Clear extraction cache

</details>

<details>
<summary><b>Chat & AI</b></summary>

- `POST /ask` - Ask question about course materials
- `POST /chat` - Send chat message
- `POST /translate` - Translate text
- `POST /sessions/new` - Create new chat session
- `GET /sessions` - List user sessions
- `GET /sessions/{id}/history` - Get session history
- `POST /sessions/{id}/rename` - Rename session
- `DELETE /sessions/{id}/delete` - Delete session
- `POST /sessions/{id}/autosummary` - Generate session summary

</details>

<details>
<summary><b>Voice</b></summary>

- `POST /stt/transcribe` - Transcribe audio to text
- `POST /stt/transcribe_public` - Public transcription endpoint
- `POST /tts/synthesize` - Convert text to speech

</details>

<details>
<summary><b>Statistics & Analytics</b></summary>

- `GET /statistics/overview` - System overview
- `GET /statistics/courses` - Course analytics
- `GET /statistics/courses/{id}` - Specific course stats
- `GET /statistics/activity` - Activity timeline (admin)
- `GET /statistics/students` - Student insights
- `GET /statistics/search` - Search analytics
- `GET /statistics/health` - System health (admin)
- `GET /statistics/alerts` - System alerts
- `GET /statistics/export/{type}` - Export data

</details>

<details>
<summary><b>Admin</b></summary>

- `GET /admin/users` - List all users
- `POST /admin/users/role` - Modify user role
- `GET /admin` - Admin dashboard

</details>

---

## 🔒 Security Features

- **Password Security:** Bcrypt hashing with salt
- **Session Management:** JWT tokens with expiration
- **HTTP-only Cookies:** Protection against XSS attacks
- **CORS Configuration:** Controlled cross-origin access
- **Role-Based Access Control:** Fine-grained permissions
- **Environment Variables:** Secrets management
- **Input Validation:** Pydantic models for request validation
- **File Upload Restrictions:** Type and size validation

---

## 🌍 Multilingual Support

The system automatically detects and handles:
- **English** - Full support for English conversations and documents
- **Arabic** - Native Arabic language support with proper RTL rendering
- **Auto-detection** - Automatic language detection in chat and voice
- **Mixed Content** - Handles documents with both English and Arabic text

---

## 🎯 Use Cases

- **Educational Institutions:** Virtual teaching assistant for students with course-specific knowledge
- **Corporate Training:** Internal knowledge base with voice interaction and multilingual support
- **Documentation Systems:** Searchable document libraries with AI-powered Q&A
- **Research Platforms:** Academic paper analysis with citation and source tracking
- **E-Learning Platforms:** Comprehensive course material management with intelligent tutoring
- **Accessibility:** Text-to-speech reading for students with visual impairments or reading difficulties
- **Self-Study:** Independent learning with AI tutor available 24/7

---

## 🌟 What Makes RoboMust Unique?

Unlike traditional learning management systems, RoboMust combines multiple AI technologies into a seamless experience:

1. **Integrated Reading + Chat Experience** - Students can read materials and ask questions without switching platforms
2. **Voice-First Design** - Natural voice interaction makes learning more accessible
3. **Course-Scoped Intelligence** - AI responses are contextually aware of specific course materials
4. **Multilingual Core** - Native support for English and Arabic (not just translation)
5. **Advanced Document AI** - IBM Granite Docling handles complex PDFs that other systems struggle with
6. **Read-Aloud Study Mode** - Converts any document into an audiobook-like experience
7. **Role-Based Education Model** - Purpose-built for student/professor/admin workflows
8. **Privacy-Focused** - Course-scoped data isolation ensures student privacy

---

## 🚧 Future Roadmap

The following enhancements are planned for future implementation in the production version:

### Infrastructure & Deployment
- **🐳 Docker Containerization** - Full Docker and Docker Compose setup for easy deployment and scalability
- **📊 Monitoring & Observability**
  - **Prometheus** - Metrics collection for application performance, LLM inference times, and system resources
  - **Grafana** - Real-time dashboards for monitoring course activity, user engagement, and system health
  
### Database & Storage
- **🗄️ PostgreSQL Integration** - Migration from JSON-based storage to PostgreSQL for:
  - Improved scalability and performance
  - Better relational data management
  - Advanced querying capabilities
  - Transaction support and data integrity

### AI & Cloud Services
- **☁️ OpenAI GPT API** - Enhanced LLM capabilities with cloud-based models for production environments

### Performance Enhancements
- Horizontal scaling with load balancing
- Redis caching for improved response times
- CDN integration for static assets
- Database connection pooling and optimization

---

## 📝 License

**Proprietary Software** - RoboMust is confidential educational platform software developed for institutional use.

---

## 🔄 Version Information

**This Repository:** Contains an earlier demonstration version of RoboMust  
**Production Version:** Includes advanced features not shown here:
- Enhanced Materials Reading Interface with async extraction
- Bulk document upload with progress tracking  
- Comprehensive statistics dashboards with data export
- Advanced caching and performance optimizations
- Additional AI-powered study tools
- Proprietary integrations and business logic

The production system is actively deployed in educational institutions and is not publicly available for confidentiality reasons.

---

## 📸 Screenshots & Documentation

For screenshots of the production system or additional documentation about advanced features, feel free to reach out.

---

## 👤 Author & Credits

**RoboMust** is developed and maintained by **[Eissa Islam](https://github.com/eissa2002)**

**Core Development (Solo):**
- 🔧 Full-stack development (Frontend + Backend + AI/ML)
- 🤖 AI/RAG pipeline implementation and optimization
- 📊 Analytics and statistics system
- 🔐 Authentication and security architecture
- 🎤 Voice features (STT/TTS) integration
- 📖 Materials reading interface with async extraction
- � Chat system and conversation management
- 📚 Course management and document handling

**Design Contributions:**
- 🎨 Homepage UI/UX design - Team collaboration
- � Avatar design and animations - Team collaboration

> Special thanks to team members who contributed design assets for the homepage and avatar animations.

---

## 🤝 Contact & Support

For questions, feature requests, collaboration opportunities, or to learn more about the production version:

- **GitHub:** [@eissa2002](https://github.com/eissa2002)
- **Email:** eissaislam.buss@gmail.com

---

## ⚠️ Disclaimer

This repository represents an **earlier version** of RoboMust and is intended for **demonstration purposes only**. The current production deployment includes significantly more features, optimizations, and proprietary components that are not included in this public repository. Many advanced capabilities, production configurations, and sensitive business logic remain confidential.

---

<div align="center">

**Built with ❤️ for Education**

*Empowering students through AI-powered learning*

</div>
