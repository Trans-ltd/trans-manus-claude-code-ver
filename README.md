# Growth Force Reporting Agent

AI-powered reporting agent for BigQuery semantic dataset analysis using Claude Code SDK.

## 🚀 Features

- **Natural Language Queries**: Ask questions in Japanese about your BigQuery data
- **Automated Report Generation**: Creates interactive charts and summaries
- **Real-time Analysis**: Powered by Claude Code SDK with BigQuery integration
- **Secure Authentication**: Google SSO with domain restrictions
- **Interactive Visualizations**: Built with Recharts for EC-focused analytics

## 📋 Prerequisites

- Node.js 18+
- Python 3.11+
- Google Cloud SDK (`gcloud`)
- Redis (for session management)
- Access to `growth-force-project` BigQuery dataset

## 🛠️ Tech Stack

### Frontend
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS + shadcn/ui
- Recharts for data visualization
- NextAuth.js for authentication

### Backend
- FastAPI (Python)
- uv package manager
- Claude Code SDK
- Google BigQuery SDK
- Redis for sessions

## 📖 Documentation

- [Setup Guide](./docs/setup-guide.md) - Detailed setup instructions
- [Architecture](./docs/architecture.md) - System design and components
- [Product Backlog](./docs/product-backlog.md) - Development progress tracking
- [Claude Subscription Hack](./docs/claude-subscription-hack.md) - Experimental auth method

## 🚦 Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/Trans-ltd/trans-manus-claude-code-ver.git
cd trans-manus-claude-code-ver
```

### 2. Backend Setup

```bash
cd backend
uv sync
cp .env.example .env
# Edit .env with your credentials
uv run uvicorn src.main:app --reload
```

### 3. Frontend Setup

```bash
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local with your credentials
npm run dev
```

### 4. Access the Application

Open http://localhost:3000 in your browser.

## 🔑 Environment Variables

See [Setup Guide](./docs/setup-guide.md) for detailed environment variable configuration.

### Required Keys
- Claude API Key (or subscription tokens)
- Google OAuth credentials
- BigQuery service account
- Redis connection

## 📊 Usage Example

1. Login with your Growth Force Google account
2. Navigate to the chat interface
3. Ask questions like:
   - "今月のMeta広告のパフォーマンスを見せて"
   - "売上が最も高い商品TOP10は？"
   - "先月と今月のROASを比較して"

## 🏗️ Project Structure

```
.
├── backend/          # FastAPI backend
│   ├── src/
│   │   ├── api/     # API endpoints
│   │   ├── services/# Business logic
│   │   └── ...
│   └── ...
├── frontend/         # Next.js frontend
│   ├── src/
│   │   ├── app/     # App Router pages
│   │   ├── components/
│   │   └── ...
│   └── ...
├── docs/            # Documentation
└── README.md
```

## 🧪 Development Status

### ✅ Completed (MVP)
- Project setup with modern tooling
- Google SSO authentication
- Claude Code SDK integration
- BigQuery connection
- Chat interface
- Report visualization components
- Experimental token authentication

### 🔄 In Progress
- End-to-end testing
- Performance optimization
- Error handling improvements

### 📅 Planned
- Session persistence
- Report templates
- Export functionality
- Multi-tenant support

## 🤝 Contributing

This is an internal Growth Force project. Please contact the engineering team for contribution guidelines.

## ⚠️ Security Notes

- Never commit `.env` files
- Use read-only BigQuery service accounts
- Restrict OAuth to company domain
- See [Security Best Practices](./docs/architecture.md#セキュリティ) for details

## 📝 License

Internal use only. Copyright © 2024 Growth Force / Trans Ltd.

## 🆘 Support

- Internal Slack: #tech-support
- Email: engineering@growth-force.co.jp
- GitHub Issues: [Create an issue](https://github.com/Trans-ltd/trans-manus-claude-code-ver/issues)