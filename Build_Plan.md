# Build Plan for MCP FastAPI PoC

> Created: 2025-05-01

This build plan breaks the PoC into incremental tasks with check-boxes so we can tick items off as work is completed.

## MCP Integration (Completed)

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

## Ecommerce Backend MVP (Current Focus)

### Completed Features (as of 2025-05-02)

- [x] **Database Models**
  - User model with authentication fields
  - Product model with basic e-commerce attributes
  - Database migrations and seeding functionality

- [x] **Authentication System**
  - [x] User registration endpoint with validation
  - [x] User login endpoint with JWT token generation
  - [x] User logout endpoint with token revocation
  - [x] Token validation middleware
  - [x] Authentication fixes for proper token handling
  - [x] Fixed user lookup by username in token validation

- [x] **Product Management**
  - [x] Product retrieval endpoint
  - [x] Product creation endpoint (admin only)

- [x] **Testing**
  - [x] Test database setup and teardown
  - [x] User registration tests (handling duplicate users)
  - [x] User login tests
  - [x] Product retrieval tests (updated to check for seeded products)
  - [x] Product creation tests

### In Progress

- [x] **User Profile Management**
  - [x] GET user profile endpoint
  - [x] PUT update user profile endpoint
  - [X] Complete testing of profile endpoints

### Outstanding Features for MV

- [x] **Order Management**
  - [x] Create order endpoint
  - [x] Retrieve user orders endpoint
  - [x] Update order status endpoint
  - [x] Tests for order functionality

- [x] **Shopping Cart**
  - [x] Add to cart endpoint
  - [x] View cart endpoint
  - [x] Update cart items endpoint
  - [x] Remove from cart endpoint
  - [x] Tests for cart functionality

- [x] **Enhanced Error Handling**
  - [x] Standardized error responses
  - [x] Proper validation error messages
  - [x] Logging system for errors

- [ ] **Documentation**
  - [ ] API documentation with Swagger UI
  - [ ] Update README with setup instructions
  - [ ] Document authentication flow

## Documentation Update [2025-05-02T03:03:03-04:00]
- Order Management endpoints (create, retrieve, update orders) successfully implemented and tested.
- Documentation updated accordingly.
- Next step: Implement Shopping Cart functionality.

## Frontend Integration (Future)

**Overview:**
- ReactJS frontend set up using Vite and Tailwind CSS with a modern wholesale-focused UI branded as "Resort Accessories".

**Completed:**
- Basic frontend project structure set up.
- Modern UI with responsive design for desktop and mobile.
- Branded as "Resort Accessories" with wholesale vacation accessories and jewelry focus.
- Created component structure with routes for all major features (Home, Products, Product Detail, Cart, Orders, Login, Register, Profile).
- Implemented mock product data with wholesale pricing tiers and minimum order quantities.
- Added professional homepage with hero section, featured collections, and wholesale benefits.

**Planned:**
- Integrate an AI speech agent for voice-based product search and recommendations.
- Build an admin portal with secure authentication for site management.
- Connect frontend components to backend API endpoints.

## API & Database Integration (Reference)

**Backend Endpoints:**
- [x] `POST /api/auth/register` - Register a new user
- [x] `POST /api/auth/login` - Login a user and get access token
- [x] `POST /api/auth/logout` - Logout a user and revoke token
- [x] `GET /api/user/profile` - Get current user profile
- [x] `PUT /api/user/profile` - Update user profile
- [x] `GET /api/products` - Retrieve a list of products
- [x] `POST /api/products` - Create a new product (admin only)
- [x] `GET /api/products/{id}` - Retrieve detailed information for a specific product
- [x] `POST /api/orders` - Create a new order
- [x] `GET /api/orders` - Get user's orders
- [x] `GET /api/orders/{id}` - Get specific order details
- [x] `POST /api/cart` - Add item to cart
- [x] `GET /api/cart` - View cart contents
- [x] `PUT /api/cart/{item_id}` - Update cart item
- [x] `DELETE /api/cart/{item_id}` - Remove item from cart

