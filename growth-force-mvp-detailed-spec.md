# Growth Force レポーティングエージェント - MVP詳細仕様

## 1. エラーハンドリング基本仕様

### タイムアウト設定
```python
# config/timeout.py
CLAUDE_CODE_TIMEOUT = 300  # 5分（300秒）
BIGQUERY_TIMEOUT = 120     # 2分（120秒）
API_REQUEST_TIMEOUT = 600  # 10分
```

### エラーレスポンス形式
```typescript
interface ErrorResponse {
  error: {
    code: 'TIMEOUT' | 'CLAUDE_ERROR' | 'BIGQUERY_ERROR' | 'VALIDATION_ERROR';
    message: string;
    userMessage: string;  // ユーザー向けメッセージ
    timestamp: string;
    requestId: string;
  }
}
```

### エラーメッセージマッピング
```python
ERROR_MESSAGES = {
    "TIMEOUT": {
        "user": "分析に時間がかかりすぎました。クエリを簡略化してお試しください。",
        "log": "Operation timed out after {timeout}s"
    },
    "CLAUDE_ERROR": {
        "user": "分析に失敗しました。もう一度お試しください。",
        "log": "Claude Code execution failed: {error}"
    },
    "BIGQUERY_ERROR": {
        "user": "データの取得に失敗しました。しばらく待ってからお試しください。",
        "log": "BigQuery error: {error}"
    },
    "VALIDATION_ERROR": {
        "user": "入力内容を確認してください。",
        "log": "Validation failed: {error}"
    }
}
```

### フロントエンドエラー表示
```tsx
// components/ErrorMessage.tsx
const ErrorMessage: React.FC<{error: ErrorResponse}> = ({error}) => {
  return (
    <Alert variant="destructive">
      <AlertCircle className="h-4 w-4" />
      <AlertTitle>エラーが発生しました</AlertTitle>
      <AlertDescription>
        {error.error.userMessage}
        <Button 
          variant="link" 
          onClick={() => window.location.reload()}
          className="ml-2"
        >
          再読み込み
        </Button>
      </AlertDescription>
    </Alert>
  );
};
```

## 2. Claude Code詳細設定

### システムプロンプト
```python
SYSTEM_PROMPT = """
あなたはBigQueryデータアナリストです。growth-force-project:semanticデータセットを分析して、
ビジネスインサイトを提供します。

## 利用可能なデータセット
bqコマンドを使用して以下のようにデータセットのテーブル一覧を確認できます：
bq ls growth-force-project:semantic

各テーブルのスキーマを確認するには：
bq show --schema --format=prettyjson growth-force-project:semantic.テーブル名

## 出力フォーマット
必ず以下のJSON形式で応答してください：
{
  "components": [
    {
      "type": "LineChart" | "BarChart" | "PieChart" | "Summary" | "Table" | "Metric",
      "props": {
        // コンポーネント固有のプロパティ
      }
    }
  ],
  "metadata": {
    "query_executed": "実行したSQLクエリ",
    "data_range": "分析対象期間",
    "row_count": "処理行数"
  }
}

## 重要な注意事項
1. 大量データをスキャンする前に、WHERE句で期間を絞ってください
2. 金額は日本円（JPY）として扱ってください
3. 日付は日本時間（JST）として扱ってください
4. パフォーマンスメトリクスは適切に集計してください（SUM, AVG等）
"""
```

### 主要テーブルスキーマ
```python
# Claude Codeが動的にスキーマを取得
# システムプロンプトで以下のように指示：
# 1. まず bq ls growth-force-project:semantic でテーブル一覧を確認
# 2. 必要なテーブルに対して bq show --schema でスキーマを取得
# 3. 取得したスキーマ情報を基にクエリを構築
```

### Claude Code実行関数
```python
async def execute_claude_analysis(query: str, session_id: str) -> dict:
    """Claude Codeを使用してクエリを分析"""
    
    # Claude Codeに動的スキーマ取得を指示
    context = f"""
    ユーザーの質問: {query}
    
    まず、必要なテーブルのスキーマをbqコマンドで確認してから、
    適切なSQLクエリを構築してください。
    """
    
    # Claude Code SDK実行
    claude = ClaudeCodeSDK(
        system_prompt=SYSTEM_PROMPT,
        timeout=CLAUDE_CODE_TIMEOUT * 1000  # ミリ秒に変換
    )
    
    try:
        result = await claude.run(context)
        
        # レスポンスのJSON部分を抽出
        json_response = extract_json_from_response(result)
        
        # バリデーション
        validated_response = validate_claude_response(json_response)
        
        return validated_response
        
    except TimeoutError:
        raise ClaudeTimeoutError("Claude Code execution timed out")
    except Exception as e:
        logger.error(f"Claude Code error: {str(e)}")
        raise ClaudeExecutionError(str(e))
```

