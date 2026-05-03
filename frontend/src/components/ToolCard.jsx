import { trackClick } from '../api.js'

const AVATAR_PALETTES = [
  ['#7c3aed', '#9f67fa'],
  ['#2563eb', '#4f86f7'],
  ['#059669', '#10b981'],
  ['#d97706', '#f59e0b'],
  ['#dc2626', '#ef4444'],
  ['#0891b2', '#06b6d4'],
  ['#be185d', '#ec4899'],
  ['#0d9488', '#14b8a6'],
]

const PRICE_STYLES = {
  free:       { bg: '#14532d22', color: '#4ade80', border: '#4ade8033' },
  freemium:   { bg: '#1e3a5f22', color: '#60a5fa', border: '#60a5fa33' },
  paid:       { bg: '#44220022', color: '#fb923c', border: '#fb923c33' },
  enterprise: { bg: '#2e1065aa', color: '#c084fc', border: '#c084fc33' },
}

function avatarPalette(name) {
  let hash = 0
  for (let i = 0; i < name.length; i++) hash = (hash * 31 + name.charCodeAt(i)) >>> 0
  return AVATAR_PALETTES[hash % AVATAR_PALETTES.length]
}

export default function ToolCard({ tool }) {
  const handleClick = () => {
    window.open(tool.url, '_blank', 'noopener,noreferrer')
    trackClick(tool.id)
  }

  const [from, to] = avatarPalette(tool.name)
  const priceStyle = PRICE_STYLES[tool.price_tier] || PRICE_STYLES.freemium

  return (
    <div className="tool-card" onClick={handleClick}>
      <div className="tool-card-top">
        <div
          className="tool-avatar"
          style={{ background: `linear-gradient(135deg, ${from}, ${to})` }}
        >
          {tool.name.charAt(0).toUpperCase()}
        </div>

        <div className="tool-meta">
          <div className="tool-name">{tool.name}</div>
          {tool.price_tier && (
            <span
              className="price-badge"
              style={{
                background: priceStyle.bg,
                color: priceStyle.color,
                border: `1px solid ${priceStyle.border}`,
              }}
            >
              {tool.price_tier}
            </span>
          )}
        </div>

        <span className="tool-link-icon">↗</span>
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
    </div>
  )
}
