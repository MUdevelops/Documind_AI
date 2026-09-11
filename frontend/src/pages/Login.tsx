import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await login(email, password);
      navigate("/dashboard");
    } catch (err: any) {
      setError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center" }}>
      <form onSubmit={onSubmit} className="panel" style={{ width: 380, padding: 32 }}>
        <h2 style={{ marginTop: 0 }}>
          Sign in to <span style={{ color: "var(--accent)" }}>DocuMind</span>
        </h2>
        {error && <p style={{ color: "var(--danger)", fontSize: 14 }}>{error}</p>}
        <label className="text-dim" style={{ fontSize: 13 }}>Email</label>
        <input className="input" style={{ margin: "6px 0 16px" }} type="email" value={email}
          onChange={(e) => setEmail(e.target.value)} required />
        <label className="text-dim" style={{ fontSize: 13 }}>Password</label>
        <input className="input" style={{ margin: "6px 0 20px" }} type="password" value={password}
          onChange={(e) => setPassword(e.target.value)} required />
        <button className="btn-primary" style={{ width: "100%" }} disabled={loading}>
          {loading ? "Signing in..." : "Sign in"}
        </button>
        <p className="text-dim" style={{ fontSize: 13, marginTop: 16, textAlign: "center" }}>
          No account? <Link to="/register">Create one</Link>
        </p>
      </form>
    </div>
  );
}
