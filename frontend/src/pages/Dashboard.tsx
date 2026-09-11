import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import { api } from "../api/client";

export default function Dashboard() {
  const [analytics, setAnalytics] = useState<any | null>(null);
  const [recentDocs, setRecentDocs] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([api.analytics(), api.listDocuments()])
      .then(([a, docs]) => {
        setAnalytics(a);
        setRecentDocs(docs.items.slice(0, 5));
      })
      .catch((err) => setError(err.message));
  }, []);

  const stats = analytics
    ? [
        { label: "Documents", value: analytics.document_count },
        { label: "Processed", value: analytics.processed_documents },
        { label: "Conversations", value: analytics.conversation_count },
        { label: "Storage", value: `${(analytics.total_storage_bytes / 1024 / 1024).toFixed(1)} MB` },
      ]
    : [];

  return (
    <Layout>
      <h1>Dashboard</h1>
      {error && <p style={{ color: "var(--danger)" }}>{error}</p>}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 16, margin: "24px 0" }}>
        {stats.map((s) => (
          <div key={s.label} className="panel" style={{ padding: 20 }}>
            <div className="text-dim" style={{ fontSize: 13 }}>{s.label}</div>
            <div style={{ fontSize: 28, fontWeight: 700, marginTop: 4 }}>{s.value}</div>
          </div>
        ))}
      </div>

      <h3>Recent documents</h3>
      <div className="panel" style={{ padding: 8 }}>
        {recentDocs.length === 0 && <p className="text-dim" style={{ padding: 16 }}>No documents yet.</p>}
        {recentDocs.map((d) => (
          <div key={d.id} style={{ display: "flex", justifyContent: "space-between", padding: "10px 16px", borderBottom: "1px solid var(--border)" }}>
            <span>{d.original_filename}</span>
            <span className={`badge badge-${d.status === "ready" ? "ready" : d.status === "failed" ? "failed" : "processing"}`}>
              {d.status}
            </span>
          </div>
        ))}
      </div>
    </Layout>
  );
}