## Development Progress Log

- [x] Initial project setup completed (04/28/2025)
- [x] Database models created and migrations run (04/29/2025)
- [x] Authentication endpoints implemented (04/30/2025)
- [x] Product endpoints implemented (05/01/2025)
- [x] Tests written for existing functionality (05/01/2025)
- [x] Tests re-run; further issues remain in user registration and login; investigation ongoing.
- [x] Implement user logout endpoint (Completed on 05/02/2025)
- [x] Fix authentication issues in get_current_user function (05/02/2025)
- [x] Update tests to handle duplicate users and verify token authentication (05/02/2025)

# Wholesale Tourist Products Platform - Comprehensive Build Plan

## Development Phases Overview

### Phase 1: Core Platform Development (Current Phase)
- [x] Project Setup and Environment Configuration
- [x] Database Design and Schema Implementation
+ [x] MCP Server and Agent Integration (Critical Priority)
- [ ] Business Customer Management 
- [ ] E-commerce Features (In Progress)
- [x] Product Management
- [ ] Order Processing (Not Started)

### Phase 2: Admin Portal Development (Next Phase)
- [ ] AI-Powered Inventory Management (In Progress)
- [ ] Smart Product Cataloging (In Progress)
- [ ] Mobile/Tablet Integration (Not Started)
- [ ] Business Intelligence Dashboard (Not Started)
- [ ] AI-Powered Product Management (Not Started)

### Phase 3: AI Integration (Future)
- [ ] Multi-modal LLM Integration (Not Started)

### Phase 4: Advanced Features (Future)
- [x] Frontend Enhancements (Completed)
- [ ] API Endpoints Expansion (Not Started)
- [ ] External System Integrations (Not Started)

## Detailed Feature Checklist with Required Endpoints

### Core Platform Features

+ #### 0. MCP Server and Agent Integration (Critical Priority)
+ - [x] MCP server setup and configuration
+ - [x] Agent authentication with Bearer token
+ - [x] End-to-end communication testing
+ - [x] Environment variable configuration
+ - [ ] Production deployment of MCP server
+ - [ ] Enhanced error handling for MCP communication
+ - [ ] Scaling strategy for multiple concurrent agents
+ 
+ **Required Endpoints:**
+ - [x] `POST /api/mcp/agent/auth` - Authenticate agent with MCP server
+ - [x] `POST /api/mcp/query` - Send query to MCP server
+ - [ ] `GET /api/mcp/status` - Check MCP server status
+ - [ ] `POST /api/mcp/feedback` - Send feedback to improve MCP responses
+ - [ ] `GET /api/mcp/logs` - Retrieve MCP interaction logs

#### 1. Business Customer Management
- [x] Business customer registration
- [x] Document upload system (PDF, JPG, PNG)
- [x] Server-side validation
- [x] Secure file storage
- [x] Document review workflow
- [x] Automated verification status updates
- [x] Email notifications for verification status
- [x] Business profile management form
- [ ] Multi-location support

**Required Endpoints:**
- [x] `POST /api/auth/register` - Register a business customer
- [x] `POST /api/auth/login` - Login a business customer
- [x] `GET /api/business/profile` - Get business profile
- [x] `PUT /api/business/profile` - Update business profile
- [ ] `POST /api/business/documents` - Upload business documents
- [ ] `GET /api/business/documents` - Get business documents
- [ ] `GET /api/business/verification-status` - Check verification status
- [ ] `POST /api/business/locations` - Add business location
- [ ] `GET /api/business/locations` - Get business locations
- [ ] `PUT /api/business/locations/{id}` - Update business location

#### 2. Product Management
- [x] Category-based organization
- [x] Product variant management
- [ ] Bulk product upload
- [x] Inventory tracking
- [x] Stock level alerts
- [x] Wholesale descriptions
- [x] Availability status
- [x] Inventory reporting features
  - [x] Low stock reporting
  - [x] Inventory valuation
  - [x] Turnover analysis

