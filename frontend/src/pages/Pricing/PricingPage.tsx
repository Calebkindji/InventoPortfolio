import { Link } from "react-router-dom";

const check = "https://www.figma.com/api/mcp/asset/c2d297fe-5d4c-4739-8937-8e86bbfb7701/3750d.svg";

const plans = [
  {
    name: "Étudiant",
    description: "L'essentiel pour démarrer votre carrière.",
    price: "Gratuit",
    features: ["Portfolio public basique", "Jusqu'à 3 projets", "Statistiques de base"],
    action: "Commencer",
  },
  {
    name: "Pro",
    description: "Des outils avancés pour vous démarquer.",
    price: "9$",
    suffix: "/mois",
    features: ["Projets illimités", "Nom de domaine personnalisé", "Analytique avancée", "Export PDF HD"],
    action: "Passer Pro",
    featured: true,
  },
  {
    name: "Établissement",
    description: "La solution complète pour les écoles.",
    price: "Sur mesure",
    features: ["Gestion des cohortes", "Marque blanche", "Support dédié", "API d'intégration"],
    action: "Contacter les ventes",
  },
];

export default function PricingPage() {
  return (
    <div className="marketing-page pricing-page">
      <main className="marketing-content">
        <header className="marketing-header">
          <h1>Choisissez votre plan</h1>
          <p>Débloquez le plein potentiel de votre portfolio avec nos offres pensées pour les<br className="desktop-only" /> étudiants, les professionnels et les établissements.</p>
        </header>

        <section className="pricing-grid">
          {plans.map((plan) => (
            <article className={`price-card ${plan.featured ? "featured" : ""}`} key={plan.name}>
              {plan.featured && <span className="popular">Populaire</span>}
              <h2>{plan.name}</h2>
              <p className="price-description">{plan.description}</p>
              <div className="price">
                {plan.price}{plan.suffix && <small>{plan.suffix}</small>}
              </div>
              <ul>
                {plan.features.map((feature) => (
                  <li key={feature}><img src={check} alt="" />{feature}</li>
                ))}
              </ul>
              <Link className={plan.featured ? "primary-btn" : "secondary-btn"} to={plan.featured ? "/register" : "/contact"}>
                {plan.action}
              </Link>
            </article>
          ))}
        </section>

        <section className="faq">
          <h2>Questions Fréquentes</h2>
          <div className="faq-list">
            <details><summary>Puis-je changer de plan plus tard ?</summary><p>Oui. Votre espace peut évoluer avec vos besoins.</p></details>
            <details><summary>Le plan étudiant est-il vraiment gratuit ?</summary><p>Oui, la formule étudiant affichée ici est gratuite.</p></details>
            <details><summary>Proposez-vous un essai gratuit pour le plan Pro ?</summary><p>Consultez les modalités affichées au moment de l'inscription.</p></details>
          </div>
        </section>
      </main>
    </div>
  );
}
