import { useEffect, useState } from 'react'
import NoteForm from './components/NoteForm'
import NoteList from './components/NoteList'
import GraphView from './components/GraphView'
import ThemeSwitch from './components/ThemeSwitch'

const API_URL = 'http://127.0.0.1:8000'

export default function App() {
  const [notes, setNotes] = useState([])
  const [loading, setLoading] = useState(false)
  const [query, setQuery] = useState('')
  const [searching, setSearching] = useState(false)
  const [results, setResults] = useState([])

  const fetchNotes = async () => {
    setLoading(true)
    try {
      const res = await fetch(`${API_URL}/notes`)
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`)
      }
      const data = await res.json()
      setNotes(data)
    } catch (error) {
      console.error('Error fetching notes:', error)
      alert('Failed to fetch notes. Please try again later.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchNotes()
  }, [])

  const handleCreate = async (payload) => {
    try {
      const res = await fetch(`${API_URL}/notes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`)
      }
      await fetchNotes()
    } catch (error) {
      console.error('Error creating note:', error)
      alert('Failed to create note. Please try again.')
    }
  }

  const handleDelete = async (id) => {
    try {
      const res = await fetch(`${API_URL}/notes/${id}`, { method: 'DELETE' })
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`)
      }
      await fetchNotes()
    } catch (error) {
      console.error('Error deleting note:', error)
      alert('Failed to delete note. Please try again.')
    }
  }

  const runSearch = async () => {
    if (!query.trim()) {
      setResults([])
      return
    }
    setSearching(true)
    try {
      const res = await fetch(`${API_URL}/notes/search?q=` + encodeURIComponent(query.trim()))
      const data = await res.json()
      setResults(data)
    } finally {
      setSearching(false)
    }
  }

  return (
    <div className="min-h-screen px-4 py-8">
      <div className="max-w-6xl mx-auto space-y-8">
        <header className="glass-panel rounded-xl p-4 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div className="flex items-center gap-3">
            <svg className="w-8 h-8 text-blue-400" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M7.5 12H16.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M12 7.5L12 16.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-blue-300 bg-clip-text text-transparent">MindMesh</h1>
          </div>
          <div className="flex gap-2 w-full md:w-auto">
            <input
              className="flex-1 md:w-96 tech-input"
              placeholder="Semantic search notes..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter') runSearch() }}
            />
            <button
              className="tech-button text-sm"
              onClick={runSearch}
              disabled={searching}
            >
              {searching ? 'Searching...' : 'Search'}
            </button>
            <button
              className="tech-button-outline text-sm"
              onClick={() => { setQuery(''); setResults([]) }}
            >
              Clear
            </button>
            <button
              className="tech-button text-sm"
              onClick={fetchNotes}
            >
              <span className="flex items-center gap-1">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Refresh
              </span>
            </button>
          </div>
        </header>

        <NoteForm notes={notes} onCreate={handleCreate} />

        {results.length > 0 && (
          <div className="tech-card animate-fadeIn">
            <div className="flex items-center justify-between mb-3">
              <h2 className="font-semibold text-blue-400 flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                Search Results
              </h2>
              <div className="text-xs text-blue-400 px-2 py-1 rounded-full bg-blue-500/10 border border-blue-500/20">
                Top {results.length} matches
              </div>
            </div>
            <ul className="space-y-3">
              {results.map((n) => (
                <li key={n.id} className="tech-card hover:scale-[1.02] transition-all duration-200">
                  <div className="font-medium text-blue-300">{n.title}</div>
                  {n.content && (
                    <div className="mt-2 text-sm text-gray-400 whitespace-pre-line">{n.content}</div>
                  )}
                </li>
              ))}
            </ul>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <NoteList notes={notes} loading={loading} onDelete={handleDelete} />
          <GraphView notes={notes} />
        </div>
        <ThemeSwitch />
      </div>
    </div>
  )
}




