const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

function getToken(): string | null {
  return localStorage.getItem("documind_access_token");
}

export function setToken(token: string | null) {
  if (token) localStorage.setItem("documind_access_token", token);
  else localStorage.removeItem("documind_access_token");
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = {
    ...(options.body && !(options.body instanceof FormData)
      ? { "Content-Type": "application/json" }
      : {}),
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };

  const res = await fetch(`${API_BASE_URL}${path}`, { ...options, headers });

  if (!res.ok) {
    let detail = `Request failed (${res.status})`;
    try {
      const body = await res.json();
      detail = body.detail || detail;
    } catch {
      /* ignore */
    }
    throw new Error(detail);
  }

  if (res.status === 204) return undefined as T;
  return res.json();
}

export const api = {
  register: (email: string, password: string, full_name: string) =>
    request("/auth/register", { method: "POST", body: JSON.stringify({ email, password, full_name }) }),

  login: (email: string, password: string) =>
    request<{ access_token: string; refresh_token: string }>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),

  me: () => request("/auth/me"),

  listDocuments: (params: { search?: string; status?: string } = {}) => {
    const qs = new URLSearchParams(params as Record<string, string>).toString();
    return request<{ items: any[]; total: number }>(`/documents${qs ? `?${qs}` : ""}`);
  },

  uploadDocument: (file: File) => {
    const form = new FormData();
    form.append("file", file);
    return request("/documents", { method: "POST", body: form });
  },

  getDocumentStatus: (id: string) => request<any>(`/documents/${id}/status`),

  deleteDocument: (id: string) => request<void>(`/documents/${id}`, { method: "DELETE" }),

  chat: (question: string, conversation_id?: string, document_id?: string) =>
    request<any>("/chat", {
      method: "POST",
      body: JSON.stringify({ question, conversation_id, document_id }),
    }),

  listConversations: () => request<any[]>("/conversations"),

  getConversation: (id: string) => request<any>(`/conversations/${id}`),

  deleteConversation: (id: string) => request<void>(`/conversations/${id}`, { method: "DELETE" }),

  search: (q: string) => request<any[]>(`/search?q=${encodeURIComponent(q)}`),

  analytics: () => request<any>("/analytics"),
};
