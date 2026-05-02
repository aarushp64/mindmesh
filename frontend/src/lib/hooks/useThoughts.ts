import { useMutation, useQuery } from '@tanstack/react-query'
import { api } from '../api'

interface ThoughtInput {
  content: string
  thought_type?: string
  metadata?: Record<string, any>
}

interface ThoughtResponse {
  id: string
  content: string
  thought_type: string
  emotion: string
  timestamp: string
  embedding_created: boolean
}

interface Memory {
  id: string
  content: string
  thought_type: string
  emotion: string
  metadata: Record<string, any>
  created_at: string
}

export function useCaptureThought() {
  return useMutation({
    mutationFn: async (thought: ThoughtInput): Promise<ThoughtResponse> => {
      const response = await api.post('/thoughts', thought)
      return response.data
    },
  })
}

export function useGetMemories(params?: {
  limit?: number
  thought_type?: string
  emotion?: string
}) {
  return useQuery({
    queryKey: ['memories', params],
    queryFn: async (): Promise<{ memories: Memory[] }> => {
      const response = await api.get('/memories', { params })
      return response.data
    },
  })
}

export function useDeleteMemory() {
  return useMutation({
    mutationFn: async (memoryId: string) => {
      const response = await api.delete(`/memories/${memoryId}`)
      return response.data
    },
  })
}