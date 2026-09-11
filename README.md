<div align="center">

# 🤖 DOCUMIND AI

### `AI-POWERED DOCUMENT INTELLIGENCE PLATFORM`

**Understand your documents. Ask better questions. Keep your data local.**

<br>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:050816,50:0b1630,100:111827&height=200&section=header&text=DOCUMIND%20AI&fontSize=54&fontColor=00E5FF&animation=fadeIn&fontAlignY=38&desc=LOCAL%20RAG%20%7C%20PRIVATE%20AI%20%7C%20DOCUMENT%20INTELLIGENCE&descAlignY=63&descSize=16&descColor=9CA3AF" width="100%" alt="DocuMind AI Header"/>

<br>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&duration=2800&pause=900&color=00E5FF&center=true&vCenter=true&width=850&lines=Local-First+AI+Document+Intelligence;Semantic+Search+%2B+RAG;Ask+Questions+About+Your+Documents;Private+Knowledge+%7C+Local+Inference;Your+Documents.+Your+Infrastructure.+Your+AI." alt="Typing Animation"/>

<br><br>

[![Python](https://img.shields.io/badge/Python-3.12+-00E5FF?style=for-the-badge\&logo=python\&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-009688?style=for-the-badge\&logo=fastapi\&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-TypeScript-61DAFB?style=for-the-badge\&logo=react\&logoColor=111827)](https://react.dev/)
[![Ollama](https://img.shields.io/badge/Ollama-LOCAL_LLM-black?style=for-the-badge)](https://ollama.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-VECTOR_DB-FF6F61?style=for-the-badge)](https://www.trychroma.com/)
[![Docker](https://img.shields.io/badge/Docker-SUPPORTED-2496ED?style=for-the-badge\&logo=docker\&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-00E5FF?style=for-the-badge)](LICENSE)

<br>

`[ SYSTEM ONLINE ]` · `[ RAG ENGINE READY ]` · `[ LOCAL AI ACTIVE ]`

</div>

---

# 🧠 SYSTEM OVERVIEW

> **DocuMind AI is a local-first document intelligence platform that transforms static documents into an intelligent, searchable knowledge system.**

Upload your:

* 📄 PDF files
* 📝 DOCX documents
* 📃 TXT files
* 🧾 Markdown files

DocuMind validates, extracts, cleans, chunks, embeds and indexes your documents.

You can then search your documents semantically or ask questions in natural language.

The RAG engine retrieves relevant document context and passes it to a local LLM through **Ollama**, producing grounded responses with source information.

### Core Principle

```text
                    YOUR DOCUMENTS
                           │
                           ▼
                    ┌─────────────┐
                    │  VALIDATE   │
                    └──────┬──────┘
                           ▼
                    ┌─────────────┐
                    │  EXTRACT    │
                    └──────┬──────┘
                           ▼
                    ┌─────────────┐
                    │   CLEAN     │
                    └──────┬──────┘
                           ▼
                    ┌─────────────┐
                    │   CHUNK     │
                    └──────┬──────┘
                           ▼
                    ┌─────────────┐
                    │  EMBEDDING  │
                    └──────┬──────┘
                           ▼
                    ┌─────────────┐
                    │  CHROMADB   │
                    └──────┬──────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ RETRIEVAL + OLLAMA  │
                └──────────┬──────────┘
                           ▼
                  ANSWER + CITATIONS
```

---

# ⚡ WHY DOCUMIND AI?

DocuMind is more than a basic PDF chatbot.

It combines:

| Capability              | Description                                                      |
| ----------------------- | ---------------------------------------------------------------- |
| 🔐 Local-First AI       | Keep AI inference and document processing on your infrastructure |
| 🧠 RAG                  | Generate answers using retrieved document context                |
| 🔎 Semantic Search      | Search by meaning instead of exact keywords                      |
| 📚 Citations            | Connect answers to retrieved document sources                    |
| 👤 User Isolation       | Keep each user's knowledge space separated                       |
| 💬 Chat Memory          | Preserve document conversations                                  |
| 📊 Analytics            | Track real application usage                                     |
| ⚙️ Processing Pipeline  | Validate → Extract → Chunk → Embed → Index                       |
| 🔌 Provider Abstraction | Swap AI/vector/document providers                                |
| 🚀 REST API             | FastAPI-powered backend                                          |
| 🐳 Docker               | Containerized deployment support                                 |
| 🧪 Testing              | Unit, API and security-oriented testing                          |

---

# 🖥️ INTERFACE SHOWCASE

DocuMind provides a modern interface for authentication, document management, AI conversations, analytics and API interaction.

---

## `01 — SPLASH SCREEN`

<p align="center">
<img src="Screenshots/Splash.png" width="92%" alt="DocuMind AI Splash Screen"/>
</p>

> **Initializing the DocuMind intelligence layer...**

---

## `02 — LOGIN // AUTHENTICATION`

<p align="center">
<img src="Screenshots/Login Account.png" width="92%" alt="DocuMind AI Login"/>
</p>

Secure authentication creates an isolated workspace for every user.

### Authentication includes

* JWT authentication
* Secure password hashing
* Validation
* Protected routes
* User-specific resources

---

## `03 — REGISTRATION // CREATE WORKSPACE`

<p align="center">
<img src="Screenshots/Register Account.png" width="92%" alt="DocuMind AI Registration"/>
</p>

Users can create their own private DocuMind workspace for documents, conversations and analytics.

---

## `04 — DASHBOARD // COMMAND CENTER`

<p align="center">
<img src="Screenshots/Dashboard.png" width="92%" alt="DocuMind AI Dashboard"/>
</p>

The dashboard acts as the central command center.

```text
┌──────────────┐
│  DOCUMENTS   │
└──────┬───────┘
       │
┌──────▼───────┐
│  PROCESSED   │
└──────┬───────┘
       │
┌──────▼──────────┐
│  CONVERSATIONS  │
└──────┬──────────┘
       │
┌──────▼──────────┐
│    STORAGE      │
└──────┬──────────┘
       │
       ▼
 REAL APPLICATION DATA
```

Dashboard information includes:

* Total documents
* Processed documents
* Conversations
* Storage usage
* Recent documents
* Recent conversations
* Processing status

---

## `05 — AI CHAT // NEURAL INTERFACE`

<p align="center">
<img src="Screenshots/AI Powered Chats.png" width="92%" alt="DocuMind AI Chat"/>
</p>

Ask natural-language questions about your indexed documents.

```text
USER QUESTION
      │
      ▼
QUESTION EMBEDDING
      │
      ▼
VECTOR RETRIEVAL
      │
      ▼
RELEVANT CHUNKS
      │
      ▼
CONTEXT CONSTRUCTION
      │
      ▼
LOCAL LLM / OLLAMA
      │
      ▼
AI RESPONSE
```

The system retrieves relevant document context before generating the response.

---

## `06 — CHAT MEMORY // CONVERSATION HISTORY`

<p align="center">
<img src="Screenshots/Chat History.png" width="92%" alt="DocuMind AI Chat History"/>
</p>

Persistent conversation history keeps previous document interactions accessible.

This allows users to continue working with their document knowledge without losing previous conversations.

---

## `07 — ANALYTICS // TELEMETRY`

<p align="center">
<img src="Screenshots/Analytics.png" width="92%" alt="DocuMind AI Analytics"/>
</p>

DocuMind provides meaningful application analytics including:

* Documents uploaded
* Documents processed
* Pages processed
* Chunks indexed
* Questions asked
* Processing time
* Response latency
* Document usage

> Analytics are based on application data rather than intentionally fabricated statistics.

---

# 📡 API // MACHINE INTERFACE

DocuMind exposes a structured REST API under:

```text
/api/v1
```

### Authentication

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/logout
```

### Documents

```text
POST   /api/v1/documents
GET    /api/v1/documents
GET    /api/v1/documents/{id}
DELETE /api/v1/documents/{id}
GET    /api/v1/documents/{id}/status
```

### Chat

```text
POST /api/v1/chat
```

### Conversations

```text
GET    /api/v1/conversations
GET    /api/v1/conversations/{id}
DELETE /api/v1/conversations/{id}
```

### Search

```text
GET /api/v1/search
```

### Analytics

```text
GET /api/v1/analytics
```

### Health

```text
GET /health
GET /api/v1/health
```

---

# 📚 API DOCUMENTATION

## `08 — SWAGGER DOCUMENTATION`

<p align="center">
<img src="Screenshots/API Documentation.png" width="92%" alt="DocuMind Swagger API Documentation"/>
</p>

Interactive API documentation makes development and testing easier.

---

## `09 — EXTENDED API DOCUMENTATION`

<p align="center">
<img src="Screenshots/API Documentation 2.png" width="92%" alt="DocuMind Extended API Documentation"/>
</p>

Explore endpoints, request schemas, authentication and API responses.

---

## `10 — API INTERFACE`

<p align="center">
<img src="Screenshots/API.png" width="92%" alt="DocuMind API Interface"/>
</p>

The API provides the machine interface connecting the frontend with the DocuMind backend services.

---

# 🧬 RAG ENGINE

DocuMind follows a Retrieval-Augmented Generation architecture.

```text
                  DOCUMENT
                     │
                     ▼
                VALIDATION
                     │
                     ▼
              TEXT EXTRACTION
                     │
                     ▼
                  CLEANING
                     │
                     ▼
                  CHUNKING
                     │
                     ▼
              LOCAL EMBEDDINGS
                     │
                     ▼
                  CHROMADB
                     │
                     ▼
              VECTOR RETRIEVAL
                     │
                     ▼
              RELEVANT CHUNKS
                     │
                     ▼
             CONTEXT BUILDING
                     │
                     ▼
                   OLLAMA
                     │
                     ▼
                 LOCAL LLM
                     │
                     ▼
              ANSWER + SOURCES
```

### Two major flows

**Document ingestion**

```text
UPLOAD
  ↓
VALIDATE
  ↓
EXTRACT
  ↓
CLEAN
  ↓
CHUNK
  ↓
EMBED
  ↓
INDEX
  ↓
READY
```

**Question answering**

```text
QUESTION
  ↓
EMBED QUERY
  ↓
VECTOR SEARCH
  ↓
RETRIEVE CONTEXT
  ↓
BUILD PROMPT
  ↓
OLLAMA
  ↓
ANSWER + CITATIONS
```

---

# 🔌 AI PROVIDER ARCHITECTURE

DocuMind is intentionally designed around provider abstractions.

```text
                         DOCUMIND CORE
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
         LLM PROVIDER    EMBEDDING PROVIDER  VECTOR STORE
              │               │               │
              ▼               ▼               ▼
           Ollama       Sentence Transformers ChromaDB
```

Core abstractions include:

```text
LLMProvider
EmbeddingProvider
VectorStore
DocumentExtractor
```

This makes alternative providers easier to introduce without rewriting the complete RAG architecture.

---

# 🔐 SECURITY // PRIVACY

DocuMind is designed around a **local-first privacy model**.

### User Isolation

```text
USER A                         USER B
  │                              │
  ├── Documents A                ├── Documents B
  ├── Chunks A                   ├── Chunks B
  └── Conversations A            └── Conversations B
```

A user cannot intentionally retrieve another user's documents through:

* Document APIs
* Semantic search
* Vector retrieval
* Chat/RAG
* Delete operations
* Conversation endpoints

### Security mechanisms

```text
✓ JWT authentication
✓ Bcrypt password hashing
✓ Ownership checks
✓ UUID-based identifiers
✓ MIME / extension validation
✓ File-size validation
✓ SHA-256 duplicate detection
✓ Safe generated filenames
✓ Path traversal protection
✓ Parameterized SQL queries
✓ Secure CORS configuration
✓ Environment-based secrets
✓ No credentials in logs
✓ No document contents in logs
```

---

# 📄 SUPPORTED DOCUMENTS

|  Format  | Support |
| :------: | :-----: |
|    PDF   |    ✅    |
|   DOCX   |    ✅    |
|    TXT   |    ✅    |
| Markdown |    ✅    |

The extraction layer uses a provider-based architecture, making future document formats easier to integrate.

---

# ⚙️ DOCUMENT PROCESSING

Every uploaded document follows a controlled pipeline:

```text
┌──────────────┐
│    UPLOAD    │
└──────┬───────┘
       ▼
┌──────────────┐
│   VALIDATE   │
└──────┬───────┘
       ▼
┌──────────────┐
│   CHECKSUM   │
└──────┬───────┘
       ▼
┌──────────────┐
│   EXTRACT    │
└──────┬───────┘
       ▼
┌──────────────┐
│    CLEAN     │
└──────┬───────┘
       ▼
┌──────────────┐
│    CHUNK     │
└──────┬───────┘
       ▼
┌──────────────┐
│    EMBED     │
└──────┬───────┘
       ▼
┌──────────────┐
│    INDEX     │
└──────┬───────┘
       ▼
     READY
```

A failed document does not intentionally crash the complete API.

Its processing state and error information are retained against the document.

---

# 🏗️ SYSTEM ARCHITECTURE

```text
                         ┌───────────────┐
                         │     USER      │
                         └───────┬───────┘
                                 │
                                 ▼
                     ┌─────────────────────┐
                     │ React + TypeScript  │
                     └──────────┬──────────┘
                                │
                           REST / JWT
                                │
                                ▼
                     ┌─────────────────────┐
                     │       FastAPI       │
                     └──────────┬──────────┘
                                │
          ┌─────────────────────┼─────────────────────┐
          │                     │                     │
          ▼                     ▼                     ▼
   AUTHENTICATION        DOCUMENT SERVICE       CHAT SERVICE
                                │                     │
                                ▼                     │
                         TEXT EXTRACTION              │
                                │                     │
                                ▼                     │
                            CHUNKING                  │
                                │                     │
                                ▼                     │
                        EMBEDDING MODEL               │
                                │                     │
                                ▼                     │
                            CHROMADB ◄────────────────┘
                                │
                                ▼
                             OLLAMA
                                │
                                ▼
                           LOCAL LLM
```

---

# 🧰 TECHNOLOGY STACK

| Layer              | Technology            |
| ------------------ | --------------------- |
| 🐍 Backend         | Python 3.12+          |
| ⚡ API              | FastAPI               |
| 🗃️ ORM            | SQLAlchemy 2          |
| ✅ Validation       | Pydantic v2           |
| 🔐 Authentication  | JWT + bcrypt          |
| 🗄️ Migrations     | Alembic               |
| 🧠 Embeddings      | Sentence Transformers |
| 🤖 LLM Runtime     | Ollama                |
| 🧬 Vector Database | ChromaDB              |
| 📄 PDF Extraction  | PyMuPDF               |
| 📝 DOCX Extraction | python-docx           |
| ⚛️ Frontend        | React                 |
| 📘 Language        | TypeScript            |
| ⚡ Build Tool       | Vite                  |
| 🧪 Testing         | Pytest                |
| 🧹 Linting         | Ruff                  |
| 🐳 Containers      | Docker                |
| 🔗 Orchestration   | Docker Compose        |
| 🔄 CI              | GitHub Actions        |

---

# 💰 ZERO-COST LOCAL AI

The default DocuMind architecture does **not require paid AI APIs**.

You do not need:

```text
✗ OpenAI API
✗ Anthropic API
✗ Google Gemini API
✗ Pinecone
✗ AWS
✗ Azure
✗ Paid vector databases
✗ Paid inference APIs
```

Instead:

```text
DOCUMENTS
    │
    ▼
LOCAL EMBEDDINGS
    │
    ▼
CHROMADB
    │
    ▼
OLLAMA
    │
    ▼
LOCAL LLM
    │
    ▼
PRIVATE ANSWERS
```

> **Your documents can remain on your machine.**

---

# 🚀 QUICK START

## Requirements

Install:

* Python 3.12+
* Node.js 18+
* Ollama
* Git
* Docker *(optional)*

---

## 1. Clone Repository

```bash
git clone https://github.com/MUdevelops/Documind_AI.git
cd Documind_AI
```

---

## 2. Create Python Environment

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Backend

```bash
pip install -e ".[dev]"
```

---

## 4. Configure Environment

### Windows

```powershell
copy .env.example .env
```

### Linux / macOS

```bash
cp .env.example .env
```

Review your environment configuration before starting the application.

> ⚠️ Never commit `.env`.

---

# 🤖 ACTIVATE LOCAL AI

Install Ollama and download the configured local model.

```bash
ollama pull llama3.1
```

Start Ollama:

```bash
ollama serve
```

Check installed models:

```bash
ollama list
```

DocuMind uses Sentence Transformers for local embeddings.

The configured embedding model is downloaded once and cached locally.

---

# 🗄️ DATABASE SETUP

Run migrations:

```bash
alembic upgrade head
```

Check migration state:

```bash
alembic current
```

---

# ▶️ START BACKEND

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

---

# 🎨 START FRONTEND

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

# 🐳 DOCKER MODE

Build and start:

```bash
docker compose up --build
```

Check containers:

```bash
docker compose ps
```

Stop services:

```bash
docker compose down
```

If Ollama is configured as a Compose service:

```bash
docker compose exec ollama ollama pull llama3.1
```

---

# 🧪 TESTING

Run the complete test suite:

```bash
pytest
```

Lint:

```bash
ruff check .
```

Formatting:

```bash
ruff format --check .
```

Recommended development workflow:

```bash
ruff check .
ruff format --check .
pytest
```

Testing covers areas such as:

```text
UNIT TESTS
   │
   ├── Extraction
   ├── Cleaning
   ├── Chunking
   ├── Embeddings
   ├── Retrieval
   └── Authentication

API TESTS
   │
   ├── Registration
   ├── Login
   ├── Documents
   ├── Search
   ├── Chat
   └── Analytics

SECURITY TESTS
   │
   └── Cross-user isolation
```

---

# 🩺 HEALTH MONITORING

DocuMind exposes health information for major system dependencies:

```text
                  APPLICATION
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      DATABASE     VECTOR STORE     LLM
```

Available endpoints:

```text
GET /health
GET /api/v1/health
```

These help troubleshoot local deployments without exposing sensitive configuration.

---

# 🛠️ CLI

### Health

```bash
python -m app.cli health
```

### Reindex Documents

```bash
python -m app.cli reindex
```

### Create Administrator

```bash
python -m app.cli create-admin \
  --email admin@example.com \
  --password changeme123
```

> ⚠️ Demo credentials should only be used for local development.

---

# ⚙️ ENVIRONMENT VARIABLES

Example configuration:

```env
DATABASE_URL=
SECRET_KEY=

VECTOR_DB_PATH=

LLM_PROVIDER=
LLM_MODEL=

EMBEDDING_MODEL=

MAX_UPLOAD_SIZE=

CORS_ORIGINS=

CHUNK_SIZE=
CHUNK_OVERLAP=

TOP_K=
SIMILARITY_THRESHOLD=
```

See:

```text
.env.example
```

for the complete configuration.

---

# 📁 PROJECT STRUCTURE

```text
Documind_AI/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── repositories/
│   ├── services/
│   ├── providers/
│   │   ├── embeddings/
│   │   ├── llm/
│   │   ├── vector_store/
│   │   └── document_extractors/
│   ├── workers/
│   ├── prompts/
│   └── utils/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── tests/
│
├── alembic/
│   └── versions/
│
├── docs/
│   ├── API.md
│   ├── TECHNOLOGY_DECISIONS.md
│   └── screenshots/
│
├── sample_data/
│
├── .github/
│   ├── workflows/
│   ├── ISSUE_TEMPLATE/
│   └── pull_request_template.md
│
├── .env.example
├── .gitignore
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── LICENSE
├── SECURITY.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
└── README.md
```

---

# 🧪 ENGINEERING PHILOSOPHY

```text
┌─────────────────────────────────────────────────────┐
│                 DOCUMIND PRINCIPLES                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│   PRIVACY       → Keep data local                   │
│   MODULARITY    → Abstract AI providers             │
│   SECURITY      → Isolate user data                 │
│   TRACEABILITY  → Ground answers in sources         │
│   TESTABILITY   → Verify critical behavior          │
│   EXTENSIBILITY → Prepare for future providers      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

# 🧠 AI ENGINE // SYSTEM STATUS

```text
> INITIALIZING DOCUMIND CORE...

[██████████████████████████████] 100%

> LOADING DOCUMENT ENGINE .......... OK
> LOADING EMBEDDING ENGINE ......... OK
> CONNECTING VECTOR MEMORY ......... OK
> CONNECTING LOCAL LLM ............. OK
> VERIFYING USER ISOLATION ......... OK
> VERIFYING API .................... OK
> VERIFYING FRONTEND ............... OK
> RUNNING TEST MATRIX .............. OK

╔══════════════════════════════════════════════╗
║                                              ║
║           ARTIFICIAL INTELLIGENCE            ║
║                  ONLINE                      ║
║                                              ║
║       DOCUMENTS → KNOWLEDGE → ANSWERS        ║
║                                              ║
║               SYSTEM READY                   ║
║                                              ║
╚══════════════════════════════════════════════╝
```

### `THE AI DOESN'T NEED YOUR DOCUMENTS TO LEAVE YOUR MACHINE.`

**Local intelligence. Private knowledge. Grounded answers.**

---

# ⚠️ CURRENT LIMITATIONS

DocuMind is powerful, but it is not magic.

Current limitations include:

* Scanned/image-only PDFs do not currently have OCR enabled.
* Chunking is currently character-based rather than fully token-aware.
* Background processing is primarily designed for local/single-node deployments.
* Local LLM performance depends heavily on CPU, GPU and RAM.
* Larger models can require significant system resources.
* Streaming behavior depends on the selected LLM provider implementation.

---

# 🛣️ ROADMAP // NEXT EVOLUTION

```text
                    CURRENT
                       │
        ┌──────────────┼──────────────┐
        │              │              │
    LOCAL RAG    SEMANTIC SEARCH   LOCAL LLM
        │              │              │
        └──────────────┼──────────────┘
                       ▼
                      NEXT
                       │
        ┌──────────────┼──────────────┐
        │              │              │
       OCR       HYBRID RETRIEVAL   RERANKING
        │              │              │
        ├──────────────┼──────────────┤
        │              │              │
    STREAMING    MULTI-DOCUMENT   TOKEN CHUNKING
        │           REASONING          │
        └──────────────┼──────────────┘
                       ▼
                  PRODUCTION
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   DISTRIBUTED     OBSERVABILITY   KUBERNETES
    WORKERS                           │
        │                             │
        └──────────────┬──────────────┘
                       ▼
                 S3 COMPATIBILITY
```

Planned areas include:

* OCR pipeline
* Token-aware chunking
* Hybrid keyword + vector retrieval
* Reranking models
* Streaming LLM responses
* Multi-document reasoning
* Advanced document previews
* Additional embedding providers
* Additional local LLM providers
* Distributed workers
* Production observability
* Kubernetes deployment
* S3-compatible object storage
* Role-based access control

---

# 📸 COMPLETE SCREENSHOT INDEX

|  #  | Module                     | Screenshot                            |
| :-: | -------------------------- | ------------------------------------- |
|  01 | Splash Screen              | `Screenshots/Splash.png`              |
|  02 | Login / Authentication     | `Screenshots/Login Account.png`       |
|  03 | Registration               | `Screenshots/Register Account.png`    |
|  04 | Dashboard                  | `Screenshots/Dashboard.png`           |
|  05 | AI Powered Chat            | `Screenshots/AI Powered Chats.png`    |
|  06 | Chat History               | `Screenshots/Chat History.png`        |
|  07 | Analytics                  | `Screenshots/Analytics.png`           |
|  08 | API Documentation          | `Screenshots/API Documentation.png`   |
|  09 | Extended API Documentation | `Screenshots/API Documentation 2.png` |
|  10 | API Interface              | `Screenshots/API.png`                 |

---

# 🤝 CONTRIBUTING

Contributions are welcome.

Before submitting a pull request:

```bash
ruff check .
ruff format --check .
pytest
```

Please review:

```text
CONTRIBUTING.md
```

before contributing.

---

# 🔒 SECURITY

If you discover a security vulnerability, please follow the responsible disclosure process in:

```text
SECURITY.md
```

Please avoid immediately opening a public issue for sensitive vulnerabilities.

---

# 📜 LICENSE

DocuMind AI is released under the **MIT License**.

See:

```text
LICENSE
```

for the complete license text.

---

# ⭐ WHY DOCUMIND AI?

DocuMind demonstrates practical production-oriented engineering across:

```text
Python Backend
      +
FastAPI
      +
REST APIs
      +
Authentication
      +
Database Engineering
      +
Document Processing
      +
Vector Databases
      +
Embeddings
      +
RAG
      +
Local LLMs
      +
React + TypeScript
      +
Docker
      +
Testing
      +
CI/CD
      +
Security
      +
AI Provider Abstraction
```

It is designed to be:

**Understandable · Modular · Secure · Extensible · Local-First**

---

<div align="center">

# 🧠 DOCUMIND AI

### `DOCUMENTS → KNOWLEDGE → ANSWERS`

**Understand your documents. Ask better questions. Keep your data local.**

<br>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:111827,50:0b1630,100:050816&height=150&section=footer&text=DOCUMIND%20AI&fontSize=38&fontColor=00E5FF&animation=twinkling&fontAlignY=65" width="100%" alt="DocuMind AI Footer"/>

<br>

### Built with 🧠 AI · ⚡ FastAPI · ⚛️ React · 🤖 Ollama · 🧬 ChromaDB

<br>

<a href="https://github.com/MUdevelops">
<img src="https://img.shields.io/badge/GitHub-MUdevelops-111827?style=for-the-badge&logo=github&logoColor=white" alt="MUdevelops GitHub"/>
</a>

<br><br>

**Build systems. Build intelligence. Build locally.**

⭐ **Star the repository if you find DocuMind useful.**

</div>
