'use client'

import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Send, Bot, User, Sparkles, Clock } from 'lucide-react'
import { useChatWithTwin } from '@/lib/hooks/useChat'
import { formatDistanceToNow } from 'date-fns'

interface Message {
  id: string
  content: string
  role: 'user' | 'twin'
  timestamp: Date
  personalityInsight?: string
}

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      content: "Hey there... it's me, but not quite me. I'm your digital reflection, slowly learning who we are together. What's on your mind?",
      role: 'twin',
      timestamp: new Date(),
    }
  ])
  const [input, setInput] = useState('')
  const [isThinking, setIsThinking] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const { mutate: sendMessage } = useChatWithTwin()

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async () => {
    if (!input.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      content: input.trim(),
      role: 'user',
      timestamp: new Date(),
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsThinking(true)

    // Send to AI twin
    sendMessage({
      message: input.trim(),
      context_limit: 10
    }, {
      onSuccess: (response) => {
        const twinMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: response.response,
          role: 'twin',
          timestamp: new Date(),
          personalityInsight: response.personality_insight
        }
        setMessages(prev => [...prev, twinMessage])
        setIsThinking(false)
      },
      onError: (error) => {
        console.error('Chat error:', error)
        const errorMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: "I'm having trouble accessing my thoughts right now. Could you try again?",
          role: 'twin',
          timestamp: new Date(),
        }
        setMessages(prev => [...prev, errorMessage])
        setIsThinking(false)
      }
    })
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="flex flex-col h-full bg-gray-900/50">
      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        <AnimatePresence>
          {messages.map((message, index) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
              className={`flex gap-4 ${message.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}
            >
              {/* Avatar */}
              <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
                message.role === 'user' 
                  ? 'bg-gradient-to-br from-neural-500 to-neural-600' 
                  : 'bg-gradient-to-br from-primary-500 to-primary-600 mind-pulse'
              }`}>
                {message.role === 'user' ? (
                  <User className="w-5 h-5 text-white" />
                ) : (
                  <Bot className="w-5 h-5 text-white" />
                )}
              </div>

              {/* Message Content */}
              <div className={`flex-1 max-w-2xl ${message.role === 'user' ? 'text-right' : 'text-left'}`}>
                <div className={`inline-block p-4 rounded-2xl ${
                  message.role === 'user' 
                    ? 'bg-neural-600/20 text-white' 
                    : 'bg-white/5 text-gray-100 border border-white/10'
                }`}>
                  <p className="whitespace-pre-wrap leading-relaxed">{message.content}</p>
                  
                  {/* Timestamp */}
                  <div className={`flex items-center gap-1 mt-2 text-xs text-gray-400 ${
                    message.role === 'user' ? 'justify-end' : 'justify-start'
                  }`}>
                    <Clock className="w-3 h-3" />
                    <span>{formatDistanceToNow(message.timestamp, { addSuffix: true })}</span>
                  </div>
                </div>

                {/* Personality Insight */}
                {message.personalityInsight && (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.5 }}
                    className="mt-2 p-3 rounded-xl bg-mind-500/10 border border-mind-500/20 max-w-md"
                  >
                    <div className="flex items-center gap-2 text-mind-300 text-xs font-medium mb-1">
                      <Sparkles className="w-3 h-3" />
                      <span>Personality Insight</span>
                    </div>
                    <p className="text-sm text-mind-200/80">{message.personalityInsight}</p>
                  </motion.div>
                )}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {/* Thinking Indicator */}
        {isThinking && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex gap-4"
          >
            <div className="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-primary-500 to-primary-600 flex items-center justify-center mind-pulse">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <div className="flex-1">
              <div className="inline-block p-4 rounded-2xl bg-white/5 border border-white/10">
                <div className="flex items-center gap-2">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-primary-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-primary-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-primary-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                  <span className="text-sm text-gray-400">Your twin is reflecting...</span>
                </div>
              </div>
            </div>
          </motion.div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-white/10 p-6">
        <div className="flex gap-4 items-end">
          <div className="flex-1">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Share what's on your mind... your twin is listening."
              className="w-full bg-white/5 border border-white/10 rounded-2xl p-4 text-white placeholder-gray-400 resize-none focus-ring min-h-[60px] max-h-[200px]"
              rows={1}
              disabled={isThinking}
            />
            <div className="flex justify-between items-center mt-2 px-2">
              <div className="text-xs text-gray-500">
                Press Enter to send, Shift+Enter for new line
              </div>
              <div className="text-xs text-gray-500">
                {input.length}/1000
              </div>
            </div>
          </div>
          
          <motion.button
            onClick={handleSendMessage}
            disabled={!input.trim() || isThinking}
            className="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-neural-500 to-neural-600 rounded-2xl flex items-center justify-center text-white disabled:opacity-50 disabled:cursor-not-allowed focus-ring"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Send className="w-5 h-5" />
          </motion.button>
        </div>
      </div>
    </div>
  )
}