**Required Endpoints:**
- [x] `GET /api/products` - Get all products
- [x] `POST /api/products` - Create a product
- [x] `GET /api/products/{id}` - Get product details
- [x] `PUT /api/products/{id}` - Update product
- [x] `DELETE /api/products/{id}` - Delete product
- [ ] `POST /api/products/bulk` - Bulk upload products
- [ ] `GET /api/categories` - Get product categories
- [ ] `POST /api/categories` - Create product category
- [ ] `GET /api/inventory/reports/low-stock` - Get low stock report
- [ ] `GET /api/inventory/reports/valuation` - Get inventory valuation
- [ ] `GET /api/inventory/reports/turnover` - Get turnover analysis

#### 3. E-commerce Features
- [x] Bulk pricing tiers
- [x] Minimum order quantities (MOQ)
- [x] Cross-linking to retail website
- [x] Wholesale pricing calculator
- [ ] Bulk order management

**Required Endpoints:**
- [x] `GET /api/products/{id}/pricing` - Get product pricing tiers
- [ ] `POST /api/calculator/wholesale` - Calculate wholesale pricing
- [ ] `GET /api/retail/links/{product_id}` - Get retail website links
- [ ] `POST /api/orders/bulk` - Create bulk order

#### 4. Order Processing
- [ ] Bulk order processing
- [ ] Business credit application
- [ ] Payment terms management
- [ ] Shipping calculation
- [ ] Order tracking
- [ ] Automated invoicing
- [ ] Return/refund management

**Required Endpoints:**
- [x] `POST /api/orders` - Create order
- [x] `GET /api/orders` - Get all orders
- [x] `GET /api/orders/{id}` - Get order details
- [ ] `PUT /api/orders/{id}` - Update order
- [ ] `POST /api/credit/applications` - Submit credit application
- [ ] `GET /api/credit/applications/{id}` - Get credit application status
- [ ] `GET /api/payment/terms` - Get payment terms
- [ ] `POST /api/shipping/calculate` - Calculate shipping
- [ ] `GET /api/orders/{id}/tracking` - Get order tracking
- [ ] `GET /api/invoices/{order_id}` - Get invoice
- [ ] `POST /api/returns` - Create return request
- [ ] `GET /api/returns/{id}` - Get return status

### Admin Portal Features

#### 1. AI-Powered Inventory Management
- [x] Image analysis capabilities
- [x] Automated description generation
- [x] Category recommendation
- [x] Product attribute extraction
- [x] Bulk image processing

**Required Endpoints:**
- [ ] `POST /api/ai/analyze-image` - Analyze product image
- [ ] `POST /api/ai/generate-description` - Generate product description
- [ ] `POST /api/ai/recommend-category` - Get category recommendations
- [ ] `POST /api/ai/extract-attributes` - Extract product attributes
- [ ] `POST /api/ai/process-images/bulk` - Process multiple images

#### 2. Smart Product Cataloging
- [x] Category prediction
- [x] Batch processing
- [x] Admin approval workflow
  - [ ] Status field in products table
  - [ ] API endpoints for status management
  - [ ] Product review UI
  - [ ] Status transition logic
- [ ] Bulk category assignment
- [ ] Smart tagging system

**Required Endpoints:**
- [ ] `POST /api/products/status/{id}` - Update product status
- [ ] `GET /api/products/pending-review` - Get products pending review
- [ ] `POST /api/products/bulk-categorize` - Assign categories in bulk
- [ ] `POST /api/products/tags` - Add tags to product
- [ ] `GET /api/products/tags` - Get product tags

#### 3. Business Intelligence
- [ ] Customer analytics
- [ ] Inventory analytics
- [ ] Sales analytics

**Required Endpoints:**
- [ ] `GET /api/analytics/customers` - Get customer analytics
- [ ] `GET /api/analytics/inventory` - Get inventory analytics
- [ ] `GET /api/analytics/sales` - Get sales analytics
- [ ] `GET /api/analytics/dashboard` - Get dashboard metrics

