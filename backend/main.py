"""FastAPI backend exposing product retrieval tools via fastapi-mcp.
Run with:
    uvicorn backend.main:app --reload
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mcp import FastApiMCP

app = FastAPI(title="E-commerce Backend PoC", version="0.1.0")

# Allow local agent & browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# In-memory product catalogue (replace with DB later)
# ---------------------------------------------------------------------------
products_db = {
    "1": {
        "id": "1",
        "name": "Awesome Gadget",
        "description": "Does cool stuff.",
        "price": 99.99,
        "url": "/products/1",
    },
    "2": {
        "id": "2",
        "name": "Super Widget",
        "description": "Makes life easier.",
        "price": 49.50,
        "url": "/products/2",
    },
}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def get_product_from_db(product_id: str):
    """Stub for database lookup (replace with actual DB query)."""
    return products_db.get(product_id)


def search_products_in_db(name_substring: str):
    """Very naive search – returns first product with substring match."""
    lowered = name_substring.lower()
    for product in products_db.values():
        if lowered in product["name"].lower():
            return product
    return None


# ---------------------------------------------------------------------------
# API endpoints (exposed as MCP tools)
# ---------------------------------------------------------------------------

@app.get("/products/{product_id}", operation_id="getProductById")
async def get_product(product_id: str):
    """Retrieve product details by ID."""
    product = get_product_from_db(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.get("/products/search", operation_id="searchProducts")
async def search_products(name: str):
    """Search for a product by (partial) name."""
    product = search_products_in_db(name)
    if product is None:
        raise HTTPException(status_code=404, detail=f"Product '{name}' not found")
    return product


# ---------------------------------------------------------------------------
# fastapi-mcp integration – expose above endpoints as tools
# ---------------------------------------------------------------------------

mcp = FastApiMCP(app)
# This will mount endpoints under /mcp (REST) and /mcp/sse (SSE)
mcp.mount()

if __name__ == "__main__":  # dev helper: `python backend/main.py`
    import uvicorn
    uvicorn.run("backend.main:app", reload=True)
