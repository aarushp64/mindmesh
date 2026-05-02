'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Brain, MessageCircle, BookOpen, BarChart3, Settings } from 'lucide-react'
import { ChatInterface } from '@/components/ChatInterface'
import { ThoughtCapture } from '@/components/ThoughtCapture'
import { MindGraph } from '@/components/MindGraph'
import { PersonalityDashboard } from '@/components/PersonalityDashboard'
import { ReflectionFeed } from '@/components/ReflectionFeed'

const navItems = [
  { id: 'chat', icon: MessageCircle, label: 'Chat with Twin', description: 'Talk to your digital self' },
  { id: 'capture', icon: BookOpen, label: 'Capture Thoughts', description: 'Feed your twin' },
  { id: 'mind', icon: Brain, label: 'Mind Graph', description: 'Visualize your thoughts' },
  { id: 'insights', icon: BarChart3, label: 'Insights', description: 'Your personality profile' },
  { id: 'reflection', icon: Settings, label: 'Reflections', description: 'Automated summaries' },
]

export default function MindMeshApp() {
  const [activeView, setActiveView] = useState<string>('chat')

  const renderActiveView = () => {
    switch (activeView) {
      case 'chat':
        return <ChatInterface />
      case 'capture':
        return <ThoughtCapture />
      case 'mind':
        return <MindGraph />
      case 'insights':
        return <PersonalityDashboard />
      case 'reflection':
        return <ReflectionFeed />
      default:
        return <ChatInterface />
    }
  }

  return (
    <div className="flex h-screen bg-gray-900">
      {/* Sidebar Navigation */}
      <motion.div 
        initial={{ x: -100, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        className="w-80 glass-effect border-r border-white/10 p-6"
      >
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-neural-500 to-mind-500 flex items-center justify-center mind-pulse">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">MindMesh</h1>
              <p className="text-sm text-gray-400">Your Digital Twin</p>
            </div>
          </div>
          <div className="h-px bg-gradient-to-r from-neural-500 to-mind-500 opacity-50"></div>
        </div>

        {/* Navigation */}
        <nav className="space-y-2">
          {navItems.map((item) => (
            <motion.button
              key={item.id}
              onClick={() => setActiveView(item.id)}
              className={`w-full flex items-center gap-3 p-3 rounded-xl transition-all duration-200 group ${
                activeView === item.id
                  ? 'bg-neural-600/30 text-white border border-neural-500/50'
                  : 'text-gray-400 hover:text-white hover:bg-white/5'
              }`}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <item.icon className={`w-5 h-5 ${
                activeView === item.id ? 'text-neural-400' : 'text-gray-500 group-hover:text-gray-300'
              }`} />
              <div className="text-left">
                <div className="font-medium">{item.label}</div>
                <div className="text-xs opacity-75">{item.description}</div>
              </div>
            </motion.button>
          ))}
        </nav>

        {/* Status Indicator */}
        <motion.div 
          className="mt-8 p-4 rounded-xl bg-gradient-to-r from-green-500/20 to-emerald-500/20 border border-green-500/30"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
        >
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-sm text-green-300">Twin is awake and learning</span>
          </div>
          <p className="text-xs text-green-300/70 mt-1">
            Processed 0 thoughts today
          </p>
        </motion.div>
      </motion.div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Top Bar */}
        <motion.header 
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="h-16 glass-effect border-b border-white/10 px-6 flex items-center justify-between"
        >
          <div>
            <h2 className="text-lg font-semibold text-white">
              {navItems.find(item => item.id === activeView)?.label}
            </h2>
            <p className="text-sm text-gray-400">
              {navItems.find(item => item.id === activeView)?.description}
            </p>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="text-right">
              <div className="text-sm font-medium text-white">Welcome back</div>
              <div className="text-xs text-gray-400">Ready to reflect?</div>
            </div>
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-neural-400 to-mind-400 flex items-center justify-center">
              <span className="text-sm font-bold text-white">You</span>
            </div>
          </div>
        </motion.header>

        {/* Content Area */}
        <motion.main 
          key={activeView}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className="flex-1 overflow-hidden"
        >
          {renderActiveView()}
        </motion.main>
      </div>
    </div>
  )
}