+++
title = "Standardizing Civic Data APIs with Protobuf and ConnectRPC"
date = 2026-08-24
description = "How civican-schemas and civican-server use Protocol Buffers and ConnectRPC to build contract-first, browser-friendly APIs for Canadian parliamentary and lobbying data."
[taxonomies]
tags = ["api", "protobuf", "connectrpc", "python", "civic-tech", "open-source"]
+++

Access to public civic data—such as parliamentary legislation and federal lobbying activity—is essential for democratic transparency. However, for software engineers and data analysts, working with government data sources often presents significant friction: data formats are fragmented, APIs are either inconsistent or non-existent, and data models lack standardized contracts.

In the [Civican](https://github.com/civican) project, we set out to solve this problem by taking a **contract-first API design** approach.

By centralizing data models in `civican-schemas` using **Protocol Buffers (Protobuf)** and serving them via **ConnectRPC** in `civican-server`, we created a unified, type-safe API ecosystem powering data pipelines for both [LEGISinfo](https://github.com/civican/legisinfo) (parliamentary bills and proceedings) and [Lobby Canada](https://github.com/civican/lobbycanada) (federal lobbying registrations and communications).

Here is a deep dive into why this architecture works, why ConnectRPC is a perfect fit, and how the components connect.

---

## The Contract-First Mindset: `civican-schemas`

In traditional civic scraper and API projects, backend services often evolve ad-hoc: a scraper writes to SQLite or Postgres, a REST framework (like FastAPI or Flask) exposes custom JSON dictionaries, and frontend clients end up reverse-engineering field names and nullable types.

With **`civican-schemas`**, the schema is the single source of truth across all tools:

```
                  ┌─────────────────────────────────┐
                  │         civican-schemas         │
                  │   (.proto files + Buf toolchain)│
                  └───────────────┬─────────────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         ▼                        ▼                        ▼
  Python Dataclasses      ConnectRPC Stubs        Protobuf-to-Pydantic
   (Type Safety)        (ASGI Service Base)        (OpenAPI Schemas)
         │                        │                        │
         └────────────────────────┼────────────────────────┘
                                  ▼
                  ┌─────────────────────────────────┐
                  │         civican-server          │
                  │ (Unified ConnectRPC/FastAPI API)│
                  └───────────────┬─────────────────┘
                                  │
                 ┌────────────────┴────────────────┐
                 ▼                                 ▼
         /legisinfo.v1.*                   /lobbycanada.v1.*
      (Parliamentary Bills)             (Lobbying Communications)
```

We use **[Buf](https://buf.build)** to manage, lint, and compile our Protocol Buffers. Our `buf.gen.yaml` configures multiple generation plugins simultaneously:

```yaml
version: v1
plugins:
  - plugin: buf.build/protocolbuffers/python:v25.2
    out: src
  - plugin: buf.build/protocolbuffers/pyi:v25.2
    out: src
  - plugin: buf.build/connectrpc/python:v0.10.1
    out: src
  - plugin: protobuf-to-pydantic
    out: src
```

This single build step produces:

1. Standard Python Protobuf message definitions.
2. Static type hints (`.pyi`) for IDE autocomplete and type checkers (`mypy`/`pyright`).
3. ConnectRPC asynchronous server & client stubs.
4. Pydantic validation models for seamless OpenAPI/Swagger generation.

---

## Composing Cross-Domain Civic Entities

One of the biggest advantages of Protobuf is clean cross-package imports and schema composition.

For instance, lobbying and legislation are deeply interconnected: lobbyists register to influence specific parliamentary bills. In `lobbycanada.v1.lobbycanada.proto`, we can directly import the bill schema from `legisinfo.v1`:

```proto
syntax = "proto3";

package lobbycanada.v1;

import "civican/schemas/proto/legisinfo/v1/legisinfo.proto";

service LobbyCanadaService {
  rpc ListRegistrations(ListRegistrationsRequest) returns (ListRegistrationsResponse);
  rpc GetRegistration(GetRegistrationRequest) returns (GetRegistrationResponse);
  rpc ListCommunications(ListCommunicationsRequest) returns (ListCommunicationsResponse);
  rpc CrossReferenceBill(CrossReferenceBillRequest) returns (CrossReferenceBillResponse);
  rpc GetTopLobbiedBills(GetTopLobbiedBillsRequest) returns (GetTopLobbiedBillsResponse);
}

message CrossReferenceBillRequest {
  string bill_number = 1;
  string session = 2;
  int32 limit = 3;
}

message CrossReferenceBillResponse {
  string target_bill = 1;
  legisinfo.v1.BillDetail bill_details = 2;   // Reused directly from LEGISinfo schema
  repeated LobbyRegistration registrations = 3;
  int32 total_registrations_count = 4;
  repeated LobbyCommunication communications = 5;
  int32 total_communications_count = 6;
}
```

Notice `bill_details` in `CrossReferenceBillResponse`: rather than duplicating bill metadata fields or treating it as an untyped JSON blob, the API guarantees that bill structures are 100% identical whether fetched directly from `LegisinfoService` or cross-referenced through `LobbyCanadaService`.

---

## Why ConnectRPC?

Historically, choosing Protocol Buffers meant committing to standard **gRPC**. While gRPC is outstanding for internal backend-to-backend communication over HTTP/2, it has notorious drawbacks for public APIs:

- Browsers cannot call gRPC endpoints natively without an intermediate proxy like Envoy (`grpc-web`).
- Standard developer tools like `curl` cannot easily inspect or invoke endpoints.
- Debugging binary wire payloads requires specialized tooling.

**[ConnectRPC](https://connectrpc.com/)** solves this fundamentally:

1. **Multi-Protocol Support:** A single ConnectRPC handler automatically accepts:
   - **Connect protocol** (HTTP POST with JSON or Protobuf)
   - **gRPC-Web** (browser-compatible gRPC)
   - **Standard gRPC** (HTTP/2 binary)
2. **Curl & Browser Friendly:** You can call any ConnectRPC endpoint with regular `curl` sending JSON headers:
   ```bash
   curl -X POST http://localhost:8000/lobbycanada.v1.LobbyCanadaService/GetTopLobbiedBills \
     -H "Content-Type: application/json" \
     -d '{"limit": 5}'
   ```
3. **No Envoy Proxy Required:** The Python ASGI application parses HTTP/1.1 and HTTP/2 requests directly in-process.

---

## Serving the API: `civican-server`

In **`civican-server`**, we mount the generated ConnectRPC applications inside a **FastAPI / Starlette** ASGI application.

We decouple the database readers from the RPC presentation layer using a clean Service-Reader pattern:

```python
from civican.schemas.proto.legisinfo.v1.legisinfo_connect import LegisinfoServiceASGIApplication
from civican.schemas.proto.lobbycanada.v1.lobbycanada_connect import LobbyCanadaServiceASGIApplication
from connectrpc.compat import google_protobuf_codecs
from fastapi import FastAPI
from civican.server.readers import LegisinfoReader, LobbyCanadaReader
from civican.server.services import LegisinfoServiceImpl, LobbyCanadaServiceImpl

# 1. Initialize Readers & Service Implementations
legisinfo_reader = LegisinfoReader()
legisinfo_servicer = LegisinfoServiceImpl(legisinfo_reader)

lobbycanada_reader = LobbyCanadaReader()
lobbycanada_servicer = LobbyCanadaServiceImpl(lobbycanada_reader)

# 2. Wrap with ConnectRPC ASGI Applications
codecs = google_protobuf_codecs()
legisinfo_app = LegisinfoServiceASGIApplication(legisinfo_servicer, codecs=codecs)
lobbycanada_app = LobbyCanadaServiceASGIApplication(lobbycanada_servicer, codecs=codecs)

# 3. Mount in FastAPI
app = FastAPI(title="CIVICAN API Server", version="0.1.0")
app.mount(legisinfo_app.path, ConnectASGIWrapper(legisinfo_app))
app.mount(lobbycanada_app.path, ConnectASGIWrapper(lobbycanada_app))
```

### Dynamic Service Activation

Civic datasets vary by deployment: a scraper repo may only contain lobbying data, a parliamentary repo may only contain bill JSONs, while a production unified portal contains both. `civican-server` inspects environment variables and dataset paths (`is_legisinfo_active()`, `is_lobbycanada_active()`) to dynamically mount only available services, exposing health and service discovery at `/health` and `/`.

---

## Data Repositories as Consumers: Ephemeral APIs with `uv` and Make

A central architectural goal was keeping data repositories like [`civican/lobbycanada`](https://github.com/civican/lobbycanada) and [`civican/legisinfo`](https://github.com/civican/legisinfo) strictly focused on data artifacts (DuckDB databases, scraped records, automated sync jobs) with **zero duplicated server boilerplate**.

Instead of writing a custom API server inside each data repo, the repositories declare `civican-server` and `civican-schemas` as **dynamic dependencies** executed on-the-fly.

In `lobbycanada/Makefile`, running the entire ConnectRPC API server is a single target:

```makefile
# Source definitions can point to sibling local directories or remote Git repos
CIVICAN_SERVER_SOURCE  ?= ../civican-server
CIVICAN_SCHEMAS_SOURCE ?= ../civican-schemas
PORT                   ?= 8001

run:
	LOBBYCANADA_DB_PATH=$$(pwd)/lobbycanada.duckdb uv run \
		--with duckdb \
		--with "civican-schemas @ file://$$(realpath $(CIVICAN_SCHEMAS_SOURCE))" \
		--with "civican-server @ file://$$(realpath $(CIVICAN_SERVER_SOURCE))" \
		-- uvicorn civican.server.main:app --host 0.0.0.0 --port $(PORT)
```

For remote consumers who don't have local checkouts of the server repo, `uv run` fetches the server package directly from Git:

```bash
LOBBYCANADA_DB_PATH=./lobbycanada.duckdb uv run \
  --with "civican-server @ git+https://github.com/civican/civican-server.git" \
  -- uvicorn civican.server.main:app --port 8001
```

### Why This Workflow Is Powerful

1. **One-Command Local Experience:** A contributor or data journalist can clone `lobbycanada`, download the latest pre-built DuckDB database, and immediately spin up a local API:
   ```bash
   make download   # Fetches latest compressed DuckDB release
   make run        # Ephemerally pulls civican-server and serves ConnectRPC API
   ```
2. **Zero Global Environment Pollution:** Using `uv run --with ...` spins up an ephemeral environment, boots Uvicorn, and cleans up automatically—without requiring `pip install` or managing virtual environments.
3. **Container Parity:** The same pattern is containerized via `make docker-run`, mounting local database files into the standard `civican-server` container for production Kubernetes or Fly.io deployments.

---

## Key Benefits & Looking Forward

By pairing **Protobuf schemas** with **ConnectRPC**:

- **Zero Drift:** Client libraries, documentation, and backend servers never fall out of sync.
- **Civic Transparency:** Connecting separate governmental registries into structured, queryable graphs allows answering real-world public interest questions—like _"Which organizations lobbied on Bill C-27 and when?"_—with a single typed RPC call.
- **AI & LLM Integration (MCP):** Structured Protobuf schemas allow direct projection into Model Context Protocol (MCP) servers (like `civican-mcp`), giving LLMs precise tool definitions to query civic data reliably without hallucinating API signatures.

All schemas and server implementations are open source on GitHub at [github.com/civican](https://github.com/civican).
