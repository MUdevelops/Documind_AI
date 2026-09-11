import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import { api } from "../api/client";

export default function Analytics() {
  const [a, setA] = useState<any | null>(null);

  useEffect(() => {
    api.analytics().then(setA);
  }, []);

  if (!a) return <Layout><p className="text-dim">Loading...</p></Layout>;

  const rows: [string, string | number][] = [
    ["Total documents", a.document_count],
    ["Processed documents", a.processed_documents],
    ["Failed documents", a.failed_documents],
    ["Total chunks", a.total_chunks],
    ["Conversations", a.conversation_count],
    ["Messages", a.message_count],
    ["Storage used", `${(a.total_storage_bytes / 1024 / 1024).toFixed(2)} MB`],
  ];

  return (
    <Layout>
      <h1>Analytics</h1>
      <div className="panel">
        {rows.map(([label, value]) => (
          <div key={label} style={{ display: "flex", justifyContent: "space-between", padding: "14px 20px", borderBottom: "1px solid var(--border)" }}>
            <span className="text-dim">{label}</span>
            <span style={{ fontWeight: 600 }}>{value}</span>
          </div>
        ))}
      </div>
    </Layout>
  );
}
