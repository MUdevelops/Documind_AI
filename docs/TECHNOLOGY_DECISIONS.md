# Technology Decisions

| Area | Choice | Why | Free/OSS | Tradeoffs |
|---|---|---|---|---|
| API framework | FastAPI | async-native, Pydantic v2 validation, auto OpenAPI | Yes | — |
| DB (dev) | SQLite | zero-setup local dev | Yes | limited concurrency |
| DB (prod) | PostgreSQL | production concurrency, JSON/indexing | Yes | needs a running server |
| Migrations | Alembic | standard SQLAlchemy migration tool | Yes | — |
| Auth | JWT (PyJWT) + bcrypt (Passlib) | stateless, simple to scale horizontally | Yes | logout is client-side unless a blocklist is added |
| PDF extraction | PyMuPDF | fast, accurate text+page extraction, active maintenance | Yes | no OCR for scanned PDFs |
| DOCX extraction | python-docx | standard, reliable paragraph extraction | Yes | tables/text boxes not fully covered |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) | strong quality/speed tradeoff, runs on CPU, no API key | Yes | first run downloads ~90MB of weights |
| Vector store | ChromaDB (persistent, local) | simple embedded local vector DB, no separate service required | Yes | not built for massive multi-tenant scale |
| LLM | Ollama (`llama3.1` default) | fully local inference, swappable models, no API key | Yes | requires a capable local machine (RAM/CPU/GPU) |
| Frontend | React + TypeScript + Vite | fast dev loop, typed, industry-standard SPA stack | Yes | — |

## Provider abstractions

`LLMProvider`, `EmbeddingProvider`, and `VectorStore` are abstract base
classes (`app/providers/*/base.py`). The default implementations are fully
local/free. A paid provider (OpenAI, Anthropic, Pinecone, etc.) could be
added as an additional implementation behind the same interface without
touching route or service code — but none is wired in by default, and the
app runs with zero paid APIs out of the box.

## Local alternatives considered

- **Embeddings**: `text-embedding-3-small` (OpenAI, paid) was rejected in
  favor of a local model to satisfy the zero-paid-API requirement.
- **Vector store**: Pinecone/Weaviate Cloud (paid/hosted) rejected in favor
  of ChromaDB's local persistent mode.
- **LLM**: any hosted API rejected in favor of Ollama, which runs entirely
  on the user's machine.

## Known validation gap

This repository's code was authored in a sandboxed environment without
outbound network access. Package installation, `pytest`, `ruff`, Alembic
migration execution, `uvicorn` startup, the frontend build, and Docker
builds were **not executed** by the generator. Run the commands in
`README.md` locally to validate; the code follows each library's current
stable API as of early 2026 training knowledge, but pin/version drift
should be checked with `pip install -e ".[dev]"` and `pytest` before
relying on it in production.
