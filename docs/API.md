# API Reference

Base URL: `/api/v1`. Full interactive schema at `/docs` (Swagger UI) when running.
Authenticated endpoints require `Authorization: Bearer <access_token>`.

## Auth
- `POST /auth/register` — `{email, password, full_name}` → 201 user
- `POST /auth/login` — `{email, password}` → `{access_token, refresh_token}`
- `POST /auth/logout` — requires auth
- `GET /auth/me` — current user

## Documents
- `POST /documents` — multipart upload (`file`) → document (processing starts in background)
- `GET /documents?page=&page_size=&search=&status=` — paginated list
- `GET /documents/{id}` — single document
- `GET /documents/{id}/status` — status/progress
- `DELETE /documents/{id}` — removes DB rows, vectors, and the stored file

## Chat / RAG
- `POST /chat` — `{question, conversation_id?, document_id?}` → answer + citations
- `GET /conversations` — list
- `GET /conversations/{id}` — with full message history
- `DELETE /conversations/{id}`

## Search
- `GET /search?q=&top_k=` — semantic search across the user's own documents

## Analytics
- `GET /analytics` — document/conversation/message counts, storage, chunk totals

## Health
- `GET /health` and `GET /api/v1/health` — component-level status (app, database, embedding model, LLM)

All list/detail/delete endpoints enforce `owner_id` scoping — a request for
another user's resource returns `404`, not `403`, to avoid confirming the
resource's existence to non-owners.
