"use client"

import { signIn } from "next-auth/react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export default function LoginPage() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <Card className="w-[400px]">
        <CardHeader>
          <CardTitle>ログイン</CardTitle>
          <CardDescription>
            Growth Forceアカウントでログインしてください
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Button 
            onClick={() => signIn("google", { callbackUrl: "/chat" })}
            className="w-full"
          >
            Googleでログイン
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}