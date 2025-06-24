# Growth Force Reporting Agent

AI-powered reporting agent for BigQuery semantic dataset analysis using Claude Code SDK.

## Project Structure

```
.
├── backend/        # Python FastAPI backend
├── frontend/       # Next.js frontend
├── docs/          # Project documentation
└── README.md
```

## Features

- Natural language query interface
- BigQuery data analysis via Claude Code
- Interactive chart generation with Recharts
- Follow-up question capability
- Google Workspace SSO authentication

## Tech Stack

- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, Recharts
- **Backend**: Python, FastAPI, Claude Code SDK
- **Database**: Google BigQuery (growth-force-project:semantic)
- **Infrastructure**: Vercel, Google Cloud Run

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.11+
- Google Cloud SDK
- BigQuery access to growth-force-project

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
uvicorn main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local with your credentials
npm run dev
```

## Development

See [CLAUDE.md](./CLAUDE.md) for development guidelines and conventions.

## Documentation

- [Technical Specification](./growth-force-reporting-agent-spec.md)
- [MVP Detailed Specification](./growth-force-mvp-detailed-spec.md)