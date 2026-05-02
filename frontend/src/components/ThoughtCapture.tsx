'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { PenTool, Heart, Target, Calendar, BookOpen, Send, Sparkles } from 'lucide-react'
import { useCaptureThought } from '@/lib/hooks/useThoughts'
import toast from 'react-hot-toast'

const thoughtTypes = [
  { id: 'thought', icon: PenTool, label: 'General Thought', color: 'neural', description: 'Ideas, reflections, observations' },
  { id: 'memory', icon: Heart, label: 'Memory', color: 'rose', description: 'Past experiences, recollections' },
  { id: 'goal', icon: Target, label: 'Goal', color: 'emerald', description: 'Aspirations, dreams, objectives' },
  { id: 'plan', icon: Calendar, label: 'Plan', color: 'blue', description: 'Future actions, schedules, intentions' },
]

export function ThoughtCapture() {
  const [content, setContent] = useState('')
  const [selectedType, setSelectedType] = useState('thought')
  const [isCapturing, setIsCapturing] = useState(false)
  const { mutate: captureThought } = useCaptureThought()

  const handleCapture = async () => {
    if (!content.trim()) {
      toast.error('Please write something first')
      return
    }

    setIsCapturing(true)

    captureThought({
      content: content.trim(),
      thought_type: selectedType,
      metadata: {
        captured_via: 'manual_input',
        word_count: content.trim().split(' ').length
      }
    }, {
      onSuccess: (response) => {
        toast.success('Thought captured and processed! 🧠')
        setContent('')
        setIsCapturing(false)
      },
      onError: (error) => {
        console.error('Capture error:', error)
        toast.error('Failed to capture thought. Try again.')
        setIsCapturing(false)
      }
    })
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      handleCapture()
    }
  }

  return (
    <div className="flex flex-col h-full p-6 bg-gray-900/30">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <div className="flex items-center gap-3 mb-4">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-neural-500 to-mind-500 flex items-center justify-center">
            <BookOpen className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Feed Your Twin</h1>
            <p className="text-gray-400">Every thought you share makes your digital self more complete</p>
          </div>
        </div>
      </motion.div>

      {/* Thought Type Selection */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="mb-6"
      >
        <h3 className="text-lg font-semibold text-white mb-4">What kind of thought is this?</h3>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {thoughtTypes.map((type) => (
            <motion.button
              key={type.id}
              onClick={() => setSelectedType(type.id)}
              className={`p-4 rounded-2xl border-2 transition-all duration-200 ${
                selectedType === type.id
                  ? 'bg-white/10 border-white/30'
                  : 'bg-white/5 border-white/10 hover:border-white/20'
              }`}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <div className="flex items-center gap-3 mb-2">
                <div className={`w-8 h-8 rounded-xl flex items-center justify-center ${
                  type.color === 'neural' ? 'bg-neural-500/20 text-neural-400' :
                  type.color === 'rose' ? 'bg-rose-500/20 text-rose-400' :
                  type.color === 'emerald' ? 'bg-emerald-500/20 text-emerald-400' :
                  'bg-blue-500/20 text-blue-400'
                }`}>
                  <type.icon className="w-4 h-4" />
                </div>
                <span className="font-medium text-white">{type.label}</span>
              </div>
              <p className="text-sm text-gray-400 text-left">{type.description}</p>
            </motion.button>
          ))}
        </div>
      </motion.div>

      {/* Writing Area */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="flex-1 flex flex-col"
      >
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-white">Express your thoughts</h3>
          <div className="text-sm text-gray-400">
            {content.length}/2000 characters
          </div>
        </div>

        <div className="flex-1 relative">
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Let your thoughts flow... What's been on your mind? What have you learned? What are you planning or dreaming about?"
            className="w-full h-full bg-white/5 border border-white/10 rounded-2xl p-6 text-white placeholder-gray-400 resize-none focus-ring text-lg leading-relaxed"
            maxLength={2000}
            disabled={isCapturing}
          />
          
          {/* Floating Tips */}
          {!content && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 1 }}
              className="absolute top-32 left-6 right-6"
            >
              <div className="glass-effect p-4 rounded-2xl border border-mind-500/20">
                <div className="flex items-center gap-2 text-mind-300 text-sm font-medium mb-2">
                  <Sparkles className="w-4 h-4" />
                  <span>Writing Tips</span>
                </div>
                <ul className="text-sm text-gray-300 space-y-1">
                  <li>• Write naturally - like you're talking to yourself</li>
                  <li>• Share feelings, not just facts</li>
                  <li>• Include context about why something matters to you</li>
                  <li>• Don't worry about grammar - focus on authenticity</li>
                </ul>
              </div>
            </motion.div>
          )}
        </div>

        {/* Action Bar */}
        <div className="flex items-center justify-between mt-6">
          <div className="text-sm text-gray-400">
            Press Ctrl+Enter to capture quickly
          </div>

          <motion.button
            onClick={handleCapture}
            disabled={!content.trim() || isCapturing}
            className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-neural-500 to-mind-500 rounded-2xl text-white font-medium disabled:opacity-50 disabled:cursor-not-allowed focus-ring"
            whileHover={!isCapturing ? { scale: 1.05 } : undefined}
            whileTap={!isCapturing ? { scale: 0.95 } : undefined}
          >
            {isCapturing ? (
              <>
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <span>Processing...</span>
              </>
            ) : (
              <>
                <Send className="w-4 h-4" />
                <span>Capture Thought</span>
              </>
            )}
          </motion.button>
        </div>
      </motion.div>

      {/* Recent Captures Preview */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
        className="mt-8 p-4 rounded-2xl bg-white/5 border border-white/10"
      >
        <h4 className="text-sm font-medium text-white mb-2">Recent Thoughts</h4>
        <div className="text-xs text-gray-400">
          Your recent thoughts will appear here once captured
        </div>
      </motion.div>
    </div>
  )
}