# Changelog

All notable changes to this PoC project will be documented in this file.

## [0.1.0] - 2025-05-01
### Added
- Initial project scaffolding files: `Build_Plan.md`, `changelog.md`.
- Drafted build plan outlining key steps to create FastAPI backend with `fastapi-mcp` integration and an `mcp-use` agent script.

## [0.2.0] - 2025-05-01
### Added
- Created backend FastAPI project with `backend/main.py` exposing `getProductById` and `searchProducts` endpoints.
- Integrated `fastapi-mcp` and mounted MCP server.
- Added simple in-memory product catalogue.
- Added agent directory with `agent/agent_script.py` that connects via `mcp-use` to backend.
- Added project `requirements.txt` listing core dependencies.
- Updated `Build_Plan.md` to tick off repository structure and dependency management tasks.

## [0.3.0] - 2025-05-01
### Added
- Created database layer placeholder using SQLAlchemy
- Added database modules:
  - `backend/db/database.py` with SQLAlchemy engine setup
  - `backend/db/models.py` with Product model
  - `backend/db/crud.py` with database operations
- Updated `Build_Plan.md` to reflect progress on task #5

## [0.4.0] - 2025-05-01
### Added
- Created comprehensive project README.md with:
  - Project overview and description of MCP
  - Installation and setup instructions
  - Usage guide for running backend and agent
  - Project structure explanation
  - "How it works" section explaining the integration flow
  - Next steps and technologies used
- Updated `Build_Plan.md` to check off documentation task

## [0.5.0] - 2025-05-01
### Added
- Successfully ran and tested the agent script connecting to the MCP server
- Added `fastembed` dependency to requirements.txt
- Fixed MCP endpoint URL in agent_script.py to connect properly
- Validated end-to-end flow from agent to FastAPI backend via MCP
### Fixed
- Modified agent endpoint URL from "/mcp/sse" to "/mcp" to correctly connect to the MCP server