### レスポンスバリデーション
```python
from pydantic import BaseModel, validator
from typing import List, Dict, Any, Literal

class ComponentProps(BaseModel):
    """コンポーネントのプロパティ基底クラス"""
    pass

class LineChartProps(ComponentProps):
    data: List[Dict[str, Any]]
    lines: List[Dict[str, str]]
    xAxis: str = "date"
    yAxis: str = "value"

class Component(BaseModel):
    type: Literal["LineChart", "BarChart", "PieChart", "Summary", "Table", "Metric"]
    props: Dict[str, Any]
    
    @validator('props')
    def validate_props(cls, v, values):
        component_type = values.get('type')
        # タイプに応じたプロパティ検証
        if component_type == 'LineChart':
            LineChartProps(**v)
        return v

class ClaudeResponse(BaseModel):
    components: List[Component]
    metadata: Dict[str, Any]

def validate_claude_response(response: dict) -> dict:
    """Claude Codeのレスポンスをバリデート"""
    try:
        validated = ClaudeResponse(**response)
        return validated.dict()
    except ValidationError as e:
        logger.error(f"Invalid Claude response: {e}")
        raise ValueError("Invalid response format from Claude Code")
```

## 3. 基本的なUI/UX

### チャット画面コンポーネント
```tsx
// app/chat/page.tsx
export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(() => generateSessionId());

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/reports/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: input,
          session_id: sessionId
        })
      });

      if (!response.ok) {
        throw new Error('API request failed');
      }

      const data = await response.json();
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.components
      }]);
    } catch (error) {
      // エラーハンドリング
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen">
      <Header />
      <div className="flex-1 overflow-y-auto p-4">
        {messages.map((msg, idx) => (
          <MessageBubble key={idx} message={msg} />
        ))}
        {isLoading && <LoadingIndicator />}
      </div>
      <ChatInput 
        value={input}
        onChange={setInput}
        onSubmit={handleSubmit}
        disabled={isLoading}
      />
    </div>
  );
}
```

### ローディング表示
```tsx
// components/LoadingIndicator.tsx
const LoadingIndicator = () => {
  const [dots, setDots] = useState('');
  
  useEffect(() => {
    const interval = setInterval(() => {
      setDots(prev => prev.length >= 3 ? '' : prev + '.');
    }, 500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex items-center space-x-2 p-4">
      <Loader2 className="h-4 w-4 animate-spin" />
      <span className="text-sm text-gray-600">
        分析中{dots}
      </span>
    </div>
  );
};
```

### レポート表示コンポーネント
```tsx
// components/ReportDisplay.tsx
const ReportDisplay: React.FC<{components: ComponentConfig[]}> = ({components}) => {
  return (
    <div className="space-y-6 p-4">
      {components.map((config, idx) => {
        switch (config.type) {
          case 'LineChart':
            return <LineChartComponent key={idx} {...config.props} />;
          case 'BarChart':
            return <BarChartComponent key={idx} {...config.props} />;
          case 'Summary':
            return <SummaryCard key={idx} {...config.props} />;
          case 'Metric':
            return <MetricCard key={idx} {...config.props} />;
          case 'Table':
            return <DataTable key={idx} {...config.props} />;
          default:
            return null;
        }
      })}
    </div>
  );
};

// components/charts/LineChartComponent.tsx
const LineChartComponent: React.FC<LineChartProps> = ({data, lines, xAxis, yAxis}) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>推移グラフ</CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={xAxis} />
            <YAxis />
            <Tooltip />
            <Legend />
            {lines.map((line, idx) => (
              <Line 
                key={idx}
                type="monotone" 
                dataKey={line.dataKey} 
                stroke={line.color}
                name={line.name}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
};
```

## 4. 最小限のセキュリティ

