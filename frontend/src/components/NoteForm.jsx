import { useMemo, useState } from 'react'

export default function NoteForm({ notes, onCreate }) {
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [tags, setTags] = useState('')
  const [selectedIds, setSelectedIds] = useState([])

  const canSubmit = useMemo(() => title.trim().length > 0, [title])

  const toggleId = (id) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    )
  }

  const submit = (e) => {
    e.preventDefault()
    if (!canSubmit) return
    const tagList = tags.split(',').map(t => t.trim()).filter(Boolean)
    onCreate({ title, content, link_ids: selectedIds, tags: tagList })
    setTitle('')
    setContent('')
    setTags('')
    setSelectedIds([])
  }

  return (
    <form onSubmit={submit} className="tech-card space-y-6">
      <div className="flex items-center gap-3">
        <svg className="w-5 h-5 text-blue-400" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 5V19M5 12H19" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
        <h2 className="section-title">Create Note</h2>
      </div>
      <input
        className="w-full tech-input"
        placeholder="Enter note title..."
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <div className="space-y-6">
        <div className="space-y-2">
          <label className="block text-sm font-medium text-blue-300">Content</label>
          <textarea
            className="w-full tech-input min-h-[120px]"
            placeholder="Write your note content here... (Markdown supported)"
            rows={4}
            value={content}
            onChange={(e) => setContent(e.target.value)}
          />
        </div>
        
        <div className="space-y-2">
          <label className="block text-sm font-medium text-blue-300">Tags</label>
          <input
            className="w-full tech-input"
            placeholder="Add tags separated by commas (e.g., work, ideas, todo)"
            value={tags}
            onChange={(e) => setTags(e.target.value)}
          />
        </div>

        <div className="space-y-3">
          <label className="block text-sm font-medium text-blue-300">Link to existing notes</label>
          <div className="flex flex-wrap gap-2">
            {notes.map((n) => (
              <button
                type="button"
                key={n.id}
                onClick={() => toggleId(n.id)}
                className={`px-3 py-1.5 rounded-lg text-sm transition-all duration-200 ${
                  selectedIds.includes(n.id)
                    ? 'bg-blue-500 text-white shadow-lg shadow-blue-500/25'
                    : 'bg-white/5 hover:bg-blue-500/10 text-gray-300'
                }`}
              >
                {n.title}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="pt-2">
        <button
          className="tech-button group"
          disabled={!canSubmit}
        >
          <svg className="w-5 h-5 transition-transform group-hover:scale-110" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 5V19M5 12H19" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          <span>Create Note</span>
        </button>
      </div>
    </form>
  )
}




