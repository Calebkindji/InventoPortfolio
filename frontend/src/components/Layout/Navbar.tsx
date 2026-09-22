import { Link, useLocation } from "react-router-dom";

const logo = "https://www.figma.com/api/mcp/asset/b173154c-995f-460d-915d-366b48424ed7/20bae.png";

export default function Navbar() {
  const location = useLocation();
  const links = [
    { label: "Accueil", to: "/" },
    { label: "Fonctionnalités", to: "/features" },
    { label: "Tarifs", to: "/pricing" },
    { label: "Ressources", to: "/contact" },
  ];

  return (
    <header className="public-header">
      <Link to="/" className="brand" aria-label="Invento">
        <img src={logo} alt="Invento" />
      </Link>

      <nav className="public-nav">
        {links.map((item) => (
          <Link
            key={item.to}
            to={item.to}
            className={location.pathname === item.to ? "active" : ""}
          >
            {item.label}
          </Link>
        ))}
      </nav>

      <Link className="header-cta" to="/register">Essai gratuit</Link>
    </header>
  );
}
