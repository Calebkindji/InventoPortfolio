import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainLayout from "./components/Layout/MainLayout";
import LandingPage from "./pages/Landing/LandingPage";
import LoginPage from "./pages/Auth/LoginPage";
import RegisterPage from "./pages/Auth/RegisterPage";
import DashboardPage from "./pages/Dashboard/DashboardPage";
import PublicPortfolioPage from "./pages/Portfolio/PublicPortfolioPage";
import TeamPage from "./pages/Portfolio/TeamPage";
import FeaturesPage from "./pages/Features/FeaturesPage";
import PricingPage from "./pages/Pricing/PricingPage";
import ContactPage from "./pages/Contact/ContactPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<MainLayout />}>
          <Route path="/" element={<LandingPage />} />
          <Route path="/features" element={<FeaturesPage />} />
          <Route path="/pricing" element={<PricingPage />} />
          <Route path="/equipe" element={<TeamPage />} />
          <Route path="/u/:username" element={<PublicPortfolioPage />} />
          <Route path="/contact" element={<ContactPage />} />
        </Route>

        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="*" element={<div className="not-found">404 — Page non trouvée</div>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
