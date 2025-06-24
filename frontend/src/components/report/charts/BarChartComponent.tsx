"use client"

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface BarData {
  dataKey: string
  name: string
  color: string
}

interface BarChartProps {
  data: any[]
  bars: BarData[]
  title?: string
  xAxis?: string
}

export function BarChartComponent({
  data,
  bars,
  title = "棒グラフ",
  xAxis = "name",
}: BarChartProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={xAxis} />
            <YAxis />
            <Tooltip />
            <Legend />
            {bars.map((bar, idx) => (
              <Bar
                key={idx}
                dataKey={bar.dataKey}
                fill={bar.color}
                name={bar.name}
              />
            ))}
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}