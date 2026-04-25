const BASE = import.meta.env.VITE_API_URL || '/api'

export async function fetchTools({ use_case, price_tier, search } = {}) {
  const params = new URLSearchParams()
  if (use_case)   params.set('use_case', use_case)
  if (price_tier) params.set('price_tier', price_tier)
  if (search)     params.set('search', search)
  const r = await fetch(`${BASE}/tools?${params}`)
  if (!r.ok) throw new Error(await r.text())
  return r.json()
}

export async function trackClick(toolId) {
  await fetch(`${BASE}/tools/${toolId}/click`, { method: 'POST' })
}

export async function fetchAnalytics() {
  const r = await fetch(`${BASE}/analytics`)
  if (!r.ok) return []
  return r.json()
}
