import { trackClick } from '../api.js'

const PRICE_COLORS = {
  free:       '#22c55e',
  freemium:   '#3b82f6',
  paid:       '#f59e0b',
  enterprise: '#8b5cf6',
}

export default function ToolCard({ tool }) {
  const handleClick = async () => {
    await trackClick(tool.id)
    window.open(tool.url, '_blank', 'noopener,noreferrer')
  }

  return (
    <div className="tool-card" onClick={handleClick}>
      <div className="tool-card-header">
        <h3 className="tool-name">{tool.name}</h3>
        {tool.price_tier && (
          <span
            className="price-badge"
            style={{ backgroundColor: PRICE_COLORS[tool.price_tier] || '#64748b' }}
          >
            {tool.price_tier}
          </span>
        )}
      </div>
      {tool.signal_summary && (
        <p className="signal-summary">{tool.signal_summary}</p>
      )}
      {tool.use_cases?.length > 0 && (
        <div className="use-cases">
          {tool.use_cases.map(tag => (
            <span key={tag} className="tag">{tag}</span>
          ))}
        </div>
      )}
      {tool.target_audience && (
        <p className="target-audience">For: {tool.target_audience}</p>
      )}
      <div className="tool-card-footer">
        <span className="click-count">{tool.click_count} clicks</span>
      </div>
    </div>
  )
}
