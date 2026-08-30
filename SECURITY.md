# Atlas Lab Security Guidelines

## Data Storage
- All data stored locally in SQLite (user data directory, not globally writable)
- No automatic cloud uploads or external data transmission
- Document processing is performed locally

## File Handling
- Path traversal protection on all file operations
- Only permitted file types (.pdf, .txt, .md, .csv, .docx) are processed
- File paths validated against allowed directories

## Process Security
- No arbitrary shell execution from user input
- Commands validated before execution
- Python backend runs as isolated process

## Input Validation
- All API endpoints validate input with Pydantic
- SQL queries restricted to SELECT only (database commands layer)
- JSON inputs sanitized before processing

## Authentication
- Local-only application; no remote authentication required
- If remote AI is used, API keys stored securely (environment variables)
- No hardcoded credentials in source

## Network
- Default mode is offline; no data sent without user consent
- Remote AI services must be explicitly enabled
- All internet usage clearly indicated to user
