import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Layout({ children }: { children: React.ReactNode }) {
  const { logout, user } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <img src="/splash.png" alt="" style={{ objectFit: "cover", borderRadius: 6 }} />
          <span>Docu<span className="mind">Mind</span></span>
        </div>
        <NavLink to="/dashboard" className={({ isActive }) => (isActive ? "nav-item active" : "nav-item")}>Dashboard</NavLink>
        <NavLink to="/documents" className={({ isActive }) => (isActive ? "nav-item active" : "nav-item")}>Documents</NavLink>
        <NavLink to="/chat" className={({ isActive }) => (isActive ? "nav-item active" : "nav-item")}>Chat</NavLink>
        <NavLink to="/analytics" className={({ isActive }) => (isActive ? "nav-item active" : "nav-item")}>Analytics</NavLink>
        <div style={{ flex: 1 }} />
        <div className="text-dim" style={{ fontSize: 12, padding: "8px 12px" }}>{user?.email}</div>
        <button
          className="btn-secondary"
          onClick={() => {
            logout();
            navigate("/login");
          }}
        >
          Log out
        </button>
      </aside>
      <main className="main-content">{children}</main>
    </div>
  );
}
