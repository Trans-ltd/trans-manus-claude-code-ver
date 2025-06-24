import { ComponentConfig } from "@/types/api"
import { LineChartComponent } from "./charts/LineChartComponent"
import { BarChartComponent } from "./charts/BarChartComponent"
import { PieChartComponent } from "./charts/PieChartComponent"
import { SummaryCard } from "./SummaryCard"
import { MetricCard } from "./MetricCard"
import { DataTable } from "./DataTable"

interface ReportDisplayProps {
  components: ComponentConfig[]
}

export function ReportDisplay({ components }: ReportDisplayProps) {
  return (
    <div className="space-y-6">
      {components.map((config, idx) => {
        switch (config.type) {
          case "LineChart":
            return <LineChartComponent key={idx} {...config.props} />
          case "BarChart":
            return <BarChartComponent key={idx} {...config.props} />
          case "PieChart":
            return <PieChartComponent key={idx} {...config.props} />
          case "Summary":
            return <SummaryCard key={idx} {...config.props} />
          case "Metric":
            return <MetricCard key={idx} {...config.props} />
          case "Table":
            return <DataTable key={idx} {...config.props} />
          default:
            return null
        }
      })}
    </div>
  )
}