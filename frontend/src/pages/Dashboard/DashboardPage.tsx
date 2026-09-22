import { Link, useLocation } from "react-router-dom";

const icons = {
  eye: "https://www.figma.com/api/mcp/asset/fc01e26f-bd71-4393-926d-7a8087e54014/d2653.svg",
  projects: "https://www.figma.com/api/mcp/asset/fc01e26f-bd71-4393-926d-7a8087e54014/a3a9b.svg",
  completion: "https://www.figma.com/api/mcp/asset/fc01e26f-bd71-4393-926d-7a8087e54014/d14a7.svg",
  arrow: "https://www.figma.com/api/mcp/asset/fc01e26f-bd71-4393-926d-7a8087e54014/9bbb4.svg",
};

const nav = [
  ["Tableau de bord", "/dashboard"],
  ["Portefeuilles", "/u/caleb-kindji"],
  ["Analyses", "/dashboard#analytics"],
  ["Paramètres", "/dashboard#settings"],
  ["Aide", "/contact"],
];

function Sidebar() {
  const location = useLocation();
  return (
    <aside className="dash-sidebar">
      <Link to="/" className="dash-brand">
        <span className="dash-brand-mark">I</span>
        <span><b>Invento</b><small>Premium Portfolio</small></span>
      </Link>
      <nav className="dash-nav">
        {nav.map(([label,to]) => (
          <Link key={label} to={to} className={location.pathname === to ? "active" : ""}>
            <span className="nav-dot">•</span>{label}
          </Link>
        ))}
      </nav>
      <Link to="/register" className="publish-btn">＋ Publier le Portfolio</Link>
      <Link to="/contact" className="support-link">? <span>Support</span></Link>
      <Link to="/" className="logout-link">↪ <span>Déconnexion</span></Link>
    </aside>
  );
}

function Topbar() {
  return (
    <header className="dash-topbar">
      <div className="dash-search">⌕ <span>Rechercher...</span></div>
      <div className="dash-user-area">
        <button className="notification" aria-label="Notifications">♢<i/></button>
        <div className="dash-user">
          <span><b>caleb kindji</b><small>Pro</small></span>
          <div className="account-circle">CK</div>
        </div>
      </div>
    </header>
  );
}

function StatCard({ title, value, caption, icon, purple }: { title:string; value:string; caption:string; icon:string; purple?:boolean }) {
  return (
    <article className={`stat-card ${purple ? "purple-stat" : ""}`}>
      <div className="stat-top">
        <span className="stat-icon"><img src={icon} alt="" /></span>
        {!purple && <span className="stat-badge">0%</span>}
      </div>
      <div>
        <h3>{title}</h3>
        <strong>{value}</strong>
        <small>{caption}</small>
      </div>
      {purple && <div className="progress"><span/></div>}
    </article>
  );
}

export default function DashboardPage() {
  return (
    <div className="dashboard-shell">
      <Sidebar />
      <div className="dash-area">
        <Topbar />
        <main className="dashboard-main">
          <section className="welcome">
            <h1>Bonjour, caleb</h1>
            <p>Voici un aperçu de vos activités et de vos projets en cours pour aujourd'hui.</p>
          </section>
          <section className="stats-grid">
            <StatCard title="Vues du profil" value="0" caption="Les derniers jours" icon={icons.eye} />
            <StatCard title="Projets publiés" value="0" caption="Total à ce jour" icon={icons.projects} />
            <StatCard title="Score de complétion" value="0%" caption="Excellent" icon={icons.completion} purple />
          </section>

          <section className="recent-projects">
            <div className="dashboard-section-heading">
              <h2>Projets</h2><Link to="/register">Voir tout <img src={icons.arrow} alt="" /></Link>
            </div>
            <div className="empty-project">
              <span>＋</span>
              <h3>Ajouter votre premier projet</h3>
              <p>Commencez à construire votre portfolio en ajoutant un projet.</p>
            </div>
          </section>
        </main>
        <footer className="dash-footer">
          <span>© 2026 Invento Portfolio. Tous droits réservés.</span>
          <div><Link to="/privacy">Confidentialité</Link><Link to="/terms">Conditions</Link><Link to="/contact">Contact</Link></div>
        </footer>
      </div>
    </div>
  );
}
