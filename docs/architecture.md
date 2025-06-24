# Growth Force Reporting Agent - Architecture

## システム概要

Growth Force Reporting Agentは、自然言語によるクエリからBigQueryデータを分析し、インタラクティブなレポートを生成するAIパワードのシステムです。

## アーキテクチャ図

```
┌─────────────────────┐     ┌──────────────────────┐     ┌─────────────────────┐
│   Next.js App       │────▶│  FastAPI Server      │────▶│  Claude Code SDK    │
│   (Frontend)        │◀────│  (Backend)           │◀────│  Process            │
└─────────────────────┘     └──────────────────────┘     └─────────────────────┘
         │                            │                            │
         │                            ▼                            ▼
         │                   ┌─────────────────┐        ┌─────────────────┐
         │                   │     Redis       │        │    BigQuery     │
         │                   │   (Session)     │        │  (Dataset)      │
         │                   └─────────────────┘        └─────────────────┘
         │
         ▼
┌─────────────────────┐
│   Google SSO        │
│  (Authentication)   │
└─────────────────────┘
```

## コンポーネント詳細

### フロントエンド (Next.js 14)

**主要ディレクトリ構造:**
```
frontend/
├── src/
│   ├── app/              # App Router pages
│   │   ├── api/auth/    # NextAuth endpoints
│   │   ├── chat/        # Chat interface (TODO)
│   │   └── login/       # Login page
│   ├── components/      # React components
│   │   └── ui/         # shadcn/ui components
│   └── middleware.ts    # Auth middleware
```

**主要技術:**
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- NextAuth.js (Google SSO)
- Recharts (データ可視化)

**認証フロー:**
1. ユーザーが `/login` にアクセス
2. Google SSOでログイン（@growth-force.co.jpドメインのみ）
3. NextAuthがセッションを作成
4. ミドルウェアが保護されたルートをガード

### バックエンド (FastAPI)

**主要ディレクトリ構造:**
```
backend/
├── src/
│   ├── api/            # API endpoints
│   │   ├── reports.py  # Report generation
│   │   └── bigquery.py # BigQuery testing
│   ├── services/       # Business logic
│   │   ├── claude_service.py    # Claude Code integration
│   │   ├── bigquery_service.py  # BigQuery client
│   │   └── session_service.py   # Session management
│   ├── middleware/     # Security headers
│   ├── config.py       # Configuration
│   └── prompts.py      # Claude prompts
```

**主要技術:**
- FastAPI
- Python 3.11
- uv (パッケージマネージャー)
- Pydantic (バリデーション)
- Redis (セッション管理)

**APIエンドポイント:**
- `POST /api/reports/generate` - レポート生成
- `GET /api/reports/session/{id}` - セッション取得
- `GET /api/bigquery/validate` - BigQuery接続検証 (開発用)
- `GET /api/bigquery/tables` - テーブル一覧 (開発用)

### Claude Code統合

**実装方式:**
```python
ClaudeCodeOptions(
    system_prompt=SYSTEM_PROMPT,
    max_turns=1,
    allowed_tools=["bash"],  # bqコマンドのみ許可
    permission_mode="auto",
)
```

**データフロー:**
1. ユーザーが自然言語でクエリを入力
2. Claude Codeがbqコマンドでスキーマを確認
3. 適切なSQLクエリを生成・実行
4. 結果をJSON形式で返却
5. フロントエンドでコンポーネントをレンダリング

**レスポンス形式:**
```json
{
  "components": [
    {
      "type": "LineChart|BarChart|Summary|Table|Metric",
      "props": { /* component specific props */ }
    }
  ],
  "metadata": {
    "query_executed": "実行したSQL",
    "data_range": "分析期間",
    "row_count": "処理行数"
  }
}
```

### BigQuery統合

**接続設定:**
- プロジェクト: `growth-force-project`
- データセット: `semantic`
- 認証: サービスアカウント（読み取り専用）

**主要テーブル:**
- `fact_shopify_order` - 注文データ
- `fact_meta_ad_performance_daily` - Meta広告パフォーマンス
- `fact_google_ads_campaign_performance_daily` - Google広告
- `dim_customer`, `dim_product`, `dim_campaign` - マスタデータ

### セッション管理

**Redis構成:**
- キー形式: `session:{session_id}`
- TTL: 3600秒（1時間）
- データ: JSON形式でメタデータを保存

### セキュリティ

**実装済みのセキュリティ対策:**
1. **認証**: Google SSO (社内ドメインのみ)
2. **CORS**: 許可されたオリジンのみ
3. **セキュリティヘッダー**: XSS, Clickjacking対策
4. **BigQuery**: 読み取り専用権限
5. **レンダリング**: 動的コード実行を回避（ハイブリッド方式）

### デプロイメント構成

**開発環境:**
- Frontend: `npm run dev` (localhost:3000)
- Backend: `uv run uvicorn src.main:app --reload` (localhost:8000)
- Redis: Docker or local instance

**本番環境（予定）:**
- Frontend: Vercel
- Backend: Google Cloud Run
- Redis: Google Cloud Memorystore
- スケーリング: 0-5インスタンス

## 環境変数

**Frontend (.env.local):**
```
NEXTAUTH_URL
NEXTAUTH_SECRET
GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET
NEXT_PUBLIC_API_URL
```

**Backend (.env):**
```
CLAUDE_API_KEY
BQ_PRIVATE_KEY_ID
BQ_PRIVATE_KEY
BQ_CLIENT_EMAIL
BQ_CLIENT_ID
REDIS_URL
CORS_ORIGINS
```

## 今後の拡張ポイント

1. **MCPサーバー統合**: BigQuery以外のツール連携
2. **キャッシュ戦略**: 同一クエリの結果を再利用
3. **ストリーミング応答**: 長時間処理のプログレス表示
4. **マルチテナント対応**: クライアント別のデータ分離

最終更新: 2024-06-24