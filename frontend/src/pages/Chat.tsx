import { FormEvent, useEffect, useState } from "react";
import Layout from "../components/Layout";
import { api } from "../api/client";

export default function Chat() {
  const [conversations, setConversations] = useState<any[]>([]);
  const [activeId, setActiveId] = useState<string | null>(null);
  const [messages, setMessages] = useState<any[]>([]);
  const [question, setQuestion] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function loadConversations() {
    api.listConversations().then(setConversations).catch((e) => setError(e.message));
  }

  useEffect(loadConversations, []);

  useEffect(() => {
    if (!activeId) {
      setMessages([]);
      return;
    }
    api.getConversation(activeId).then((c) => setMessages(c.messages));
  }, [activeId]);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (!question.trim()) return;
    setSending(true);
    setError(null);
    const q = question;
    setQuestion("");
    try {
      const res = await api.chat(q, activeId || undefined);
      setActiveId(res.conversation_id);
      setMessages((m) => [
        ...m,
        { id: `local-user-${Date.now()}`, role: "user", content: q, citations: [] },
        { id: res.message_id, role: "assistant", content: res.answer, citations: res.citations },
      ]);
      loadConversations();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSending(false);
    }
  }

  return (
    <Layout>
      <div style={{ display: "flex", gap: 20, height: "calc(100vh - 56px)" }}>
        <div className="panel" style={{ width: 220, padding: 12, overflowY: "auto" }}>
          <button className="btn-primary" style={{ width: "100%", marginBottom: 12 }} onClick={() => setActiveId(null)}>
            + New chat
          </button>
          {conversations.map((c) => (
            <div
              key={c.id}
              onClick={() => setActiveId(c.id)}
              style={{
                padding: "8px 10px",
                borderRadius: 8,
                cursor: "pointer",
                fontSize: 13,
                background: activeId === c.id ? "var(--bg-panel-2)" : "transparent",
                marginBottom: 4,
              }}
            >
              {c.title}
            </div>
          ))}
        </div>

        <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
          <div style={{ flex: 1, overflowY: "auto", display: "flex", flexDirection: "column", gap: 14, paddingBottom: 16 }}>
            {messages.length === 0 && (
              <p className="text-dim">Ask a question about your uploaded documents.</p>
            )}
            {messages.map((m) => (
              <div key={m.id} className="panel" style={{ padding: 14, alignSelf: m.role === "user" ? "flex-end" : "flex-start", maxWidth: "75%" }}>
                <div className="text-dim" style={{ fontSize: 11, marginBottom: 4 }}>{m.role === "user" ? "You" : "DocuMind"}</div>
                <div>{m.content}</div>
                {m.citations && m.citations.length > 0 && (
                  <div style={{ marginTop: 10, display: "flex", flexDirection: "column", gap: 6 }}>
                    {m.citations.map((c: any, i: number) => (
                      <div key={i} className="text-dim" style={{ fontSize: 12, borderLeft: "2px solid var(--accent)", paddingLeft: 8 }}>
                        {c.filename}{c.page_number ? ` · p.${c.page_number}` : ""} · score {c.score}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
          {error && <p style={{ color: "var(--danger)" }}>{error}</p>}
          <form onSubmit={onSubmit} style={{ display: "flex", gap: 10 }}>
            <input
              className="input"
              placeholder="Ask about your documents..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
            />
            <button className="btn-primary" disabled={sending}>{sending ? "..." : "Send"}</button>
          </form>
        </div>
      </div>
    </Layout>
  );
}
