# Claude Code サブスクリプション版の認証ハック

## 概要

Claude Codeのサブスクリプション版（ブラウザ版）の認証トークンを使用してAPIアクセスする方法です。

## 必要なトークン

1. **access_token** - アクセストークン
2. **refresh_token** - リフレッシュトークン
3. **expires_at** - 有効期限（Unix timestamp）

## トークンの取得方法

### 方法1: ブラウザの開発者ツールから取得

1. Claude Code（claude.ai/code）にログイン
2. F12で開発者ツールを開く
3. 「Application」タブ → 「Local Storage」または「Session Storage」
4. 認証関連のキーを探す（例: `auth_token`, `session`, etc）

### 方法2: ネットワークタブから取得

1. 開発者ツールの「Network」タブを開く
2. Claude Codeで何か操作を実行
3. APIリクエストのヘッダーから`Authorization`を確認
4. レスポンスからトークン情報を取得

## APIでの使用方法

### 1. トークンを設定

```bash
curl -X POST http://localhost:8000/api/auth/set-tokens \
  -H "Content-Type: application/json" \
  -d '{
    "access_token": "YOUR_ACCESS_TOKEN",
    "refresh_token": "YOUR_REFRESH_TOKEN",
    "expires_at": 1234567890
  }'
```

### 2. 通常通りレポート生成

```bash
curl -X POST http://localhost:8000/api/reports/generate \
  -H "Content-Type: application/json" \
  -d '{
    "query": "今月のMeta広告のパフォーマンスを分析して"
  }'
```

## 実装の仕組み

1. **ClaudeAuthService**がトークンを管理
2. `ANTHROPIC_AUTH_TOKEN`環境変数に`Bearer {access_token}`を設定
3. Claude Code SDKがこの環境変数を使用して認証
4. トークンの有効期限切れ時は自動的にリフレッシュ

## セキュリティ上の注意

⚠️ **警告**: この方法は以下のリスクがあります：

1. **利用規約違反の可能性** - Anthropicの利用規約を確認してください
2. **トークンの漏洩リスク** - トークンは厳重に管理してください
3. **API制限** - 不正使用と判断される可能性があります
4. **動作保証なし** - 公式にサポートされていない方法です

## 代替案

1. **公式APIキー** - Anthropic APIコンソールから取得（推奨）
2. **Claude CLI** - 公式CLIツールを使用
3. **手動運用** - ブラウザで手動操作

## トラブルシューティング

### トークンが無効な場合
- トークンの有効期限を確認
- 正しい形式（Bearer prefix）を使用しているか確認
- ブラウザで再ログインして新しいトークンを取得

### リフレッシュが失敗する場合
- リフレッシュトークンの有効期限切れ
- APIエンドポイントの変更
- 認証フローの変更

## 免責事項

この方法は非公式なハックであり、以下の点にご注意ください：

- いつでも動作しなくなる可能性があります
- Anthropicのサービス利用規約に違反する可能性があります
- 自己責任でご使用ください
- 本番環境での使用は推奨しません

公式のAPIキーを使用することを強く推奨します。