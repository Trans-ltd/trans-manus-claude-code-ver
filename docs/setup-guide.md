# Growth Force Reporting Agent - セットアップガイド

## 必要な環境変数

### 1. フロントエンド設定 (frontend/.env.local)

```bash
# Next Auth設定
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=<ランダムな32文字以上の文字列を生成>

# Google OAuth設定
GOOGLE_CLIENT_ID=<Google Cloud ConsoleでOAuthクライアントIDを作成>
GOOGLE_CLIENT_SECRET=<同上のクライアントシークレット>

# バックエンドAPI URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### Google OAuth設定手順
1. [Google Cloud Console](https://console.cloud.google.com/)にアクセス
2. 「APIとサービス」→「認証情報」
3. 「認証情報を作成」→「OAuth クライアント ID」
4. アプリケーションの種類: 「ウェブ アプリケーション」
5. 承認済みのリダイレクトURI: `http://localhost:3000/api/auth/callback/google`

### 2. バックエンド設定 (backend/.env)

```bash
# Claude API設定
CLAUDE_API_KEY=<Claude APIキー または 後述の注意事項参照>

# BigQuery サービスアカウント設定
BQ_PRIVATE_KEY_ID=1f17c317f6e66b5a4eabf413c5c581a05c2e7cbf
BQ_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCQX3tnEa5mcJYI\niw02C9BfMBDFRVYYFF3CPxOp1i9pCzVc9+yBlIlFLkP7sKukqc8p3sKBGOBB/Hc8\np24l6AzUoYqTPj4HM83xKl/DFxc9b06TGEH0MchIfnlx6IPQ6dqFg56xNyqFJyYc\nIhhjxcSgP+ibBvQOy9jKnx8z1amyOmWpWzgNCM5f/JpoeylqwOUkCMdddE0DpmP+\n5mcFoRUcpchZlmQO8k5cTl9xnjCeDN6OoiI7PiWTAnYfI90rmuzGlRQW6amqiH4N\n9uoIXM1s5jpm2i5SHdTNjElWkB6qnulcjbfYfH4wKnEFp/kbL9miWxfxO6ryZeKh\n5h6LGv4ZAgMBAAECggEAHQtgd5lKhShUPq6+vyc8SdIRJaavzdNXE2t+KLZCvna3\nSxdDeMQpo4XNvnZJ6awR1cIPTkpzX0MLt+OVGMIoxqQjDUFB2FAXN9PHBSgBkGXy\noEwKhLZ5LQBorT5SOna5dA/JHqzS/IumMpW3Y2cXigehY4LQGaPv3r+JVvO+mnCw\nqT62XfNnnrDlo5d4XhDOYKw+PpUmiHwBSQyIrjp6PBGm8cZb8kG+DIiNuNfCYeHh\nG0Xj83Buwzij0ls5FqUFS2IUN1gNAO2+QpIcotgHwEc5JHO5qzf3dk88AFv3OKoZ\ntZYvrwf6dVatGVX22x1FisPLlVEG3hLNQli5GnKikwKBgQDK10WucvjWf7tWIL+H\nkZ+8dTMkYGne9yRuOxiEx3nf9Zs4+yGhDkNMBIvo4TsrkpSt126H0ZlyHwe+1Drf\nfhoxS7zUODiMXo6n0amC9HqqEsEXnJmBLdYUicyNeqLf+ivu2TJSOvCTF8AC8pt2\nHwCHhuOvLJQ6bftTtR12TBqNKwKBgQC2NY78roC/wANcGFWlhuVxn1F1daZdDACI\nUkSzNdl0OhThOL4ujLufxLR36l1Emk28XhkkvabzDLGj57MNY3H/CFZDH6ovhRDo\n9Pe93xEMDkZPmbkbN1+/IhOWtA4bLGs0YY3z75a+TfRtC4sHBHQy1f8bKET+Onbc\nr6QOwOKnywKBgQC0QAR991FFW5CgAs3wrOmj0Qo3Yy3xovFOu1kYdSLKcDkVs6S4\nuDH5VXj2419vYvyYVv6z1wBit0xsua/vduHTuJf+hk9J/aULYHcgFh0DEVNhphmK\n/65j5ehOORKPsoJj58Kd7B5ouAw7Elgv6XDQ/n9J5XV7TsyuIB4kR5C4rQKBgAZI\nionEKsRyBquiWzG+GSN17wUx7W6//zS0QZI8hScw6Y9quYQ5bi7wRZjtCBJZj9yz\nEgLmV1+CTI3ua4pGp6O30eG2sdO5rv+ZkwGFM71KsLoF/xAlNLQOpMZJp0LgoUHJ\nK3ACDxy463jnMQAo8yjdoFJ7bQWnVnn9xJaNqENJAoGAZUGSRaYUGPorAIYe4Qi5\nqLtEeyAGck0Hon0FLS7dc2cBUggfghnfMTXSfcRL7XZxnYmEaalNxyqGsLp2jwp+\n7bExZFARI7/Uf9V5qLJ2hTiOkmypoBkLBEyeLOiGXJxLulPFygY/HmjAOQuqvK6+\nJ2ttox9kA3vbV+LSqfn6WrQ=\n-----END PRIVATE KEY-----
BQ_CLIENT_EMAIL=reporting-agent@growth-force-project.iam.gserviceaccount.com
BQ_CLIENT_ID=113474805453801263193

# Redis設定
REDIS_URL=redis://localhost:6379

# API設定
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO

# CORS設定
CORS_ORIGINS=http://localhost:3000

# 環境設定
ENVIRONMENT=development
```

### 3. その他必要なサービス

#### Redis
```bash
# Dockerを使用する場合
docker run -d -p 6379:6379 redis:alpine

# またはHomebrewでインストール（Mac）
brew install redis
brew services start redis
```

## Claude Code サブスクリプション版を使用する場合

現在の実装はClaude Code SDKを使用していますが、サブスクリプション版（ブラウザ版）を使用したい場合は以下の変更が必要です：

### 方法1: Claude CLI経由での利用
1. Claude CLIをインストール: `npm install -g @anthropic-ai/claude-code`
2. ブラウザでログイン: `claude-code login`
3. バックエンドのClaude Service実装を変更してCLIを呼び出す

### 方法2: 手動での利用
1. ブラウザでClaude Codeにログイン
2. バックエンドでクエリを生成し、手動でコピー＆ペースト
3. 結果を手動でシステムに入力

**注意**: サブスクリプション版の自動化は技術的に難しく、APIキーを使用する方が推奨されます。

## 起動手順

### バックエンド
```bash
cd backend
uv sync
uv run uvicorn src.main:app --reload
```

### フロントエンド
```bash
cd frontend
npm install
npm run dev
```

アプリケーションは http://localhost:3000 でアクセスできます。