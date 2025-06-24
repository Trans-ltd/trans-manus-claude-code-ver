import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

interface SummaryCardProps {
  text: string
  title?: string
  metrics?: Record<string, any>
}

export function SummaryCard({ text, title = "サマリー", metrics }: SummaryCardProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <CardDescription className="whitespace-pre-wrap">{text}</CardDescription>
        {metrics && (
          <div className="mt-4 grid grid-cols-2 gap-4">
            {Object.entries(metrics).map(([key, value]) => (
              <div key={key} className="text-sm">
                <span className="text-muted-foreground">{key}: </span>
                <span className="font-medium">{value}</span>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  )
}