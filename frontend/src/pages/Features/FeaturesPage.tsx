import { Link } from "react-router-dom";

export default function FeaturesPage() {
  return (
    <div className="marketing-page features-page">
      <main className="features-content">
        <section className="features-hero">
          <div>
            <h1>L'avenir de la présentation<br />professionnelle.</h1>
            <p>
              Concevez, optimisez et partagez des portfolios percutants sans écrire une seule ligne de
              code. Invenio associe un design minimaliste à une IA puissante pour propulser votre carrière.
            </p>
            <div className="feature-actions">
              <Link className="primary-btn" to="/register">Commencer maintenant</Link>
              <button className="secondary-btn" type="button">Voir la démo</button>
            </div>
          </div>
          <div className="feature-hero-art">
            <div className="fake-browser">
              <div className="fake-browser-top"><i/><i/><i/></div>
              <div className="fake-lines"><b/><span/><span/><em/><em/></div>
            </div>
          </div>
        </section>

        <section className="feature-bento">
          <article className="feature-card">
            <div className="feature-icon purple">✦</div>
            <h2>Création Sans Code Intégrale</h2>
            <p>Assemblez visuellement vos expériences, compétences et projets via une interface glisser-déposer intuitive. Obtenez un rendu pixel-perfect instantanément.</p>
          </article>

          <article className="feature-card ai-card">
            <div className="feature-icon purple">✧</div>
            <h2>Optimisation par l'IA</h2>
            <p>Notre assistant IA analyse vos descriptions de postes et suggère des reformulations percutantes pour maximiser l'impact auprès des recruteurs.</p>
            <div className="ai-demo">
              <del>"J'ai géré une équipe de 5 personnes..."</del>
              <strong>"Direction d'une équipe transversale de 5 collaborateurs, augmentant la productivité de 20%..."</strong>
            </div>
          </article>

          <article className="feature-card stats-card">
            <div className="feature-icon purple">▥</div>
            <h2>Analyses Statistiques</h2>
            <p>Suivez les vues de votre portfolio, le temps passé par section et les téléchargements de CV pour affiner votre stratégie de recherche.</p>
            <div className="mini-chart"><span>12</span><span>28</span><span>45</span><span>89</span></div>
          </article>

          <article className="feature-card wide">
            <div className="feature-icon purple">▦</div>
            <h2>Gestion Avancée de Projets</h2>
            <p>Organisez vos réalisations par catégories, ajoutez des collaborateurs, des tags de compétences et liez des dépôts de code ou des maquettes externes.</p>
            <div className="feature-tags">
              <span>Catégorisation intelligente</span>
              <span>Intégration GitHub / Figma</span>
              <span>Études de cas structurées</span>
            </div>
          </article>
        </section>
      </main>
    </div>
  );
}
