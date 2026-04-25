import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell
} from 'recharts'

const COLORS = ['#0ea5e9', '#38bdf8', '#7dd3fc', '#bae6fd', '#e0f2fe']

export default function AnalyticsDashboard({ data }) {
  if (!data || !data.length) return null

  return (
    <div className="analytics-dashboard">
      <h2>Trending Tools</h2>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data} margin={{ top: 8, right: 16, left: 0, bottom: 64 }}>
          <XAxis
            dataKey="tool_name"
            angle={-35}
            textAnchor="end"
            interval={0}
            tick={{ fontSize: 12, fill: '#94a3b8' }}
          />
          <YAxis tick={{ fontSize: 12, fill: '#94a3b8' }} />
          <Tooltip
            contentStyle={{ background: '#1e293b', border: '1px solid #334155', color: '#e2e8f0' }}
          />
          <Bar dataKey="click_count" radius={[4, 4, 0, 0]}>
            {data.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
