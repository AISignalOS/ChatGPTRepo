import ToolCard from './ToolCard.jsx'

export default function ToolGrid({ tools }) {
  if (!tools.length) {
    return (
      <div className="empty-state">
        <p>No tools found. Install the extension and browse some AI tool sites to get started!</p>
      </div>
    )
  }

  return (
    <div className="tool-grid">
      {tools.map(tool => (
        <ToolCard key={tool.id} tool={tool} />
      ))}
    </div>
  )
}
