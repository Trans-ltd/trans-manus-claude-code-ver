import { Message, ComponentConfig } from "@/types/api"
import { ReportDisplay } from "@/components/report/ReportDisplay"
import { cn } from "@/lib/utils"

interface MessageBubbleProps {
  message: Message
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user"

  return (
    <div
      className={cn(
        "flex w-full",
        isUser ? "justify-end" : "justify-start"
      )}
    >
      <div
        className={cn(
          "max-w-[80%] rounded-lg px-4 py-2",
          isUser
            ? "bg-primary text-primary-foreground"
            : "bg-muted"
        )}
      >
        {typeof message.content === "string" ? (
          <p className="text-sm">{message.content}</p>
        ) : (
          <ReportDisplay components={message.content as ComponentConfig[]} />
        )}
        <time className="text-xs opacity-70 mt-1 block">
          {message.timestamp.toLocaleTimeString("ja-JP", {
            hour: "2-digit",
            minute: "2-digit",
          })}
        </time>
      </div>
    </div>
  )
}