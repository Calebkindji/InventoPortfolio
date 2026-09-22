import { FormEvent, useState } from "react";
import { Link } from "react-router-dom";

export default function ContactPage() {
  const [message, setMessage] = useState("");
  const submit = (e: FormEvent) => { e.preventDefault(); setMessage("Votre demande a été préparée."); };

  return (
    <div className="marketing-page contact-page">
      <main className="contact-main">
        <section className="contact-heading">
          <h1>Contact et Aide</h1>
          <p>Besoin d'assistance ? Notre équipe de support et notre base de connaissances sont là pour vous aider à tirer le meilleur parti de votre portfolio Invenio.</p>
        </section>
        <section className="contact-grid">
          <article className="contact-form-card">
            <h2>✉ Envoyer un message</h2>
            <p>Nous vous répondrons dans les plus brefs délais (généralement sous 24h ouvrées).</p>
            <form onSubmit={submit}>
              <div className="two-inputs">
                <label>Nom complet<input defaultValue="Caleb kindji" /></label>
                <label>Adresse email<input defaultValue="calebkindji61@gmail.com" type="email" /></label>
              </div>
              <label>Sujet<select defaultValue=""><option value="">Sélectionnez un sujet...</option><option>Compte</option><option>Portfolio</option><option>Facturation</option></select></label>
              <label>Message<textarea placeholder="Décrivez votre besoin en détail..." value={message} onChange={(e)=>setMessage(e.target.value)} /></label>
              <button className="primary-btn" type="submit">Envoyer la demande</button>
            </form>
          </article>
          <div className="help-stack">
            <article className="help-card">
              <h2>Base de connaissances</h2>
              <Link to="/features"><b>Guide de démarrage</b><span>Configurez votre portfolio en 5 étapes.</span></Link>
              <Link to="/features"><b>Personnalisation du thème</b><span>Ajustez les couleurs et la typographie.</span></Link>
              <Link to="/features"><b>Domaines personnalisés</b><span>Liez votre propre nom de domaine.</span></Link>
              <Link to="/features" className="all-articles">Voir tous les articles</Link>
            </article>
            <article className="partner-card">
              <span>Partenariat Officiel</span><h2>Université Don Bosco</h2>
              <p>Étudiant ou Alumni de l'Université Don Bosco ? Vous bénéficiez d'un accès premium gratuit et d'un support prioritaire.</p>
              <Link className="primary-btn" to="/register">Activer mon avantage</Link>
            </article>
          </div>
        </section>
      </main>
      {message && <div className="contact-toast">{message}</div>}
    </div>
  );
}
