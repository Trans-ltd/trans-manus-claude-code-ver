"use client"

import { useSession } from "next-auth/react"
import { redirect } from "next/navigation"
import { useChat } from "@/hooks/useChat"
import { ChatInput } from "@/components/chat/ChatInput"
import { MessageBubble } from "@/components/chat/MessageBubble"
import { LoadingIndicator } from "@/components/chat/LoadingIndicator"
import { ErrorMessage } from "@/components/chat/ErrorMessage"
import { Button } from "@/components/ui/button"
import { Trash2 } from "lucide-react"

export default function ChatPage() {
  const { data: session, status } = useSession()
  const { messages, isLoading, error, sendMessage, clearMessages } = useChat()

  if (status === "loading") {
    return <div>Loading...</div>
  }

  if (!session) {
    redirect("/login")
  }

  return (
    <div className="flex h-screen flex-col">
      {/* Header */}
      <header className="border-b bg-background px-4 py-3">
        <div className="mx-auto flex max-w-4xl items-center justify-between">
          <h1 className="text-lg font-semibold">Growth Force Reporting Agent</h1>
          <div className="flex items-center gap-4">
            <span className="text-sm text-muted-foreground">
              {session.user?.email}
            </span>
            {messages.length > 0 && (
              <Button
                variant="ghost"
                size="sm"
                onClick={clearMessages}
                title="会話をクリア"
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            )}
          </div>
        </div>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto">
        <div className="mx-auto max-w-4xl space-y-4 p-4">
          {messages.length === 0 && (
            <div className="text-center text-muted-foreground py-12">
              <p className="text-lg mb-2">BigQueryデータ分析を始めましょう</p>
              <p className="text-sm">
                例: 「今月のMeta広告のパフォーマンスを見せて」
              </p>
            </div>
          )}
          {messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}
          {isLoading && <LoadingIndicator />}
          {error && <ErrorMessage error={error} />}
        </div>
      </div>

      {/* Input */}
      <ChatInput onSubmit={sendMessage} disabled={isLoading} />
    </div>
  )
}