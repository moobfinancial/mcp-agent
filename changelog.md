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

## [0.4.0] - 2025-05-02
### Added
- Implemented MCP middleware for routing agent requests to API endpoints
- Created comprehensive configuration system for intent-to-endpoint mapping
- Added parameter validation and response formatting
- Implemented authentication handling for secure communication
- Created thorough test suite with 100% test coverage for configuration
- Added example script demonstrating middleware usage

### Updated
- Enhanced README with middleware documentation and usage examples
- Updated Build Plan to prioritize MCP integration roadmap

## [0.5.0] - 2025-05-01
### Added
- Successfully ran and tested the agent script connecting to the MCP server
- Added `fastembed` dependency to requirements.txt
- Fixed MCP endpoint URL in agent_script.py to connect properly
- Validated end-to-end flow from agent to FastAPI backend via MCP
### Fixed
- Modified agent endpoint URL from "/mcp/sse" to "/mcp" to correctly connect to the MCP server

## [0.6.0] - 2025-05-01
### Added
- Authentication system with API key verification
- Added `backend/auth.py` with dependencies for API key validation
- Updated database layer to use PostgreSQL with environment variable configuration
- Added database initialization on app startup
- Modified endpoints to use real database instead of in-memory data
- Added Dockerfiles and docker-compose.yml for containerization
- Updated Build_Plan.md to mark all tasks as complete

### Changed
- Improved agent script error handling and logging
- Modified database connection to fallback to SQLite for development

## [0.6.1] - 2025-05-01
### Fixed
- Fixed authentication between agent and backend using the standard Bearer token approach
- Updated the FastAPI auth middleware to properly handle Authorization header with Bearer token
- Improved agent configuration to properly pass authentication headers to the MCP server
- Successfully tested end-to-end communication with authentication

## [0.7.0] - 2025-05-01
### Added
- Introduced a new section in Build_Plan.md detailing an ecommerce project with a ReactJS/Tailwind/shadcn frontend, AI agent integration, and admin portal.
- Outlined future enhancements including personalized recommendations and extensive product management features.

## [2025-05-02 00:55:39-04:00] Test Procedure and Results
- Executed backend tests using pytest on the FastAPI backend integrated with PostgreSQL.
- Resolved dependency override issues by refactoring the conftest.py override and updating the admin endpoint in main.py to use the injected session.
- Implemented a dependency override that creates a fresh engine and session per request to ensure proper event loop usage.
- All tests passed successfully.

## [0.8.0] - 2025-05-02
### Added
- Updated database fixture in tests to drop all tables before tests run.
- Configured engine with NullPool and future=True in tests to avoid connection concurrency issues.
- Modified the admin_create_product and user registration endpoints to fetch committed objects using session.get, resolving concurrent operation errors.
- All tests are now passing successfully.

### Next Task
- Implement a user logout endpoint, ensuring that users can invalidate their JWT tokens (if applicable) or end their session securely.
