'use client'

import { motion } from 'framer-motion'
import { BarChart3, Heart, Target, Sparkles } from 'lucide-react'

export function PersonalityDashboard() {
  return (
    <div className="flex flex-col h-full p-6 bg-gray-900/30">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center py-20"
      >
        <div className="w-20 h-20 mx-auto mb-6 rounded-3xl bg-gradient-to-br from-neural-500 to-mind-500 flex items-center justify-center mind-pulse">
          <BarChart3 className="w-10 h-10 text-white" />
        </div>
        <h2 className="text-2xl font-bold text-white mb-4">Personality Insights</h2>
        <p className="text-gray-400 max-w-md mx-auto mb-8">
          Your digital twin's personality profile will develop as you share more thoughts and interact more.
        </p>
        <div className="grid grid-cols-3 gap-4 max-w-md mx-auto text-sm text-gray-500">
          <div className="flex flex-col items-center gap-2">
            <Heart className="w-4 h-4" />
            <span>Emotions</span>
            <span className="text-xs">Neutral</span>
          </div>
          <div className="flex flex-col items-center gap-2">
            <Target className="w-4 h-4" />
            <span>Goals</span>
            <span className="text-xs">None yet</span>
          </div>
          <div className="flex flex-col items-center gap-2">
            <Sparkles className="w-4 h-4" />
            <span>Traits</span>
            <span className="text-xs">Learning...</span>
          </div>
        </div>
      </motion.div>
    </div>
  )
}