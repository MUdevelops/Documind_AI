import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    if (password.length < 8) {
      setError("Password must be at least 8 characters");
      return;
    }
    setLoading(true);
    try {
      await register(email, password, fullName);
      navigate("/dashboard");
    } catch (err: any) {
      setError(err.message || "Registration failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center" }}>
      <form onSubmit={onSubmit} className="panel" style={{ width: 380, padding: 32 }}>
        <h2 style={{ marginTop: 0 }}>Create your account</h2>
        {error && <p style={{ color: "var(--danger)", fontSize: 14 }}>{error}</p>}
        <label className="text-dim" style={{ fontSize: 13 }}>Full name</label>
        <input className="input" style={{ margin: "6px 0 16px" }} value={fullName}
          onChange={(e) => setFullName(e.target.value)} />
        <label className="text-dim" style={{ fontSize: 13 }}>Email</label>
        <input className="input" style={{ margin: "6px 0 16px" }} type="email" value={email}
          onChange={(e) => setEmail(e.target.value)} required />
        <label className="text-dim" style={{ fontSize: 13 }}>Password (min 8 characters)</label>
        <input className="input" style={{ margin: "6px 0 20px" }} type="password" value={password}
          onChange={(e) => setPassword(e.target.value)} required minLength={8} />
        <button className="btn-primary" style={{ width: "100%" }} disabled={loading}>
          {loading ? "Creating..." : "Create account"}
        </button>
        <p className="text-dim" style={{ fontSize: 13, marginTop: 16, textAlign: "center" }}>
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
      </form>
    </div>
  );
}
