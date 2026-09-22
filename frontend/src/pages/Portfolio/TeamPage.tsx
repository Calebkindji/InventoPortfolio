import { Link } from "react-router-dom";

const portrait = "https://www.figma.com/api/mcp/asset/816ffbac-9f1e-43f0-877b-ac3e53372230/f09da.png";

export default function TeamPage() {
  return (
    <div className="team-page">
      <main className="team-main">
        <section className="team-hero">
          <div className="team-portrait"><img src={portrait} alt="Onyx Innovation" /></div>
          <div className="team-intro">
            <h1>Onyx_Innovation</h1>
            <p>Étudiants à l'Université Don Bosco, soutenus par Onyx Innovation.</p>
            <div className="social-pills"><a href="#linkedin">in</a><a href="#github">⌘</a></div>
          </div>
        </section>

        <section className="team-bento">
          <div className="team-left">
            <article className="team-info-card">
              <h2>À propos</h2>
              <p>
                Expertise reconnue dans la gestion de fonds multi-actifs. Approche analytique
                combinant modèles quantitatifs et analyse macroéconomique approfondie. Passionné
                par l'innovation financière et l'investissement durable (ESG).
              </p>
            </article>
            <article className="team-info-card">
              <h2>Compétences</h2>
              <div className="skill-cloud">
                {["Allocation d'actifs","Gestion des risques","Analyse Macro","Critères ESG","Modélisation Quant."].map(x => <span key={x}>{x}</span>)}
              </div>
            </article>
            <article className="team-info-card">
              <h2>Formations</h2>
              <div className="education">
                <div><strong>MBA Finance</strong><span>London Business School • 2008 - 2010</span></div>
                <div><strong>CFA Charterholder</strong><span>CFA Institute • 2012</span></div>
              </div>
            </article>
          </div>

          <div className="team-right">
            <article className="team-info-card experience">
              <h2>Expériences</h2>
              <div className="timeline">
                <div><strong>Senior Product & Investment</strong><span>Onyx Innovation • 2020 - aujourd'hui</span><p>Conception de produits numériques et pilotage de projets professionnels.</p></div>
                <div><strong>Product Designer</strong><span>2016 - 2020</span><p>Design d'interfaces et transformation de parcours complexes.</p></div>
              </div>
            </article>
            <article className="team-info-card">
              <div className="projects-heading"><h2>Projets</h2><Link to="/register">Voir tout ↗</Link></div>
              <div className="project-mini-grid">
                <div><b>Invento</b><span>Portfolio professionnel</span></div>
                <div><b>Clarity</b><span>Plateforme éducative</span></div>
              </div>
            </article>
          </div>
        </section>
      </main>
    </div>
  );
}