#### 4. Supplier Management (New)
- [ ] Suppliers table schema
- [ ] Supplier CRUD operations
- [ ] Product-supplier association
- [ ] Supplier cost tracking
- [ ] Initial purchase quantity tracking

**Required Endpoints:**
- [ ] `GET /api/suppliers` - Get all suppliers
- [ ] `POST /api/suppliers` - Create supplier
- [ ] `GET /api/suppliers/{id}` - Get supplier details
- [ ] `PUT /api/suppliers/{id}` - Update supplier
- [ ] `DELETE /api/suppliers/{id}` - Delete supplier
- [ ] `POST /api/suppliers/{id}/products` - Associate product with supplier
- [ ] `GET /api/suppliers/{id}/products` - Get supplier products
- [ ] `POST /api/suppliers/costs` - Add supplier cost
- [ ] `GET /api/suppliers/costs` - Get supplier costs

#### 5. User Management (Enhanced)
- [ ] Super admin role
- [ ] Granular permissions
- [ ] Role-based access control

**Required Endpoints:**
- [ ] `GET /api/admin/users` - Get all users
- [ ] `POST /api/admin/users` - Create user
- [ ] `GET /api/admin/users/{id}` - Get user details
- [ ] `PUT /api/admin/users/{id}` - Update user
- [ ] `DELETE /api/admin/users/{id}` - Delete user
- [ ] `GET /api/admin/roles` - Get all roles
- [ ] `POST /api/admin/roles` - Create role
- [ ] `PUT /api/admin/roles/{id}` - Update role
- [ ] `GET /api/admin/permissions` - Get all permissions
- [ ] `POST /api/admin/permissions` - Assign permissions to role

## Next Priority Tasks

+ 1. **MCP Server and Agent Integration** (Highest Priority)
+    - Ensure robust MCP server deployment for production
+    - Implement enhanced error handling for MCP communication
+    - Develop scaling strategy for multiple concurrent agents
+    - Create monitoring and logging system for MCP interactions
1. Complete document review workflow for business verification
2. Implement bulk product upload functionality
3. Develop order processing system
4. Build admin approval workflow for products (Current focus)
   - Status management API
   - Product review UI
   - Approval notifications
5. Create business intelligence dashboard
6. Implement supplier management
   - Database schema
   - Admin UI
   - Product associations
7. Add super admin role and permissions

## MCP Integration Roadmap

### Current Status (as of 2025-05-02)

- MCP server and agent communication successfully tested in POC
- Basic endpoints created and tested with database
- Frontend UI developed for Resort Accessories wholesale platform
- Virtual environment configured for development

### Integration Phases

### Phase 1: Endpoint-to-MCP Integration (Immediate Priority - Next 2 Weeks)

1. **Week 1: MCP Agent Configuration for API Endpoints**
   - Create MCP agent configuration file that maps intents to API endpoints
   - Implement middleware to handle authentication between MCP and API endpoints
   - Develop response formatters to standardize API responses for MCP consumption
   - Test basic CRUD operations through MCP agent

2. **Week 2: Database Integration with MCP Queries**
   - Extend MCP agent to handle complex database queries
   - Implement caching layer for frequently accessed data
   - Create data validation layer between MCP requests and database operations
   - Set up error handling and logging for database operations triggered by MCP

### Phase 2: Chatbot Integration (Weeks 3-4)

1. **Week 3: Text-Based Chatbot Development**
   - Integrate MCP agent with frontend chat interface
   - Implement session management for chat conversations
   - Develop context-aware responses based on user history
   - Create specialized handlers for product inquiries, order status, and account management

2. **Week 4: Advanced Chatbot Features**
   - Implement product recommendation system through chatbot
   - Add natural language processing for order placement
   - Create chatbot analytics dashboard
   - Develop A/B testing framework for chatbot responses

### Phase 3: Voice Bot Integration (Weeks 5-8)

1. **Week 5-6: Voice Recognition Setup**
   - Integrate speech-to-text API with frontend
   - Implement voice input component in React
   - Develop voice command parser for common wholesale operations
   - Create voice signature verification for secure operations

