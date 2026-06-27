# tools/

Reusable capabilities invoked by agents. Agents never call external APIs directly.

| Tool | File | Integration | Fallback |
|------|------|-------------|----------|
| Web search | `web_search.py` | Tavily → Firecrawl | Mock search results |
| Company extraction | `company_extraction.py` | Gemini LLM | Mock companies |
| Qualification | `qualification.py` | Gemini LLM | Rule-based mock |
| Contact enrichment | `contact_enrichment.py` | Apollo.io | Mock contacts |
| Recommendation | `recommendation.py` | Gemini LLM | Template mock |

Every tool returns `ToolResult` with `source`, `is_mock`, and `error` fields.
Agents propagate these under `integrations` in shared state / memory.

Access via `tools.registry.get_*()` functions.
