# CLAUDE.md

This file provides guidance to Claude Code when working with the Growth Force Reporting Agent project.

## Project Overview

AI-powered reporting agent that analyzes BigQuery semantic dataset (growth-force-project:semantic) using Claude Code SDK to generate business reports from natural language queries.

## Key Technical Decisions

### Architecture
- **Frontend**: Next.js 14 (App Router) with TypeScript
- **Backend**: Python + FastAPI
- **Chart Library**: Recharts (selected for EC-specific features)
- **Authentication**: Google Workspace SSO
- **Infrastructure**: Vercel (frontend) + Google Cloud Run (backend)

### Rendering Approach
- **Hybrid rendering**: Backend generates component definitions (type + props), frontend renders pre-defined components
- **No direct React code generation**: For security reasons, avoid eval() and dynamic code execution

### Claude Code Integration
- **Dynamic schema retrieval**: Use bq commands to fetch table schemas instead of hardcoding
- **System prompt**: Instruct Claude to first check schemas with bq commands before building queries
- **Timeout**: 10 minutes for API requests, 5 minutes for Claude Code execution

### BigQuery Access
- **Dataset**: growth-force-project:semantic
- **Access method**: Service account with read-only permissions
- **Schema discovery**: Use `bq ls` and `bq show --schema` commands

## User Workflow Preferences

### Git Workflow
- **Commit splitting**: Split commits appropriately by logical changes
- **Commit messages**: Include emoji footer with Claude Code attribution
- **Branch strategy**: Use 'main' as default branch

### Development Workflow
- **Documentation**: Only create documentation files when explicitly requested
- **Error handling**: Provide Japanese user-facing error messages
- **Testing**: Run lint and typecheck commands before marking tasks complete
- **Git commits**: Commit and push automatically when a feature is completed

### Communication Style
- **Language**: Respond in Japanese when user writes in Japanese
- **Conciseness**: Keep responses brief and to the point
- **Proactivity**: Be proactive with planning and implementation

## Project-Specific Requirements

### MVP Scope
1. Natural language query input
2. BigQuery data analysis via Claude Code
3. Chart/graph report generation with Recharts
4. Follow-up question capability

### Security Requirements
- Google SSO authentication (growth-force.co.jp domain only)
- HTTPS communication
- Read-only BigQuery access
- No dynamic code execution

### Performance Requirements
- Report generation within 5 minutes
- API timeout: 10 minutes
- Cloud Run scaling: 0-5 instances max

## Repository Information
- **GitHub**: https://github.com/Trans-ltd/trans-manus-claude-code-ver
- **Organization**: Trans-ltd

## Important Notes
- Always use bq commands for dynamic schema retrieval
- Prefer editing existing files over creating new ones
- Commit and push when features are completed
- Run appropriate lint/typecheck commands after code changes