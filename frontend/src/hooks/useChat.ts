"use client"

import { useState, useCallback } from "react"
import { Message, ReportGenerateRequest, ReportGenerateResponse, ErrorResponse } from "@/types/api"

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [sessionId, setSessionId] = useState<string | null>(null)

  const sendMessage = useCallback(async (query: string) => {
    // Add user message
    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: query,
      timestamp: new Date(),
    }
    setMessages((prev) => [...prev, userMessage])
    setIsLoading(true)
    setError(null)

    try {
      const request: ReportGenerateRequest = {
        query,
        session_id: sessionId || undefined,
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/reports/generate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(request),
      })

      if (!response.ok) {
        const errorData = await response.json() as ErrorResponse
        throw new Error(errorData.error.userMessage || "レポート生成に失敗しました")
      }

      const data = await response.json() as ReportGenerateResponse

      // Update session ID
      if (!sessionId) {
        setSessionId(data.session_id)
      }

      // Add assistant message
      const assistantMessage: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: data.components,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, assistantMessage])

    } catch (err) {
      setError(err instanceof Error ? err.message : "エラーが発生しました")
    } finally {
      setIsLoading(false)
    }
  }, [sessionId])

  const clearMessages = useCallback(() => {
    setMessages([])
    setSessionId(null)
    setError(null)
  }, [])

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    clearMessages,
  }
}