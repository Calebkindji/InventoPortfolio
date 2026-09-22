import { useState } from "react";
import { Link } from "react-router-dom";

const hero = "https://www.figma.com/api/mcp/asset/b173154c-995f-460d-915d-366b48424ed7/5d0cf.png";
const caleb = "https://www.figma.com/api/mcp/asset/b173154c-995f-460d-915d-366b48424ed7/f39c0.png";
const divine = "https://www.figma.com/api/mcp/asset/b173154c-995f-460d-915d-366b48424ed7/71503.png";
const jiresse = "https://www.figma.com/api/mcp/asset/b173154c-995f-460d-915d-366b48424ed7/c4b3e.png";

const profiles = [
  {
    name: "Caleb Kindji",
    role: "Product Designer Senior (Front-end & Maquette)",
    description: "Étudiant à l'Université Don Bosco.",
    image: caleb,
    tags: ["Figma", "Maquette", "Front-end"],
    to: "/u/caleb-kindji",
  },
  {
    name: "Divine",
    role: "Frontend Developer",
    description: "Étudiante à l'Université Don Bosco.",
    image: divine,
    tags: ["React", "Frontend", "Web"],
    to: "/u/divine",
  },
  {
    name: "Jiresse",
    role: "Développeur Full-Stack (Frontend & Backend)",
    description: "Étudiant à l'Université Don Bosco.",
    image: jiresse,
    tags: ["CSS", "Full-Stack", "Frontend"],
    to: "/u/jiresse",
  },
];

export default function LandingPage() {
  const [query, setQuery] = useState("");

  return (
    <div className="landing-page">
      <section className="landing-main">
        <div className="landing-hero">
          <div className="hero-copy">
            <h1>
              Créez votre portfolio professionnel.
              <span>Sans coder.</span>
            </h1>
            <p>
              Présentez vos compétences, expériences et projets avec une interface premium
              conçue pour les professionnels exigeants.
            </p>

            <form className="hero-search" onSubmit={(e) => e.preventDefault()}>
              <span className="search-glyph">⌕</span>
              <input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Rechercher un métier, une compétence, un profil..."
                aria-label="Rechercher"
              />
              <button type="submit">Explorer</button>
            </form>

            <div className="hero-visual">
              <img src={hero} alt="Aperçu abstrait d'un portfolio Invento" />
              <div className="hero-visual-gradient" />
            </div>
          </div>
        </div>

        <section className="team-preview">
          <div className="section-heading">
            <div>
              <h2>Notre Équipe</h2>
              <p>Découvrez les talents derrière le projet Invento.</p>
            </div>
            <Link to="/equipe">Voir tous les profils <span>↗</span></Link>
          </div>

          <div className="profile-grid">
            {profiles.map((profile) => (
              <Link to={profile.to} className="profile-card" key={profile.name}>
                <div className="profile-top">
                  <img className="profile-avatar" src={profile.image} alt={profile.name} />
                  <div className="profile-meta">
                    <h3>{profile.name}</h3>
                    <p><span className="tiny-icon">◫</span>{profile.role}</p>
                  </div>
                </div>
                <p className="profile-description">{profile.description}</p>
                <div className="tag-row">
                  {profile.tags.map((tag) => <span key={tag}>{tag}</span>)}
                </div>
                <div className="profile-hover">Voir le portfolio</div>
              </Link>
            ))}
          </div>
        </section>
      </section>
    </div>
  );
}
