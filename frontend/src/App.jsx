import { useState, useEffect } from 'react'
import FilterBar from './components/FilterBar.jsx'
import ToolGrid from './components/ToolGrid.jsx'
import AnalyticsDashboard from './components/AnalyticsDashboard.jsx'
import { fetchTools, fetchAnalytics } from './api.js'

export default function App() {
  const [tools, setTools]         = useState([])
  const [analytics, setAnalytics] = useState([])
  const [filters, setFilters]     = useState({})
  const [loading, setLoading]     = useState(false)
  const [error, setError]         = useState(null)

  useEffect(() => {
    setLoading(true)
    setError(null)
    fetchTools(filters)
      .then(setTools)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [filters])

  useEffect(() => {
    fetchAnalytics().then(setAnalytics)
  }, [tools]) // refresh analytics when tools list changes

  return (
    <div className="app">
      <header className="app-header">
        <div className="app-header-inner">
          <div>
            <h1>AI Tool Directory</h1>
            <p className="app-subtitle">Powered by Research Agent + Claude</p>
          </div>
          <span className="tool-count">{tools.length} tools</span>
        </div>
      </header>

      <main className="app-main">
        <FilterBar filters={filters} onChange={setFilters} />

        {error && <div className="error-banner">Failed to load tools: {error}</div>}

        {loading
          ? <div className="loading">Loading...</div>
          : <ToolGrid tools={tools} />
        }

        <AnalyticsDashboard data={analytics} />
      </main>
    </div>
  )
}
