import { useMutation } from '@tanstack/react-query'
import { api } from '../api'

interface ChatMessage {
  message: string
  context_limit?: number
}

interface ChatResponse {
  response: string
  context_memories: Array<{
    id: string
    content: string
    thought_type: string
    emotion: string
    similarity: number
  }>
  personality_insight?: string
}

export function useChatWithTwin() {
  return useMutation({
    mutationFn: async (message: ChatMessage): Promise<ChatResponse> => {
      const response = await api.post('/chat', message)
      return response.data
    },
  })
}