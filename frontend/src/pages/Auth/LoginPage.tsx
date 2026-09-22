import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

const visual = "https://www.figma.com/api/mcp/asset/e0235058-6fdb-4401-b5cb-a0d172db797c/8a83b.png";
const emailIcon = "https://www.figma.com/api/mcp/asset/e0235058-6fdb-4401-b5cb-a0d172db797c/72a1d.svg";
const passwordIcon = "https://www.figma.com/api/mcp/asset/e0235058-6fdb-4401-b5cb-a0d172db797c/611a8.svg";
const googleIcon = "https://www.figma.com/api/mcp/asset/e0235058-6fdb-4401-b5cb-a0d172db797c/e2f41.svg";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const submit = (event: FormEvent) => {
    event.preventDefault();
    navigate("/dashboard");
  };

  return (
    <div className="auth-login">
      <section className="auth-brand-side">
        <div className="auth-art"><img src={visual} alt="" /></div>
        <div className="auth-art-overlay" />
        <div className="auth-brand-copy">
          <div className="auth-wordmark">Invento</div>
          <h1>Votre portfolio,<br />redéfini.</h1>
          <p>
            Accédez à votre espace premium pour gérer, analyser et présenter vos actifs
            professionnels avec une clarté et une précision inégalées.
          </p>
        </div>
      </section>

      <section className="auth-form-side">
        <div className="auth-card login-card">
          <div className="auth-card-heading">
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <h2>Connexion</h2>
              <Link to="/" title="Retour à l'accueil" style={{ fontSize: "24px", color: "var(--body)", textDecoration: "none", lineHeight: 1 }}>⌂</Link>
            </div>
            <p>Entrez vos identifiants pour accéder à votre espace.</p>
          </div>

          <form onSubmit={submit} className="auth-form">
            <label>
              <span>ADRESSE EMAIL</span>
              <div className="input-with-icon">
                <img src={emailIcon} alt="" />
                <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="calebkindji61@gmail.com" type="email" required />
              </div>
            </label>

            <label>
              <div className="label-line">
                <span>MOT DE PASSE</span>
                <a href="#forgot">Mot de passe oublié ?</a>
              </div>
              <div className="input-with-icon">
                <img src={passwordIcon} alt="" />
                <input value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" type="password" required />
              </div>
            </label>

            <button className="primary-btn auth-submit" type="submit">Se connecter</button>
          </form>

          <div className="or-divider"><span>OU CONTINUER AVEC</span></div>

          <button className="google-btn" type="button">
            <img src={googleIcon} alt="" /> Google
          </button>

          <p className="auth-bottom">
            Vous n'avez pas de compte ? <Link to="/register">Demander un accès</Link>
          </p>
        </div>
      </section>
    </div>
  );
}
