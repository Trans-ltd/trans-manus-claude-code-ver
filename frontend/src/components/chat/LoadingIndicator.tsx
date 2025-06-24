"use client"

import { useEffect, useState } from "react"
import { Loader2 } from "lucide-react"

export function LoadingIndicator() {
  const [dots, setDots] = useState("")

  useEffect(() => {
    const interval = setInterval(() => {
      setDots((prev) => (prev.length >= 3 ? "" : prev + "."))
    }, 500)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="flex items-center space-x-2 p-4">
      <Loader2 className="h-4 w-4 animate-spin" />
      <span className="text-sm text-muted-foreground">
        分析中{dots}
      </span>
    </div>
  )
}