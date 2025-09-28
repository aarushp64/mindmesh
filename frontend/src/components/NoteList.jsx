import React from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

export default function NoteList({ notes, loading, onDelete }) {
  return (
    <div className="tech-card">
      <div className="flex items-center gap-3 mb-6">
        <svg className="w-5 h-5 text-blue-400" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M9 5H7C5.89543 5 5 5.89543 5 7V19C5 20.1046 5.89543 21 7 21H17C18.1046 21 19 20.1046 19 19V7C19 5.89543 18.1046 5 17 5H15M9 5C9 6.10457 9.89543 7 11 7H13C14.1046 7 15 6.10457 15 5M9 5C9 3.89543 9.89543 3 11 3H13C14.1046 3 15 3.89543 15 5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
        <h2 className="section-title">Notes</h2>
      </div>
      
      {loading ? (
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-400"></div>
        </div>
      ) : notes.length === 0 ? (
        <div className="text-center py-8">
          <div className="text-gray-400 mb-2">No notes yet</div>
          <div className="text-sm text-gray-500">Create your first note to get started</div>
        </div>
      ) : (
        <ul className="space-y-4">
          {notes.map((n) => (
            <li key={n.id} className="tech-card group">
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-3">
                    <h3 className="font-medium text-lg text-blue-300">{n.title}</h3>
                    {n.layer && (
                      <span className="tech-tag capitalize">
                        {n.layer}
                      </span>
                    )}
                  </div>
                  {n.content && (
                    <div className="prose prose-sm prose-invert max-w-none">
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {n.content}
                      </ReactMarkdown>
                    </div>
                  )}
                  <div className="flex items-center gap-3 mt-3 flex-wrap">
                    {n.tags?.length > 0 && (
                      <div className="flex flex-wrap gap-1.5">
                        {n.tags.map((tag) => (
                          <span key={tag} className="tech-tag">
                            #{tag}
                          </span>
                        ))}
                      </div>
                    )}
                    {n.links?.length > 0 && (
                      <div className="text-xs text-blue-400 flex gap-2 items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                        </svg>
                        {n.links.map((link, idx) => (
                          <span key={link} className="hover:text-blue-300 transition-colors">
                            {idx > 0 && ', '}
                            <a href={link} target="_blank" rel="noopener noreferrer">
                              {link}
                            </a>
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
                <button
                  className="text-red-400 hover:text-red-300 transition-colors text-sm flex-shrink-0"
                  onClick={() => onDelete(n.id)}
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
