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

## Project Structure

```bash
resonote/
├── backend/                            # Flask backend application
│   ├── app/                            # Main backend package
│   │   ├── __init__.py                 # Python module marker
│   │   ├── main.py                     # Flask app factory
│   │   ├── config.py                   # App configuration (dev/prod/etc.)
│   │   ├── models/                     # SQLAlchemy or Pydantic models
│   │   ├── routes/                     # Flask Blueprints (API routes)
│   │   ├── services/                   # Core logic: ingestion, curation, etc.
│   │   ├── core/                       # NLP, vector indexing, AI utils
│   │   └── db/                         # Database setup, session, migrations
│   ├── scripts/                        # CLI tools for scraping, seeding, etc.
│   ├── tests/                          # Unit + integration tests (pytest)
│   ├── requirements.txt                # Python dependencies
│   └── run.py                          # Entry point for running Flask app
│
├── frontend/                           # SvelteKit frontend application
│   ├── public/                         # Static assets (favicons, etc.)
│   ├── src/
│   │   ├── routes/                     # SvelteKit file-based routing
│   │   ├── components/                 # Shared UI components
│   │   ├── lib/                        # Stores, utils, helper functions
│   │   └── App.svelte                  # Root Svelte component
│   ├── svelte.config.js                # SvelteKit config
│   ├── vite.config.js                  # Vite bundler config
│   └── package.json                    # Frontend dependencies + scripts
│
├── .env                                # Environment variables for local dev
├── README.md                           # Project overview and setup guide
└── pyproject.toml (optional)           # Python project metadata (if needed)
```

---

## Backend Setup

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