2. **Week 7-8: Voice Response System**
   - Implement text-to-speech for chatbot responses
   - Develop voice tone and style guidelines
   - Create voice response templates for different scenarios
   - Test and optimize voice interaction flow

### Implementation Details

### Environment Setup

1. **Development Environment**
   - Continue using virtual environment for consistency
   - Implement Docker containers for MCP server and API services
   - Set up CI/CD pipeline for automated testing and deployment
   - Create separate environments for development, staging, and production

2. **Production Environment**
   - Deploy MCP server to cloud provider with auto-scaling
   - Set up load balancing for API endpoints
   - Implement database replication for high availability
   - Configure monitoring and alerting for all components

### Integration Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Frontend   │◄────┤  MCP Agent  │◄────┤  MCP Server │
│  (React)    │     │  (Gateway)  │     │             │
└──────┬──────┘     └──────┬──────┘     └─────────────┘
        │                   │
        │                   │
┌──────▼──────┐     ┌──────▼──────┐     ┌─────────────┐
│  Chat/Voice │     │ API Endpoints│◄────┤  Database   │
│  Interface  │     │ (FastAPI)    │     │  (Postgres) │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Key Dependencies and Requirements

1. **Technical Dependencies**
   - MCP server version 2.0 or higher
   - FastAPI 0.95+ for API endpoints
   - PostgreSQL 14+ for database
   - React 18+ for frontend
   - WebSockets for real-time chat
   - Web Speech API for voice recognition (browser-based)
   - Cloud Text-to-Speech API for voice responses

2. **Development Requirements**
   - Update virtual environment with all required packages
   - Ensure all developers have access to MCP documentation
   - Set up shared testing environment for MCP integration
   - Establish code review process for MCP-related changes

### Timeline and Milestones

| Milestone | Target Date | Deliverables |
|-----------|-------------|--------------|
| MCP-API Integration | 2025-05-16 | MCP agent configured for API endpoints, database integration |
| Chatbot Launch | 2025-05-30 | Functional text chatbot with product and order capabilities |
| Voice Bot Beta | 2025-06-13 | Basic voice recognition and response system |
| Voice Bot Release | 2025-06-27 | Full voice interaction system with all planned features |

### Success Metrics

1. **Technical Metrics**
   - MCP response time < 200ms for API queries
   - 99.9% uptime for MCP server
   - < 5% error rate on voice recognition
   - Database query optimization reducing load times by 30%

2. **Business Metrics**
   - 50% reduction in customer service inquiries
   - 25% increase in wholesale order completion rate
   - 40% of users adopting voice interface within 3 months
   - 15% increase in average order value through recommendations

### Next Steps (Immediate Actions)

1. Review and update virtual environment configuration
2. Create MCP agent configuration file for existing API endpoints
3. Implement authentication middleware for MCP-API communication
4. Set up development environment for chatbot testing
5. Schedule team training session on MCP integration

This roadmap will be reviewed and updated weekly to reflect progress and any changes in requirements or priorities.

## Dependencies
+ - MCP server and authentication system (Critical)
- Gemini API for AI features
- Retail website API integration
- Payment gateway integration (Planned)
- Accounting software integration (Future)
- CRM system integration (Future)
- Inventory management system (Future)

## Risk Assessment
1. AI integration complexity - Medium risk
2. Performance at scale - High risk
3. Third-party API reliability - Medium risk
4. Data migration requirements - Low risk

## Changelog

**2025-05-02**
+ - Added MCP server and agent integration as critical priority component
- Updated frontend with modern UI branded as "Resort Accessories"
- Completed all basic cart endpoints
- Added comprehensive build plan with detailed feature checklist and required endpoints
- Frontend now features wholesale-focused product listings with pricing tiers and MOQs

**2025-05-01**
- Implemented product endpoints
- Created tests for existing functionality

**2025-04-30**
- Implemented authentication endpoints

**2025-04-29**
- Created database models and ran migrations

**2025-04-28**
- Completed initial project setup