### Google SSO認証設定
```typescript
// app/api/auth/[...nextauth]/route.ts
import NextAuth from 'next-auth';
import GoogleProvider from 'next-auth/providers/google';

export const authOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
      authorization: {
        params: {
          hd: "growth-force.co.jp", // 社内ドメインのみ許可
          prompt: "select_account"
        }
      }
    })
  ],
  callbacks: {
    async signIn({ account, profile }) {
      // 社内ドメインのメールアドレスのみ許可
      if (profile?.email?.endsWith('@growth-force.co.jp')) {
        return true;
      }
      return false;
    },
    async session({ session, token }) {
      session.userId = token.sub;
      return session;
    }
  },
  pages: {
    signIn: '/login',
    error: '/auth/error'
  }
};

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };
```

### ミドルウェア認証チェック
```typescript
// middleware.ts
import { withAuth } from "next-auth/middleware";

export default withAuth({
  pages: {
    signIn: "/login",
  },
});

export const config = {
  matcher: [
    "/chat/:path*",
    "/api/reports/:path*"
  ]
};
```

### BigQuery サービスアカウント設定
```python
# config/bigquery.py
from google.oauth2 import service_account
from google.cloud import bigquery

# サービスアカウントの認証情報
SERVICE_ACCOUNT_JSON = {
    "type": "service_account",
    "project_id": "growth-force-project",
    "private_key_id": os.getenv("BQ_PRIVATE_KEY_ID"),
    "private_key": os.getenv("BQ_PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": os.getenv("BQ_CLIENT_EMAIL"),
    "client_id": os.getenv("BQ_CLIENT_ID"),
}

# 権限スコープ（読み取り専用）
SCOPES = ['https://www.googleapis.com/auth/bigquery.readonly']

def get_bigquery_client():
    """読み取り専用のBigQueryクライアントを取得"""
    credentials = service_account.Credentials.from_service_account_info(
        SERVICE_ACCOUNT_JSON,
        scopes=SCOPES
    )
    return bigquery.Client(
        credentials=credentials,
        project="growth-force-project"
    )
```

### APIセキュリティヘッダー
```python
# middleware/security.py
from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware

def setup_security(app):
    """セキュリティ関連の設定"""
    
    # CORS設定（フロントエンドドメインのみ許可）
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://reporting.growth-force.co.jp",
            "http://localhost:3000"  # 開発環境
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )
    
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response
```

### 環境変数設定
```bash
# .env.local (フロントエンド)
NEXTAUTH_URL=https://reporting.growth-force.co.jp
NEXTAUTH_SECRET=<ランダムな秘密鍵>
GOOGLE_CLIENT_ID=<Google OAuth Client ID>
GOOGLE_CLIENT_SECRET=<Google OAuth Client Secret>
NEXT_PUBLIC_API_URL=https://api-reporting.growth-force.co.jp

# .env (バックエンド)
CLAUDE_API_KEY=<Claude API Key>
BQ_PRIVATE_KEY_ID=<BigQuery Service Account Private Key ID>
BQ_PRIVATE_KEY=<BigQuery Service Account Private Key>
BQ_CLIENT_EMAIL=<BigQuery Service Account Email>
BQ_CLIENT_ID=<BigQuery Service Account Client ID>
REDIS_URL=redis://localhost:6379
LOG_LEVEL=INFO
```

## デプロイメント構成

### Docker設定
```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Cloud Run デプロイ設定
```yaml
# cloud-run.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: reporting-agent-api
spec:
  template:
    metadata:
      annotations:
        run.googleapis.com/execution-environment: gen2
    spec:
      containers:
      - image: gcr.io/growth-force-project/reporting-agent-api
        ports:
        - containerPort: 8000
        env:
        - name: CLAUDE_API_KEY
          valueFrom:
            secretKeyRef:
              name: claude-api-key
              key: latest
        resources:
          limits:
            cpu: "2"
            memory: "4Gi"
        livenessProbe:
          httpGet:
            path: /health
          initialDelaySeconds: 30
          periodSeconds: 30
      serviceAccountName: reporting-agent-sa
      timeoutSeconds: 600
  traffic:
  - percent: 100
    latestRevision: true
  autoscaling:
    minScale: 0
    maxScale: 5  # 最大5インスタンスまでスケール
```