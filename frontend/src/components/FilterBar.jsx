const USE_CASES = [
  'content-writing', 'code-generation', 'image-generation',
  'data-analysis', 'customer-support', 'productivity', 'research',
  'audio-generation', 'video-generation', 'automation',
  'writing-assistance', 'design', 'marketing', 'sales', 'education',
]

const PRICE_TIERS = ['free', 'freemium', 'paid', 'enterprise']

export default function FilterBar({ filters, onChange }) {
  return (
    <div className="filter-bar">
      <input
        type="text"
        className="filter-search"
        placeholder="Search tools..."
        value={filters.search || ''}
        onChange={e => onChange({ ...filters, search: e.target.value })}
      />
      <select
        className="filter-select"
        value={filters.use_case || ''}
        onChange={e => onChange({ ...filters, use_case: e.target.value })}
      >
        <option value="">All use cases</option>
        {USE_CASES.map(uc => (
          <option key={uc} value={uc}>{uc}</option>
        ))}
      </select>
      <select
        className="filter-select"
        value={filters.price_tier || ''}
        onChange={e => onChange({ ...filters, price_tier: e.target.value })}
      >
        <option value="">All prices</option>
        {PRICE_TIERS.map(pt => (
          <option key={pt} value={pt}>{pt}</option>
        ))}
      </select>
      {(filters.use_case || filters.price_tier || filters.search) && (
        <button
          className="filter-clear"
          onClick={() => onChange({})}
        >
          Clear
        </button>
      )}
    </div>
  )
}
