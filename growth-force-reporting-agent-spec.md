# Growth Force レポーティングエージェント - 技術仕様書

## プロジェクト概要
BigQueryのsemanticデータセットを分析し、自然言語による質問からレポートを自動生成するAIエージェントシステム。社内ツールから開始し、段階的にクライアント向けに拡張予定。

## 外部要件定義

### エピック

#### エピック1: 基本レポート生成
**概要**: 自然言語による質問からBigQueryデータを分析し、レポートを自動生成する

**ユーザーストーリー:**
- マーケティング担当者として、「今月のMeta広告のCPAは？」と質問して、即座に分析結果を確認したい
- データアナリストとして、「売上が下がった原因は？」と聞いて、関連データを自動調査してほしい
- マネージャーとして、複雑なSQLを書かずに、日次・週次レポートを自動生成したい

#### エピック2: インタラクティブ分析
**概要**: 初回レポートに対する追加質問で深掘り分析を実行

**ユーザーストーリー:**
- レポート結果を見て、「この数値が高い理由は？」と追加質問したい
- 「同期間の前年比は？」など、関連する比較分析を簡単に依頼したい
- 異常値を発見した際に、「この日に何があった？」と詳細調査したい

#### エピック3: ダッシュボード機能
**概要**: よく使う分析をダッシュボード化して定期実行

**ユーザーストーリー:**
- 毎朝、主要KPIの前日実績を自動レポートで受け取りたい
- チーム全体で共有できる定期レポートを設定したい
- アラート機能で、異常値検知時に通知を受けたい

### 機能要件

#### 必須機能 (MVP)
- 自然言語での質問入力
- BigQueryデータの自動分析
- グラフ・チャート付きレポート生成
- 追加質問による深掘り分析

#### 拡張機能 (Phase 2)
- 定期レポート設定
- アラート・通知機能
- レポート共有・エクスポート
- カスタムダッシュボード

#### 将来機能 (Phase 3)
- 予測分析・トレンド予測
- 自動最適化提案
- 多言語対応
- クライアント向けホワイトラベル

### 非機能要件
- **パフォーマンス**: レポート生成5分以内
- **可用性**: 99.9%稼働率
- **セキュリティ**: 社内認証、データアクセス制御
- **スケーラビリティ**: 50人同時利用対応

## 技術スタック

### フロントエンド
- **Next.js 14 (App Router)** - サーバーサイドレンダリング対応
- **TypeScript** - 型安全性
- **Tailwind CSS** - スタイリング
- **shadcn/ui** - UIコンポーネント
- **Recharts** - EC向けグラフ・チャート描画（選定理由：ECに特化、軽量、TypeScript対応）

### バックエンド
- **Python + FastAPI** - 高速APIフレームワーク
- **Claude Code SDK (Python版)** - AIエージェント統合
- **Google Cloud BigQuery SDK** - データベース連携
- **Pydantic** - データバリデーション
- **Redis** - セッション管理

### データ基盤
- **BigQuery** - growth-force-project:semanticデータセット
- **bqコマンド / Google Cloud SDK** - データアクセス
- **サービスアカウント認証** - セキュアな接続

### インフラ（MVP段階）
- **Vercel** - フロントエンドホスティング
- **Google Cloud Run** - バックエンドAPI
- **Google Cloud Redis** - セッション管理

### 認証・セキュリティ
- **Google Workspace SSO** - シングルサインオン
- **NextAuth.js** - 認証ライブラリ
- **RBAC** - ロールベースアクセス制御

## アーキテクチャ

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Next.js App   │────▶│  FastAPI Server │────▶│  Claude Code    │
│   (Frontend)    │◀────│   (Backend)     │◀────│  SDK Process    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │                          │
                               ▼                          ▼
                        ┌─────────────┐          ┌─────────────┐
                        │    Redis    │          │   BigQuery  │
                        │  (Session)  │          │  (Dataset)  │
                        └─────────────┘          └─────────────┘
```

## API仕様

### レポート生成エンドポイント

```python
POST /api/reports/generate
{
  "query": "今月のMeta広告のパフォーマンスは？",
  "session_id": "uuid-v4",
  "context": {
    "client_id": "optional-filter"
  }
}

Response:
{
  "session_id": "uuid-v4",
  "components": [
    {
      "type": "LineChart",
      "props": {
        "data": [...],
        "lines": [
          {"dataKey": "spend", "name": "広告費", "color": "#8884d8"},
          {"dataKey": "revenue", "name": "売上", "color": "#82ca9d"}
        ]
      }
    },
    {
      "type": "Summary",
      "props": {
        "text": "今月のMeta広告は...",
        "metrics": {
          "roas": 3.2,
          "spend": 1500000
        }
      }
    }
  ]
}
```

## レンダリング方式

ハイブリッド方式を採用：
- バックエンドでコンポーネント定義（type + props）を生成
- フロントエンドで事前定義されたコンポーネントを安全にレンダリング
- セキュリティを保ちながら柔軟性を確保

### フロントエンドコンポーネント構造

```typescript
// チャートレジストリ
const chartComponents = {
  LineChart: RechartsLineChart,
  BarChart: RechartsBarChart,
  PieChart: RechartsPieChart,
  Summary: CustomSummaryCard,
  Table: DataTable,
  Metric: MetricCard
};

