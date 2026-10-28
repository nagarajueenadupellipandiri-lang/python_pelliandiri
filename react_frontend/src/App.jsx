import { Routes, Route } from 'react-router-dom';
import Navbar from './Navbar';
import Packages from './Packages';
import Footer from './Footer';
import './App.css';

const features = [
  {
    icon: '🛡️',
    title: 'Trusted & Safe',
    description: 'Your privacy and security are our top priority.',
    color: 'pink',
  },
  {
    icon: '✓',
    title: 'Verified Profiles',
    description: 'Real people, genuine connections.',
    color: 'blue',
  },
  {
    icon: '♡',
    title: 'Better Matches',
    description: 'Find someone who shares your values.',
    color: 'rose',
  },
  {
    icon: '★',
    title: 'Easy to Use',
    description: 'A simple and smooth registration process.',
    color: 'green',
  },
  {
    icon: '♧',
    title: '24/7 Support',
    description: 'We are always here to help you.',
    color: 'purple',
  },
];

// Existing Home Page — same file, no Home.jsx needed
function HomePage() {
  return (
    <div className="website">
      <Navbar />

      <main>
        {/* Hero Section */}
        <section className="hero" id="home">
          <div className="hero-content">
            <p className="eyebrow">
              <span></span> YOUR JOURNEY TO FOREVER <span></span>
            </p>

            <h1>
              Welcome to <span>PelliPandiri</span>
            </h1>

            <h2>Find your perfect life partner</h2>

            <p className="hero-description">
              Where traditions meet modern love. Join thousands of happy
              couples who found their perfect match on PelliPandiri.
            </p>

            <div className="hero-buttons">
              <a href="/createUser/" className="primary-btn">
                ♡ &nbsp; Free Registration <span>→</span>
              </a>

              <a href="/login/" className="secondary-btn">
                ♙ &nbsp; Login <span>→</span>
              </a>
            </div>

            <div className="trust-points">
              <span>🛡️ Safe &amp; Secure</span>
              <span>👥 Verified Profiles</span>
              <span>♡ Better Matches</span>
              <span>♧ 24/7 Support</span>
            </div>
          </div>

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

        {/* Features Section */}
        <section className="features-section" id="features">
          <div className="section-heading">
            <p>MADE FOR YOUR HAPPILY EVER AFTER</p>
            <span className="tiny-heart">♥</span>
            <h2>Why Choose PelliPandiri?</h2>
            <p className="section-subtitle">
              Because your happiness matters to us
            </p>
          </div>

          <div className="features-grid">
            {features.map((feature) => (
              <article
                className={`feature-card ${feature.color}`}
                key={feature.title}
              >
                <div className="feature-icon">{feature.icon}</div>
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
              </article>
            ))}
          </div>
        </section>

        {/* About Section */}
        <section className="about-section" id="about">
          <div>
            <p className="eyebrow">YOUR STORY STARTS HERE</p>
            <h2>Every great love story begins with a connection.</h2>
          </div>

          <p>
            PelliPandiri helps you take the first step towards a meaningful
            relationship. Create your profile and begin your journey today.
          </p>

          <a href="/createUser/" className="primary-btn">
            Create Your Profile →
          </a>
        </section>

        {/* How It Works Section */}
        <section className="how-section" id="how-it-works">
          <div className="section-heading">
            <p>THREE SIMPLE STEPS</p>
            <h2>Your Journey to Forever</h2>
          </div>

          <div className="steps-grid">
            <article>
              <span>01</span>
              <h3>Create Your Profile</h3>
              <p>Share your details and preferences.</p>
            </article>

            <article>
              <span>02</span>
              <h3>Discover Matches</h3>
              <p>Explore profiles that suit you.</p>
            </article>

            <article>
              <span>03</span>
              <h3>Start Your Story</h3>
              <p>Take the next step towards a relationship.</p>
            </article>
          </div>
        </section>

        {/* Call To Action Section */}
        <section className="cta-section" id="success">
          <p>YOUR FOREVER PERSON MAY BE CLOSER THAN YOU THINK</p>
          <h2>Ready to find your perfect match?</h2>

          <a href="/createUser/" className="light-btn">
            Join PelliPandiri Today →
          </a>
        </section>
      </main>
      <Footer />
    </div>
  );
}

// Routing
function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/packages" element={<Packages />} />
    </Routes>
  );
}

export default App;