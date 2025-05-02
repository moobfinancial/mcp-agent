# Build Plan for MCP FastAPI PoC

> Created: 2025-05-01

This build plan breaks the PoC into incremental tasks with check-boxes so we can tick items off as work is completed.

- [x] **1. Create initial repository structure**
  - `/backend` FastAPI server
  - `/agent` standalone agent script
  - Support files: `requirements.txt`, `README.md`, `Build_Plan.md`, `changelog.md`

- [x] **2. Dependency management**
  - Populate `requirements.txt` with all packages required for backend & agent
  - (Optional) set up `pip-tools` / Poetry later

- [x] **3. FastAPI backend**
  - Implement `main.py` with sample in-memory product data
  - Add endpoints:
    - `GET /products/{product_id}` (`operation_id = getProductById`)
    - `GET /products/search?name=` (`operation_id = searchProducts`)

- [x] **4. Integrate fastapi-mcp**
  - Add `FastApiMCP(app).mount()` after endpoint definitions
  - Confirm MCP server reachable at `/mcp` & SSE at `/mcp/sse`

- [x] **5. Database layer (placeholder)**
  - Stub Postgres connection using SQLAlchemy
  - Replace in-memory store when ready

- [x] **6. Agent script**
  - `agent_script.py` using `mcp-use` & an LLM (OpenAI GPT-4o)
  - Reads `.env` for API keys
  - Connects to local MCP server and queries product tool

- [x] **7. Testing & validation**
  - Run backend with `uvicorn` and agent script; verify successful tool call
  - Add authentication dependency and show 401 failure scenario

- [x] **8. Documentation / README updates**
  - Explain local setup, running backend, running agent, env vars

- [x] **9. Prepare for deployment (stretch goal)**
  - Containerize backend, CI pipeline, hosting

- [x] **10. Authentication (critical feature)**
  - Implement proper authentication between agent and MCP server
  - Use standard Bearer token approach as recommended in MCP documentation
  - Successfully tested end-to-end communication with authentication

---

_Note: Tick the boxes when tasks are finished. If the file grows too large, create `Build_Plan_v2.md` etc._
