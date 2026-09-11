import { useNavigate } from "react-router-dom";

export default function Splash() {
  const navigate = useNavigate();
  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        background: "radial-gradient(circle at 50% 30%, #0d1330 0%, #05070f 70%)",
        textAlign: "center",
        padding: 24,
      }}
    >
      <img src="/splash.png" alt="DocuMind" style={{ maxWidth: 560, width: "100%", borderRadius: 12 }} />
      <div style={{ display: "flex", gap: 14, marginTop: 32 }}>
        <button className="btn-primary" onClick={() => navigate("/register")}>
          Get started
        </button>
        <button className="btn-secondary" onClick={() => navigate("/login")}>
          Sign in
        </button>
      </div>
    </div>
  );
}
