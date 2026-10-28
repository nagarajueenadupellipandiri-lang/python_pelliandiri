
import { Link, useLocation } from 'react-router-dom';

function Navbar() {
  const location = useLocation();

  const isActive = (path) =>
    location.pathname === path ? 'active' : '';

  return (
    <header className="navbar">
      <Link to="/" className="brand">
        <span className="brand-icon">♥</span>
        <span>
          <strong> Pelli<span>Pandiri</span> </strong>
          <small>Together for a Better Tomorrow</small>
        </span>
      </Link>

      <nav className="nav-links">
        <Link className={isActive('/')} to="/"> Home </Link>
        <Link to="/packages" className={isActive('/packages')}> Packages </Link>
        <Link className={isActive('/events')} to="/events"> Events </Link>
        <Link className={isActive('/about')} to="/about"> About Us </Link>
        <Link className={isActive('/branches')} to="/branches"> Branches </Link>
        <Link className={isActive('/success-stories')} to="/success-stories"> Success Stories </Link>
        <Link className={isActive('/blog')} to="/blog"> Blog </Link>
        <Link className={isActive('/contact')} to="/contact"> Contact Us </Link>
      </nav>

      <div className="nav-actions">
        <a href="/login/" className="login-btn"> Login </a>
        <a href="/createUser/" className="register-btn"> Register ↗ </a>
      </div>
    </header>
  );
}

export default Navbar;
