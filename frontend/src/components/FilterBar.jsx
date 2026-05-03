const CATEGORIES = [
  'code-generation',
  'content-writing',
  'image-generation',
  'video-generation',
  'audio-generation',
  'research',
  'data-analysis',
  'productivity',
  'automation',
  'design',
  'marketing',
  'customer-support',
  'education',
  'writing-assistance',
  'sales',
]

const PRICE_TIERS = ['free', 'freemium', 'paid', 'enterprise']

export default function FilterBar({ filters, onChange }) {
  const setUseCase = (val) =>
    onChange({ ...filters, use_case: filters.use_case === val ? '' : val })

  const setPrice = (val) =>
    onChange({ ...filters, price_tier: filters.price_tier === val ? '' : val })

  return (
    <div className="filter-section">
      <div className="filter-row">
        <button
          className={`filter-pill ${!filters.use_case ? 'active' : ''}`}
          onClick={() => onChange({ ...filters, use_case: '' })}
        >
          All tools
        </button>

        {CATEGORIES.map(cat => (
          <button
            key={cat}
            className={`filter-pill ${filters.use_case === cat ? 'active' : ''}`}
            onClick={() => setUseCase(cat)}
          >
            {cat}
          </button>
        ))}

        <div className="filter-divider" />

        {PRICE_TIERS.map(pt => (
          <button
            key={pt}
            className={`filter-pill ${filters.price_tier === pt ? 'active' : ''}`}
            onClick={() => setPrice(pt)}
          >
            {pt}
          </button>
        ))}
      </div>
    </div>
  )
}
