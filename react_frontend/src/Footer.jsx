
import { Link, useLocation } from 'react-router-dom';

function Footer() {
  const location = useLocation();

  const isActive = (path) =>
    location.pathname === path ? 'active' : '';

  return (
    <footer className="footer" id="contact">
        <a href="#home" className="footer-brand"> ♥ PelliPandiri <small>Together for a Better Tomorrow</small> </a>
        <p>© 2026 PelliPandiri. All rights reserved.</p>
        <div className="footer-links">
          <a href="#about">About</a>
          <a href="#features">Features</a>
          <a href="/login/">Login</a>
        </div>
      </footer>
  );
}

export default Footer;
