'use client'

import { motion } from 'framer-motion'
import { Brain, Network, Zap } from 'lucide-react'

export function MindGraph() {
  return (
    <div className="flex flex-col h-full p-6 bg-gray-900/30">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center py-20"
      >
        <div className="w-20 h-20 mx-auto mb-6 rounded-3xl bg-gradient-to-br from-neural-500 to-mind-500 flex items-center justify-center mind-pulse">
          <Network className="w-10 h-10 text-white" />
        </div>
        <h2 className="text-2xl font-bold text-white mb-4">Mind Graph Visualization</h2>
        <p className="text-gray-400 max-w-md mx-auto mb-8">
          Your thought network will appear here once you've captured more memories and reflections.
        </p>
        <div className="flex items-center justify-center gap-4 text-sm text-gray-500">
          <div className="flex items-center gap-2">
            <Brain className="w-4 h-4" />
            <span>Memories: 0</span>
          </div>
          <div className="flex items-center gap-2">
            <Zap className="w-4 h-4" />
            <span>Connections: 0</span>
          </div>
        </div>
      </motion.div>
    </div>
  )
}