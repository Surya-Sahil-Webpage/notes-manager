# Notes Manager

A full-stack Notes Manager application built with FastAPI and React.

## Tech Stack

**Backend:** FastAPI, SQLAlchemy, Alembic, PostgreSQL, Pydantic  
**Frontend:** React, Vite, Tailwind CSS v4, React Router, Axios

## Features

- Create, view, edit, and delete notes
- RESTful API with full Swagger documentation
- Persistent PostgreSQL storage
- Responsive UI

## Local Development

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

API runs at: http://localhost:8000  
Swagger docs: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App runs at: http://localhost:5173