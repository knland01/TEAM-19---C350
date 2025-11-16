```mermaid
flowchart LR
  classDef routers fill:#F8E6CD,stroke:#c29a5b,stroke-width:2px,color:#333
  classDef db fill:#CDEEBF,stroke:#30A930,stroke-width:2px,color:#333
  classDef frontend fill:#ABA2F3,stroke:#FF00FB,stroke-width:2px,color:#333
  classDef services fill:#F2C9EA,stroke:#F85BF8,stroke-width:2px,color:#333
  classDef core fill:#F5F3C2,stroke:#877C03,stroke-width:2px,color:#333
  classDef main fill:#F5F299,stroke:#E600FF,stroke-width:2px,color:#333
  classDef spotify fill:#010101,stroke:#0CA03B,stroke-width:2px,color:#F8F8F8
  style EXT fill:#272E30FF,stroke:#0CA03B,stroke-width:2px,color:#F8F8F8
  
  %% ================= Frontend =================
  subgraph FEgrp["Frontend"]
    direction TB
    FE[frontend/index.html<br/>frontend/style.css]:::frontend
  end

  %% ================= Backend =================
  subgraph BE["Backend"]
    direction TB

    %% ----- Core -----
    subgraph Core["FastAPI Core"]
      direction TB
      MAIN[main.py]:::main
      CFG["core/config.py<br/>(.env Vars)"]:::core
      DEPS["core/dependencies.py<br/>(get_db)"]:::core
    end
    
    %% ----- Services -----
    subgraph Services["EchoLogz Services"]
      direction TB
      CALLS["spot_calls.py"]:::services
      SCORE["score.py"]:::services
      UTIL["utils.py"]:::services
    end

    %% ----- DB Layer -----
    subgraph DBLayer["EchoDB – Data Layer"]
      direction LR
      %%AUTH["r_auth.py<br/>(EchoLogz JWT Auth)"]:::routers
      VAL["db_validation.py<br/>(Pydantic I/O)"]:::db
      CRUD["db_crud.py<br/>(DB operations)"]:::db
      SCHEMAS["db_schemas.py<br/>(SQLAlchemy ORM)"]:::db
      DBMOD["db_session.py<br/>(engine, SessionLocal, Base)"]:::db
      FILEDB[("echologz.db<br/>(SQLite → Postgres)")]:::db
    end

    

    %% ----- Routers -----
    subgraph Routers["Routers (HTTP Endpoints)"]
      direction TB
      ROUTERS{{"routers/*"}}:::routers
      SPOTAUTH["r_spot_auth.py<br/>(Spotify OAuth2)"]:::routers
      MATCH["r_match.py<br/>(calls score.py)"]:::routers
      USERS["r_users.py<br/>(CRUD)"]:::routers
      AUTH["r_auth.py<br/>(EchoLogz JWT Auth)"]:::routers
      STATUS["r_status.py<br/>(Status)"]:::routers
    end


  end
    %% ----- External -----
  subgraph EXT["External Services"]
    direction TB
    ACCOUNTS[(Spotify Accounts Service)]:::spotify
    WEBAPI[(Spotify Web API)]:::spotify
  end

  %% ========= Connections =========
  FE -->|HTTP requests| MAIN

  MAIN --> CFG
  MAIN --> ROUTERS
  MAIN --> DEPS

  %% Routers use deps + services
  ROUTERS --> SPOTAUTH
  ROUTERS --> AUTH
  ROUTERS --> MATCH
  ROUTERS --> USERS
  ROUTERS --> STATUS
  ROUTERS --> DEPS

  %% Router → Service
  SPOTAUTH --> CALLS
  MATCH --> SCORE
  

  %% Services → DB (through CRUD)
  SCORE --> CRUD
  %%SCORE --> UTIL
  CALLS --> VAL 
  %%CALLS --> UTIL 
  %% if you map Spotify payloads to Pydantic models (optional)

  %% DB flow
  AUTH --> VAL
  AUTH --> CRUD
  USERS --> VAL
  USERS --> CRUD
  CRUD --> SCHEMAS
  CRUD --> DBMOD
  SCHEMAS --> DBMOD
  DBMOD --> FILEDB

  %% OAuth exchange & API calls
  SPOTAUTH -->|Redirect → Spotify Login| ACCOUNTS
  ACCOUNTS -.->|Issues access_token| SPOTAUTH
  CALLS -->|GET playlists / <br/> audio features| WEBAPI
  ```