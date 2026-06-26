# Frontend

React + Vite + Tailwind CSS + shadcn/ui shell for ProspectPilot.

## Layout

| Folder              | Responsibility                              |
|---------------------|---------------------------------------------|
| `src/components/`   | Shared UI (layout, chat, trace panels)      |
| `src/components/ui/`| shadcn/ui primitives (Button, Card, …)     |
| `src/pages/`        | Route-level screens                         |
| `src/hooks/`        | Reusable React hooks                        |
| `src/api/`          | Backend HTTP client                         |
| `src/lib/`          | Utilities (`cn()` for Tailwind merging)     |

Run: `npm install && npm run dev`

Add shadcn components: `npx shadcn@latest add button`
