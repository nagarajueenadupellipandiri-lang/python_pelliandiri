import { useState } from 'react'
import heroImg from './assets/hero.png'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import './App.css'

const features = [
  {
    icon: "🛡️",
    title: "Trusted & Safe",
    description: "Your privacy and security are our top priority.",
    color: "pink",
  },
  {
    icon: "✓",
    title: "Verified Profiles",
    description: "Real people, genuine connections.",
    color: "blue",
  },
  {
    icon: "♡",
    title: "Better Matches",
    description: "Find someone who shares your values.",
    color: "rose",
  },
  {
    icon: "★",
    title: "Easy to Use",
    description: "A simple and smooth registration process.",
    color: "green",
  },
  {
    icon: "♧",
    title: "24/7 Support",
    description: "We are always here to help you.",
    color: "purple",
  },
];

function App() {
  return (
    <div className="website">
      <header className="navbar">
        <a href="#home" className="brand">
          <span className="brand-icon">♥</span>
          <span>
            <strong>Pelli<span>Pandiri</span></strong>
            <small>Together for a Better Tomorrow</small>
          </span>
        </a>

        <nav className="nav-links">
          <a className="active" href="#home">Home</a>
          <a href="#packages">packages</a>
          <a href="#packages">Events</a>
          <a href="#about">About Us</a>
          <a href="#packages">Branches</a>
          <a href="#success">Success Stories</a>
          <a href="#packages">Blog</a>
          <a href="#contact">Contact Us</a>
        </nav>

        <div className="nav-actions">
          <a href="/login/" className="login-btn">Login</a>
          <a href="/createUser/" className="register-btn">Register ↗</a>
        </div>
      </header>

      <main>
        <section className="hero" id="home">
          <div className="hero-content">
            <p className="eyebrow"> <span></span> YOUR JOURNEY TO FOREVER <span></span> </p>
            <h1> Welcome to <span>PelliPandiri</span> </h1>
            <h2>Find your perfect life partner</h2>
            <p className="hero-description"> Where traditions meet modern love. Join thousands of happy couples who found their perfect match on PelliPandiri. </p>
            <div className="hero-buttons">
              <a href="/createUser/" className="primary-btn"> ♡ &nbsp; Free Registration <span>→</span> </a>
              <a href="/login/" className="secondary-btn"> ♙ &nbsp; Login <span>→</span> </a>
            </div>
            <div className="trust-points">
              <span>🛡️ Safe & Secure</span>
              <span>👥 Verified Profiles</span>
              <span>♡ Better Matches</span>
              <span>♧ 24/7 Support</span>
            </div>
          </div>

          {/* <div className="hero-note">
            <span>Real People</span>
            <span>Real Stories</span>
            <span>Lasting Bonds ♥</span>
          </div> */}

          <div className="happy-couples">
            <div className="avatar-stack">
              <span>👩🏻</span>
              <span>👨🏻</span>
              <span>👩🏽</span>
            </div>
            <div>
              <strong>1000+ Happy Couples ♥</strong>
              <small>Found their life partner</small>
            </div>
          </div>
        </section>

        <section className="features-section" id="features">
          <div className="section-heading">
            <p>MADE FOR YOUR HAPPILY EVER AFTER</p>
            <span className="tiny-heart">♥</span>
            <h2>Why Choose PelliPandiri?</h2>
            <p className="section-subtitle"> Because your happiness matters to us </p>
          </div>

          <div className="features-grid">
            {features.map((feature) => (
              <article className={`feature-card ${feature.color}`} key={feature.title} >
                <div className="feature-icon">{feature.icon}</div>
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="about-section" id="about">
          <div>
            <p className="eyebrow">YOUR STORY STARTS HERE</p>
            <h2>Every great love story begins with a connection.</h2>
          </div>
          <p> PelliPandiri helps you take the first step towards a meaningful relationship. Create your profile and begin your journey today. </p>
          <a href="/createUser/" className="primary-btn"> Create Your Profile → </a>
        </section>

        <section className="how-section" id="how-it-works">
          <div className="section-heading">
            <p>THREE SIMPLE STEPS</p>
            <h2>Your Journey to Forever</h2>
          </div>
          <div className="steps-grid">
            <article><span>01</span><h3>Create Your Profile</h3><p>Share your details and preferences.</p></article>
            <article><span>02</span><h3>Discover Matches</h3><p>Explore profiles that suit you.</p></article>
            <article><span>03</span><h3>Start Your Story</h3><p>Take the next step towards a relationship.</p></article>
          </div>
        </section>

        <section className="cta-section" id="success">
          <p>YOUR FOREVER PERSON MAY BE CLOSER THAN YOU THINK</p>
          <h2>Ready to find your perfect match?</h2>
          <a href="/createUser/" className="light-btn">Join PelliPandiri Today →</a>
        </section>
      </main>

      <footer className="footer" id="contact">
        <a href="#home" className="footer-brand"> ♥ PelliPandiri <small>Together for a Better Tomorrow</small> </a>
        <p>© 2026 PelliPandiri. All rights reserved.</p>
        <div className="footer-links">
          <a href="#about">About</a>
          <a href="#features">Features</a>
          <a href="/login/">Login</a>
        </div>
      </footer>
    </div>
  );
}

export default App

