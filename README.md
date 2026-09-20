# 🧠 MCP-Powered AI Learning Path Generator

A student-friendly project demonstrating how an AI learning application can use the
**Model Context Protocol (MCP)** to call structured tools.

## Current architecture

```text
User
  ↓
Streamlit Web App
  ↓
MCP Client
  ↓
MCP Server
  ├── generate_learning_path
  └── find_learning_resources
  ↓
Personalized Learning Path
```

## Features

- Learning topic, duration and level input
- Day-by-day roadmap
- Concepts and practice tasks
- Project ideas
- Learning resource links
- JSON download
- Real MCP client → MCP server tool calls

## Run locally

Python 3.10+ is required.

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install:

```bash
pip install -r requirements.txt
```

Run:

```bash
streamlit run app.py
```

## MCP inspection

The official MCP Python SDK provides development tooling. You can inspect the
server separately with:

```bash
mcp dev mcp_server.py
```

## Next integration stage

For the workshop submission, this starter can be extended with real external
services:

- YouTube search/API tool
- Google Drive document creation
- Notion page creation
- Optional LLM-generated personalization

Keep credentials in environment variables or Streamlit secrets. Never commit
real API keys.

## Project purpose

This is not just a chatbot. The application demonstrates the MCP pattern:

**AI/application → MCP client → MCP server → tools → structured results**

## License

For educational/project use.
