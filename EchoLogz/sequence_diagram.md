```mermaid
sequenceDiagram
  autonumber
  participant Client
  participant App as FastAPI app (backend/main.py)
  participant Router as Endpoint (backend/routers/*.py)
  participant Deps as get_db() (db_session.py)
  participant CRUD as db_crud.py
  participant DB as Session/Engine (db_session.py)
  participant Models as ORM (db_schemas.py)
  participant Schemas as Pydantic (db_validation.py)

  Client->>App: HTTP /users
  App->>Router: route dispatch
  Router->>Schemas: validate request (Pydantic)
  Router->>Deps: Depends(get_db) → SessionLocal()
  Deps-->>Router: db session
  Router->>CRUD: create/get/update(...)
  CRUD->>Models: build/query ORM objects
  CRUD->>DB: add/commit/query
  DB-->>CRUD: rows / commit result
  CRUD-->>Router: domain objects
  Router->>Schemas: serialize response
  Router-->>Client: JSON
  Deps-->>DB: finally: close()
```

```mermaid
sequenceDiagram
  autonumber
  participant FE as Frontend
  participant SPOTR as routers/spotify_auth.py
  participant CALLS as services/spotify_calls.py
  participant DB as echoDB (tokens table via db_crud)

  FE->>SPOTR: GET /auth/spotify/login
  SPOTR-->>FE: 302 → Spotify authorize URL

  FE->>SPOTIFY: user consents
  SPOTIFY-->>SPOTR: redirect /auth/spotify/callback?code=...

  SPOTR->>CALLS: exchange_code_for_tokens(code)
  CALLS-->>SPOTR: access_token, refresh_token, expires_at
  SPOTR->>DB: persist tokens (via db_crud)
  SPOTR-->>FE: 200/login OK

  FE->>SPOTR: GET /auth/me (optional)
  SPOTR->>CALLS: get_user_profile(access_token)
  CALLS-->>SPOTR: profile JSON
  SPOTR-->>FE: profile JSON
  ```
