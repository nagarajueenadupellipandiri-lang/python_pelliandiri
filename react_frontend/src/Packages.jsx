
import Navbar from './Navbar';
import './Packages.css';
import Footer from './Footer';

const packages = [
  {
    name: 'Silver',
    price: '₹1,999',
    duration: '3 Months',
    description: 'Start your journey to find a life partner.',
    features: [
      'Create your matrimonial profile',
      'Browse member profiles',
      'View limited contact details',
      'Basic customer support',
    ],
    className: 'silver',
  },
  {
    name: 'Gold',
    price: '₹4,999',
    duration: '6 Months',
    description: 'More opportunities to find your perfect match.',
    features: [
      'All Silver package features',
      'View contact details',
      'Send interest to profiles',
      'Priority profile visibility',
      'Priority customer support',
    ],
    className: 'gold',
    popular: true,
  },
  {
    name: 'Platinum',
    price: '₹9,999',
    duration: '12 Months',
    description: 'A premium experience for your marriage search.',
    features: [
      'All Gold package features',
      'Unlimited profile browsing',
      'Premium profile visibility',
      'Dedicated relationship assistance',
      'Premium customer support',
    ],
    className: 'platinum',
  },
];

function Packages() {
  return (
    <div className="packages-page">
      <Navbar />

      <section className="packages-hero">
        <p className="packages-eyebrow">YOUR JOURNEY STARTS HERE</p>
        <h1>Choose Your Perfect Package</h1>
        <p> Find the right plan for your journey towards a happy marriage. Discover meaningful connections with PelliPandiri. </p>
      </section>
      <section className="packages-section">
        <div className="packages-heading">
          <h2>Membership Plans</h2>
          <p>Choose a plan that works best for you.</p>
        </div>
        <div className="packages-grid">
          {packages.map((pkg) => (
            <article className={`package-card ${pkg.className}`} key={pkg.name} >
              {pkg.popular && (
                <span className="popular-badge">Most Popular</span>
              )}
              <h3>{pkg.name}</h3>
              <p className="package-description">{pkg.description}</p>
              <div className="package-price"> {pkg.price} <span> / {pkg.duration}</span> </div>
              <ul>
                {pkg.features.map((feature) => (
                  <li key={feature}> <span className="check-icon">✓</span> {feature} </li>
                ))}
              </ul>
              <a href="/createUser/" className={`package-button ${pkg.className}-button`} > Get Started → </a>
            </article>
          ))}
        </div>
        <p className="packages-note"> Please confirm package prices, validity and benefits with PelliPandiri before publishing these plans. </p>
      </section>
      
      <Footer />
    </div>
  );
}

export default Packages;
