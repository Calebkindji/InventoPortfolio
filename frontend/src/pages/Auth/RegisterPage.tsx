import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

const visual = "https://www.figma.com/api/mcp/asset/e0235058-6fdb-4401-b5cb-a0d172db797c/8a83b.png";
const emailIcon = "https://www.figma.com/api/mcp/asset/e0235058-6fdb-4401-b5cb-a0d172db797c/72a1d.svg";
const passwordIcon = "https://www.figma.com/api/mcp/asset/e0235058-6fdb-4401-b5cb-a0d172db797c/611a8.svg";
const googleIcon = "https://www.figma.com/api/mcp/asset/e0235058-6fdb-4401-b5cb-a0d172db797c/e2f41.svg";

export default function RegisterPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const navigate = useNavigate();

  const submit = (event: FormEvent) => {
    event.preventDefault();
    if (password !== confirmPassword) {
      alert("Les mots de passe ne correspondent pas.");
      return;
    }
    navigate("/dashboard");
  };

  return (
    <div className="auth-login">
      <section className="auth-brand-side">
        <div className="auth-art"><img src={visual} alt="" /></div>
        <div className="auth-art-overlay" />
        <div className="auth-brand-copy">
          <div className="auth-wordmark">Invento</div>
          <h1>Rejoignez<br />l'excellence.</h1>
          <p>
            Créez votre espace premium pour gérer, analyser et présenter vos actifs
            professionnels avec une clarté et une précision inégalées.
          </p>
        </div>
      </section>

      <section className="auth-form-side">
        <div className="auth-card login-card">
          <div className="auth-card-heading">
            <h2>Créer un compte</h2>
            <p>Rejoignez Invento pour gérer votre portfolio premium.</p>
          </div>

          <form onSubmit={submit} className="auth-form">
            <label>
              <span>NOM COMPLET</span>
              <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Onyx Innovation" required />
            </label>

            <label>
              <span>ADRESSE EMAIL</span>
              <div className="input-with-icon">
                <img src={emailIcon} alt="" />
                <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="contact@onyxinnovation.net" type="email" required />
              </div>
            </label>

            <label>
              <span>MOT DE PASSE</span>
              <div className="input-with-icon">
                <img src={passwordIcon} alt="" />
                <input value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" type="password" required />
              </div>
            </label>

            <label>
              <span>CONFIRMER LE MOT DE PASSE</span>
              <div className="input-with-icon">
                <img src={passwordIcon} alt="" />
                <input value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} placeholder="••••••••" type="password" required />
              </div>
            </label>

            <button className="primary-btn auth-submit" type="submit">S'inscrire</button>
          </form>

          <div className="or-divider"><span>OU S'INSCRIRE AVEC</span></div>

          <button className="google-btn" type="button">
            <img src={googleIcon} alt="" /> Google
          </button>

          <p className="auth-bottom">
            Vous avez déjà un compte ? <Link to="/login">Se connecter</Link>
          </p>
        </div>
      </section>
    </div>
  );
}
