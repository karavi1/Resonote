# Resonote
Resonote (Research + Note + Resonance) is a research-focused, modular reading and reflection data-agnostic system designed to help you build intentional and critical reading habits, retain insights, and connect ideas across any field. Resonote encourages critical engagement by combining content ingestion, thoughtful curation, structured indexing, and lightweight reflection — with support for future expansion into knowledge graphs and external integrations. It will serve users to build effective, consistent reading habits and enhance memory, accuracy, and critical thinking.

Tech: Built with a **Flask backend** and **SvelteKit frontend**, Resonote focuses on transparency, personalization, and long-term learning across any knowledge domain.

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

ingestion/: Scrapers and ingestion logic for fetching raw content from external sources.

curation/: Cleans content and extracts metadata (title, tags, read time).

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
                          (Coming Soon: React/Svelte UI)

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

---


## Frontend Setup

```bash
cd frontend
npx sv create .
npm install
npm run dev
```

Visit: http://localhost:5173

---

## Running Tests

```bash
pytest
```