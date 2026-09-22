import { Link } from "react-router-dom";

const logo = "https://www.figma.com/api/mcp/asset/b173154c-995f-460d-915d-366b48424ed7/20bae.png";

export default function Footer() {
  return (
    <footer className="public-footer">
      <div className="public-footer-inner">
        <Link to="/" className="footer-brand">
          <img src={logo} alt="" />
        </Link>
        <div className="footer-copy">
          <strong>© 2026 Invento Portfolio. Tous droits réservés.</strong>
          <span>Soutenu par Onyx Innovation</span>
        </div>
        <nav className="footer-nav">
          <Link to="/privacy">Confidentialité</Link>
          <Link to="/terms">Conditions</Link>
          <Link to="/contact">Contact</Link>
          <Link to="/contact">Aide</Link>
        </nav>
      </div>
    </footer>
  );
}
