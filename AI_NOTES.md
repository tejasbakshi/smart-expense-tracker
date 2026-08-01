# AI Tools Usage

## Tools Used

- **ChatGPT / Claude** — Used for generating initial code scaffolding, suggesting architecture patterns, and drafting test cases.
- **GitHub Copilot** — Used inline during code writing for autocompletion and syntax suggestions.

---

## What Was AI-Generated vs. Written by Me

### AI-Generated (then reviewed and modified by me)

- Initial project structure suggestion (I restructured the layout)
- Pydantic model definitions (I adjusted field constraints and added the two-model pattern)
- Storage class boilerplate (I added thread safety and file persistence logic)
- Test case suggestions (I rewrote edge cases and added missing scenarios)

### Written Entirely by Me

- The decision to use FastAPI over Flask (I evaluated both and chose FastAPI for automatic OpenAPI docs)
- Error handling architecture (custom exception hierarchy with RFC 9457 vocabulary)
- Category normalization logic (`.lower().strip()` on both create and filter)
- Route ordering (`/expenses/totals` defined before `/expenses/{expense_id}` to prevent FastAPI path matching bug)
- Health check endpoint
- Thread safety implementation (Lock wrapping full read-modify-write cycle)
- All final decisions on what NOT to build

---

## What I Validated, Tested, or Changed

### Validated

- Every endpoint tested manually via curl against a running server before writing tests
- All 34 pytest tests verified passing in a clean virtual environment
- README commands tested from scratch (deactivate, delete venv, recreate, reinstall, run tests)
- Date serialization confirmed to produce ISO 8601 format (`"2026-08-01"`)
- Swagger UI at `/docs` confirmed to auto-document all endpoints

### Changed From AI Output

**1. Fixed URL encoding bug in tests**
- AI-generated test used raw URL string with `&` character (`?category=dining & drinks`)
- The `&` was parsed as a query parameter separator, causing test failure
- I changed to `params={"category": "dining & drinks"}` for proper URL encoding
- This was caught during the first test run (1 failure out of 34)

**2. Added thread safety to storage**
- AI's original storage implementation had no concurrency protection
- I recognized that FastAPI runs synchronous handlers in a threadpool (up to 40 threads)
- Added `threading.Lock` wrapping the entire read-modify-write cycle to prevent race conditions and data loss

**3. Added directory creation guarantee**
- AI's storage code assumed the `data/` directory exists
- On a fresh clone it does not, which causes `FileNotFoundError`
- I added `pathlib.Path.mkdir(parents=True, exist_ok=True)` before every write

**4. Chose standard library logging over structlog**
- AI recommended `structlog` for structured logging
- I evaluated it and decided stdlib `logging` with proper format configuration is sufficient
- For a single-process local server with 5 endpoints, a third-party logging dependency violates YAGNI
- Both produce readable terminal output; stdlib adds zero dependencies

**5. Simplified error format**
- AI initially suggested either bare `HTTPException` or full RFC 9457 Problem Details
- I chose a middle path: adopt RFC 9457 key vocabulary (`title`, `detail`, `status`) without the full spec
- No type URIs, no instance pointers — those serve external consumers that don't exist for this project

---

## AI Suggestions I Decided Not to Use

### 1. Correlation IDs and request tracing middleware

AI suggested generating a unique `X-Request-ID` for every request and including it in all log lines.

**Why I rejected it:** Correlation IDs solve the problem of tracing a request across multiple distributed services. This is a single-process server. Every log line is already correlated by being in the same process. Adding this would be solving a problem that does not exist.

### 2. Deep copies on all service layer return values

AI suggested calling `model_copy(deep=True)` on every Pydantic model returned from the service layer to prevent accidental mutation.

**Why I rejected it:** The service constructs new Pydantic model instances from stored dictionary data each time. These are already separate objects. The deep copy adds method calls defending against a threat the architecture already prevents.

### 3. Lifespan context manager for storage load/save

AI suggested using FastAPI's lifespan events to load data on startup and save on shutdown.

**Why I rejected it:** The storage layer already loads on initialization and saves after every mutation. A lifespan handler would add complexity for a benefit that does not exist in this design.

### 4. Pagination on the list endpoint

AI suggested cursor-based pagination for `GET /expenses`.

**Why I rejected it:** This is a personal expense tracker. A user will have hundreds of records at most. Pagination adds complexity to the service, router, and response format for a problem that does not exist in this context.

### 5. PATCH endpoint for updating expenses

AI suggested adding `PATCH /expenses/{id}` for completeness.

**Why I rejected it:** The assignment specifies five operations: add, view, filter, calculate totals, delete. Update is not one of them. Adding it increases the surface area for bugs without serving the requirements.

### 6. Docker support

AI suggested adding a Dockerfile and docker-compose.yml.

**Why I rejected it:** Not required by the assignment. Adds complexity for no functional benefit in a local evaluation.

---

## Summary

AI tools were used as a starting point for code generation and as a sounding board for architectural decisions. Every piece of AI-generated output was reviewed, tested, and modified before inclusion. The key architectural decisions — thread safety, route ordering, error format, category normalization, and the YAGNI rejections — were my own judgment calls made after evaluating AI suggestions against the project's actual constraints.
