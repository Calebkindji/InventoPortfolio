import { Link, useParams } from "react-router-dom";

const caleb = "https://www.figma.com/api/mcp/asset/b173154c-995f-460d-915d-366b48424ed7/f39c0.png";

export default function PublicPortfolioPage() {
  const { username } = useParams();
  const displayName = username
    ? username.split("-").map((w) => w.charAt(0).toUpperCase() + w.slice(1)).join(" ")
    : "Caleb Kindji";

  return (
    <div className="public-portfolio">
      <div className="portfolio-inner">
        <div className="portfolio-topbar">
          <Link to="/" className="portfolio-logo">Invento</Link>
          <Link to="/register" className="secondary-btn">Créer le mien</Link>
        </div>

        <section className="portfolio-hero">
          <div>
            <span className="availability">DISPONIBLE POUR DE NOUVEAUX PROJETS</span>
            <h1>Je conçois et développe des <span>produits numériques</span> mémorables.</h1>
            <p>Bonjour, je m'appelle {displayName}. Je combine design d'interface et ingénierie logicielle pour donner vie à des applications web performantes et centrées sur l'utilisateur.</p>
            <div className="portfolio-actions"><button className="primary-btn">Me contacter</button><button className="secondary-btn">Voir le CV</button></div>
          </div>
          <div className="portfolio-avatar-wrap"><img src={caleb} alt={displayName} /></div>
        </section>

        <section className="portfolio-section">
          <span className="eyebrow">EXPERTISE & STACK</span>
          <div className="portfolio-chips">{["React / Next.js","TypeScript","Node.js","Django REST","PostgreSQL","Tailwind CSS","UI/UX Architecture","Figma Specialist"].map(x=><span key={x}>{x}</span>)}</div>
        </section>

        <section className="portfolio-section">
          <span className="eyebrow">PORTFOLIO</span>
          <h2>Sélection de réalisations</h2>
          <div className="work-grid">
            <article><div className="work-preview">Aperçu de l'interface logicielle</div><div className="work-copy"><h3>Plateforme SaaS Financière</h3><p>Une solution complète de facturation automatisée et de gestion de trésorerie.</p></div></article>
            <article><div className="work-preview">Aperçu du design mobile</div><div className="work-copy"><h3>Application de Productivité</h3><p>Application mobile et web pour la gestion intelligente des tâches d'équipe.</p></div></article>
          </div>
        </section>
      </div>
    </div>
  );
}
