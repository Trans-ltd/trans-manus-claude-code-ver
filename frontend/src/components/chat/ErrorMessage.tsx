import { AlertCircle } from "lucide-react"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Button } from "@/components/ui/button"

interface ErrorMessageProps {
  error: string
  onRetry?: () => void
}

export function ErrorMessage({ error, onRetry }: ErrorMessageProps) {
  return (
    <Alert variant="destructive">
      <AlertCircle className="h-4 w-4" />
      <AlertTitle>エラーが発生しました</AlertTitle>
      <AlertDescription>
        {error}
        {onRetry && (
          <Button
            variant="link"
            onClick={onRetry}
            className="ml-2 h-auto p-0"
          >
            再試行
          </Button>
        )}
      </AlertDescription>
    </Alert>
  )
}