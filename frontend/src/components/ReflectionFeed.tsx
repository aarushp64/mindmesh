'use client'

import { motion } from 'framer-motion'
import { Settings, Calendar, TrendingUp, BookOpen } from 'lucide-react'

export function ReflectionFeed() {
  return (
    <div className="flex flex-col h-full p-6 bg-gray-900/30">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center py-20"
      >
        <div className="w-20 h-20 mx-auto mb-6 rounded-3xl bg-gradient-to-br from-neural-500 to-mind-500 flex items-center justify-center mind-pulse">
          <Settings className="w-10 h-10 text-white" />
        </div>
        <h2 className="text-2xl font-bold text-white mb-4">Automated Reflections</h2>
        <p className="text-gray-400 max-w-md mx-auto mb-8">
          Your twin will generate daily, weekly, and monthly reflection summaries based on your thoughts and patterns.
        </p>
        <div className="grid grid-cols-3 gap-4 max-w-md mx-auto text-sm text-gray-500">
          <div className="flex flex-col items-center gap-2">
            <Calendar className="w-4 h-4" />
            <span>Daily</span>
            <span className="text-xs">No data</span>
          </div>
          <div className="flex flex-col items-center gap-2">
            <TrendingUp className="w-4 h-4" />
            <span>Weekly</span>
            <span className="text-xs">No data</span>
          </div>
          <div className="flex flex-col items-center gap-2">
            <BookOpen className="w-4 h-4" />
            <span>Monthly</span>
            <span className="text-xs">No data</span>
          </div>
        </div>
      </motion.div>
    </div>
  )
}