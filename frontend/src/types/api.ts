export interface ReportGenerateRequest {
  query: string
  session_id?: string
  context?: Record<string, any>
}

export interface ComponentConfig {
  type: "LineChart" | "BarChart" | "PieChart" | "Summary" | "Table" | "Metric"
  props: Record<string, any>
}

export interface ReportGenerateResponse {
  session_id: string
  components: ComponentConfig[]
  metadata?: Record<string, any>
}

export interface ErrorResponse {
  error: {
    code: "TIMEOUT" | "CLAUDE_ERROR" | "BIGQUERY_ERROR" | "VALIDATION_ERROR"
    message: string
    userMessage: string
    timestamp: string
    requestId: string
  }
}

export interface Message {
  id: string
  role: "user" | "assistant" | "system"
  content: string | ComponentConfig[]
  timestamp: Date
}