// レンダラー
interface ComponentConfig {
  type: keyof typeof chartComponents;
  props: Record<string, any>;
}

const ReportRenderer: React.FC<{components: ComponentConfig[]}> = ({components}) => {
  return (
    <div className="space-y-6">
      {components.map((config, idx) => {
        const Component = chartComponents[config.type];
        return <Component key={idx} {...config.props} />;
      })}
    </div>
  );
};
```

## Claude Code統合仕様

```python
# Claude Code実行
async def execute_report_query(query: str, session_id: str):
    # Claude Code SDKでプロセス起動
    claude = ClaudeCodeSDK(
        system_prompt="""
        あなたはBigQueryデータアナリストです。
        growth-force-project:semanticデータセットを分析して、
        Recharts用のコンポーネント定義を返してください。
        """
    )
    
    # BigQuery分析を実行
    result = await claude.run(f"""
        {query}
        
        必要なデータをBigQueryから取得し、
        以下の形式でレポートを作成してください:
        {{
          "components": [
            {{
              "type": "チャートタイプ",
              "props": {{...}}
            }}
          ]
        }}
    """)
    
    return parse_claude_response(result)
```

## データセット概要

growth-force-project:semanticデータセットには以下のテーブルが含まれる：

### Fact Tables
- fact_shopify_order - 注文データ
- fact_meta_ad_performance_daily - Meta広告パフォーマンス
- fact_google_ads_campaign_performance_daily - Google広告パフォーマンス
- fact_inventory_snapshot_daily - 在庫スナップショット

### Dimension Tables
- dim_customer - 顧客マスタ
- dim_product - 商品マスタ
- dim_campaign - キャンペーンマスタ
- dim_ad - 広告マスタ

### 特徴
- 日次パーティション（ほとんどのFactテーブル）
- マルチプラットフォーム対応（Meta、Google、Yahoo、Instagram、Shopify）
- クラスタリング最適化済み

## セキュリティ考慮事項

1. **動的コード実行の回避**: Reactコードを直接生成せず、データ構造のみを返す
2. **認証・認可**: Google Workspace SSOとRBACによるアクセス制御
3. **データアクセス制限**: BigQueryのサービスアカウント権限を最小限に
4. **セッション管理**: Redisでの安全なセッション管理
5. **入力検証**: Pydanticによる厳格なデータバリデーション

## 今後の実装計画

1. **Phase 1 (MVP)**: 基本的なレポート生成機能
2. **Phase 2**: ダッシュボード機能、定期レポート
3. **Phase 3**: 予測分析、マルチテナント対応

## 追加仕様検討項目

### 1. エラーハンドリング・障害対応
- タイムアウト処理: Claude Code/BigQueryの実行時間制限
- リトライ戦略: 失敗時の再実行ロジック
- エラーメッセージ: ユーザー向けのわかりやすいエラー表示
- フォールバック: AIが失敗した時の代替処理

### 2. パフォーマンス最適化
- キャッシュ戦略: 同じクエリの結果をどう再利用するか
- BigQueryコスト最適化: スキャン量削減の仕組み
- ストリーミング応答: 長時間処理のプログレス表示
- 同時実行数制限: Claude Codeプロセスの管理

### 3. データガバナンス
- アクセス制御: クライアント間のデータ分離
- 監査ログ: 誰がいつどんなクエリを実行したか
- データマスキング: 機密情報の保護
- 利用量制限: ユーザー/部門別のクォータ

### 4. UI/UX詳細設計
- チャット履歴: セッション管理とUIデザイン
- レポートテンプレート: よく使うレポートの保存
- エクスポート機能: PDF/Excel/画像形式
- モバイル対応: レスポンシブデザイン

### 5. Claude Code詳細設定
- プロンプトエンジニアリング: 最適なシステムプロンプト
- コンテキスト管理: データスキーマの効率的な渡し方
- MCPサーバー設定: BigQuery以外のツール連携
- モデル選択: タスクに応じたモデル切り替え

### 6. 運用・保守
- デプロイメント: CI/CDパイプライン
- モニタリング: メトリクス収集（Datadog/CloudWatch）
- ログ管理: 構造化ログとトレーシング
- バックアップ: セッションデータの永続化

### 7. ビジネスロジック
- レポート品質保証: AIの出力検証ルール
- コスト計算: 利用料金の算出ロジック
- 権限モデル: 部門/役職別のデータアクセス
- SLA定義: 応答時間やアップタイムの保証

### 8. 拡張性・統合
- Webhook/API公開: 外部システムからの利用
- Slack/Teams連携: チャットボット機能
- 定期実行: cronジョブ的な仕組み
- アラート配信: 閾値超過時の通知