# Resonote
Resonote (Research + Note + Resonance) is a research-focused, modular reading and reflection data-agnostic system designed to help you build intentional and critical reading habits, retain insights, and connect ideas across any field. Resonote encourages critical engagement by combining content ingestion, thoughtful curation, structured indexing, and lightweight reflection — with support for future expansion into knowledge graphs and external integrations. It will serve users to build effective, consistent reading habits and enhance memory, accuracy, and critical thinking.

Tech: Built with a **Flask backend** and **React/Vite frontend**, Resonote focuses on transparency, personalization, and long-term learning across any knowledge domain.

---

## Core Features

- Modular ingestion (web, PDFs, feeds, etc.)
- Smart filtering and deduplication
- Indexing for search and retrieval
- Reflection tools (summarization, prompting, spaced repetition)
- Personalized tracking and insights - Mind Map

---

## Project Breakdown

```bash
app/: Root application directory containing all backend logic and structure.

db/: Database layer with SQLAlchemy models, session setup, and schema init.

services/: Core backend services organized by domain (ingestion, curation, etc.).

ingestion/: Scrapers and ingestion logic for fetching metadata from external sources.

curation/: Cleans and extracts metadata (title, tags, read time).

routes/: Flask API route handlers for articles, ingestion, and status updates.

main.py: Flask app factory that initializes routes and app config.

run.py: Entry point to start the Flask API server (python run.py).

pipeline_run.py: Script to run ingestion + curation pipeline manually for testing.

```

---
## Overall Data Flow Architecture

                         +-----------------------+
                         |    Ingestion Layer    |
                         |-----------------------|
                         | RedditScraper         |
                         | ReutersScraper        |
                         +-----------+-----------+
                                     |
                                     v
                         +-----------------------+
                         |    Curation Engine     |
                         |-----------------------|
                         | Clean HTML             |
                         | Extract Metadata       |
                         | Estimate Read Time     |
                         +-----------+-----------+
                                     |
                                     v
                         +------------------------+
                         |      Indexing & DB     |
                         |------------------------|
                         | AWS RDS (MySQL)        |
                         | CuratedArticle table   |
                         +-----------+------------+
                                     |
                                     v
                      +-----------------------------+
                      |        Flask API Server      |
                      |-----------------------------|
                      | /api/articles                |
                      | /api/articles/:id/mark-read  |
                      | /api/articles/:id/favorite   |
                      +-----------------------------+
                                     |
                                     v
                          (Coming Soon: React UI)

---

## Backend Setup

Initialize DB (one-time): `python backend/init_db.py`

Run the Ingestion & Curation Pipeline: `python backend/pipeline_run.py`

Start API Server: `python backend/run.py`

```bash
cd backend

python3 -m venv venv
source venv/bin/activate

pip3 install -r requirements.txt

python3 run.py
```

Visit: http://localhost:5000/api

Run tests: `PYTHONPATH=backend pytest -v`

---


## Frontend Setup

React + Vite
```bash
npm run dev
```

Visit: http://localhost:5173

---

## Running Tests

Example curl commands:
```bash
# Resonote API — Usage Examples

## General

### GET: Hello World check (routing test)
curl http://localhost:5000/api/hello

### GET: Welcome message with list of available endpoints
curl http://localhost:5000/api/

---

## Ingestion + Storage Endpoints (writes to DB)

# Ingest from Reddit (default: r/news)
curl -X POST http://localhost:5000/api/ingest/reddit

# Ingest from r/technology
curl -X POST "http://localhost:5000/api/ingest/reddit?subreddit=technology"

# Ingest from r/health
curl -X POST "http://localhost:5000/api/ingest/reddit?subreddit=health"

# Ingest from r/worldnews with 10 articles
curl -X POST "http://localhost:5000/api/ingest/reddit?subreddit=worldnews&max_count=10"

# Ingest from r/science with headless scraping disabled (if used internally)
curl -X POST "http://localhost:5000/api/ingest/reddit?subreddit=science&headless=false"

# Ingest from The Guardian -- Default: section=news
curl -X POST http://localhost:5000/api/ingest/guardian

# Specific section and query
curl -X POST "http://localhost:5000/api/ingest/guardian?section=technology"

# Increase max_count
curl -X POST "http://localhost:5000/api/ingest/guardian?section=world&max_count=10"


---

## Article Indexing

### GET: Fetch the latest 25 articles (default limit)
curl http://localhost:5000/api/articles

### GET: Filter articles by source
curl "http://localhost:5000/api/articles?source=Reuters"

### GET: Filter articles by reading status
curl "http://localhost:5000/api/articles?status=unread"

### GET: Filter articles by favorite status
curl "http://localhost:5000/api/articles?favorite=true"

### GET: Filter articles by tag substring (case-insensitive match)
curl "http://localhost:5000/api/articles?tag=lifestyle"

### GET: Pagination — fetch next set of results
curl "http://localhost:5000/api/articles?limit=5&offset=5"

---

## Tag Analytics

### GET: Get a list of all tags with frequency counts
curl http://localhost:5000/api/tags

---

## Reflection System

### GET: Get reflection for a specific article
curl http://localhost:5000/api/reflect/fetch/2

### POST: Make a new reflection for an article
curl -X POST http://localhost:5000/api/reflect/make/2 \
  -H "Content-Type: application/json" \
  -d '{"content": "This article made me rethink my assumptions about a subject."}'

### POST: Update existing reflection for an article
curl -X POST http://localhost:5000/api/reflect/update/2 \
  -H "Content-Type: application/json" \
  -d '{"content": "Updated reflection — even more convinced about the implications now."}'

---

## Article Status Updates

### POST: Mark an article as "read"
curl -X POST http://localhost:5000/api/articles/1/mark-read

### POST: Toggle an article's favorite status
curl -X POST http://localhost:5000/api/articles/1/favorite


```