import Link from "next/link"
import { Button } from "@/components/ui/button"

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-24">
      <main className="flex flex-col items-center gap-8">
        <h1 className="text-4xl font-bold">Growth Force Reporting Agent</h1>
        <p className="text-xl text-muted-foreground">
          BigQueryデータを分析してレポートを自動生成
        </p>
        <Link href="/chat">
          <Button size="lg">分析を開始</Button>
        </Link>
      </main>
    </div>
  )
}