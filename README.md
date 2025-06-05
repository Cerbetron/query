# Query Demo App

This repository contains a small demo application composed of a FastAPI backend and a React frontend.

## Development

- `docker-compose up --build` will start PostgreSQL, ChromaDB, the API and the React app.
- The API is available at `http://localhost:8000` and the React app at `http://localhost:3000`.

The backend exposes a `/search` endpoint that supports the following fields:

- `keyword` – free text search over name, description and eligibility
- `age` – integer to filter resources within the age range
- `county` – one of the counties configured in the sample data
- `insurance` – insurance type
- `system` – list of systems
- `tags` – list of tags

## Data

For demonstration purposes the API serves a handful of in-memory resources. The Excel loader and Chroma integration utilities are provided but not wired to the demo data.

During startup the demo records are automatically indexed into Chroma. Keyword
queries will use the vector index to rank results. You can load your own data
via the utilities in `app/utils` and index them with `index_resources`.
