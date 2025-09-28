import { useMemo } from 'react'

// Minimal adjacency rendering; not an actual canvas/graph lib to keep dependencies light
export default function GraphView({ notes }) {
  const edges = useMemo(() => {
    const list = []
    for (const n of notes) {
      if (Array.isArray(n.links)) {
        for (const toId of n.links) list.push([n.id, toId])
      }
    }
    return list
  }, [notes])

  return (
    <div className="tech-card">
      <div className="flex items-center gap-3 mb-6">
        <svg className="w-5 h-5 text-blue-400" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M9 6v12m0-12a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm0 12a3 3 0 1 0 0 6 3 3 0 0 0 0-6Zm6-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M9 6c2.284 4.247 5.973 3.999 6 6.004-.027 2.005-3.716 1.757-6 6.004" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
        <h2 className="section-title">Graph View</h2>
      </div>
      
      {edges.length === 0 ? (
        <div className="text-center py-8">
          <div className="text-gray-400 mb-2">No connections yet</div>
          <div className="text-sm text-gray-500">Link notes together to visualize connections</div>
        </div>
      ) : (
        <ul className="space-y-2">
          {edges.map(([from, to], idx) => (
            <li key={idx} className="flex items-center gap-3 p-2 rounded-lg bg-white/5 hover:bg-blue-500/10 
              group transition-all duration-200 border border-transparent hover:border-blue-400/20">
              <span className="px-2 py-1 rounded bg-white/5 text-gray-300 text-sm">{from}</span>
              <svg className="w-4 h-4 text-blue-400 group-hover:scale-110 transition-transform" 
                viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M5 12h14m-7-7 7 7-7 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              <span className="px-2 py-1 rounded bg-white/5 text-gray-300 text-sm">{to}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}




