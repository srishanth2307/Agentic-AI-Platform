# ProspectPilot

Reusable Agentic AI Platform — hackathon project by XL Ventures.AI.

## Structure

```
├── backend/          # FastAPI + agent platform core
├── frontend/         # React + Tailwind + shadcn/ui
└── README.md
```

See each subfolder's README for module responsibilities.

## Quick start (after setup)

```bash
# Backend
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```
