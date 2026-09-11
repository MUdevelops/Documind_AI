import { useCallback, useEffect, useRef, useState } from "react";
import Layout from "../components/Layout";
import { api } from "../api/client";

export default function Documents() {
  const [docs, setDocs] = useState<any[]>([]);
  const [search, setSearch] = useState("");
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInput = useRef<HTMLInputElement>(null);

  const load = useCallback(() => {
    api
      .listDocuments(search ? { search } : {})
      .then((r) => setDocs(r.items))
      .catch((err) => setError(err.message));
  }, [search]);

  useEffect(() => {
    load();
    const interval = setInterval(load, 4000); // poll for processing status
    return () => clearInterval(interval);
  }, [load]);

  async function handleFiles(files: FileList | null) {
    if (!files || files.length === 0) return;
    setUploading(true);
    setError(null);
    try {
      for (const file of Array.from(files)) {
        await api.uploadDocument(file);
      }
      load();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  }

  async function handleDelete(id: string) {
    await api.deleteDocument(id);
    load();
  }

  return (
    <Layout>
      <h1>Documents</h1>

      <div
        className="panel"
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => {
          e.preventDefault();
          handleFiles(e.dataTransfer.files);
        }}
        onClick={() => fileInput.current?.click()}
        style={{ padding: 32, textAlign: "center", cursor: "pointer", border: "1px dashed var(--border)", marginBottom: 20 }}
      >
        <input
          ref={fileInput}
          type="file"
          multiple
          hidden
          accept=".pdf,.docx,.txt,.md"
          onChange={(e) => handleFiles(e.target.files)}
        />
        <p style={{ margin: 0 }}>{uploading ? "Uploading..." : "Drag & drop files here, or click to browse"}</p>
        <p className="text-dim" style={{ fontSize: 13 }}>PDF, DOCX, TXT, Markdown</p>
      </div>

      {error && <p style={{ color: "var(--danger)" }}>{error}</p>}

      <input
        className="input"
        placeholder="Search documents..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        style={{ marginBottom: 16, maxWidth: 320 }}
      />

      <div className="panel">
        {docs.length === 0 && <p className="text-dim" style={{ padding: 16 }}>No documents found.</p>}
        {docs.map((d) => (
          <div key={d.id} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "12px 16px", borderBottom: "1px solid var(--border)" }}>
            <div>
              <div>{d.original_filename}</div>
              <div className="text-dim" style={{ fontSize: 12 }}>
                {(d.size_bytes / 1024).toFixed(0)} KB · {d.chunk_count} chunks
                {d.error_message ? ` · ${d.error_message}` : ""}
              </div>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
              <span className={`badge badge-${d.status === "ready" ? "ready" : d.status === "failed" ? "failed" : "processing"}`}>
                {d.status}
              </span>
              <button className="btn-secondary" onClick={() => handleDelete(d.id)}>Delete</button>
            </div>
          </div>
        ))}
      </div>
    </Layout>
  );
}
