"""Reusable web search — Tavily primary, Firecrawl fallback, mock last resort."""

import httpx

from config.settings import settings
from tools.types import IntegrationSource, ToolResult


class WebSearchTool:
    """
    Search the web for companies matching an ICP.

    Priority: Tavily → Firecrawl → mock (clearly labeled).
    """

    def search(self, query: str, max_results: int = 5) -> ToolResult:
        if settings.tavily_api_key:
            return self._search_tavily(query, max_results)
        if settings.firecrawl_api_key:
            return self._search_firecrawl(query, max_results)
        return self._search_mock(query, max_results)

    def _search_tavily(self, query: str, max_results: int) -> ToolResult:
        try:
            response = httpx.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": settings.tavily_api_key,
                    "query": query,
                    "search_depth": "advanced",
                    "max_results": max_results,
                    "include_answer": True,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            payload = response.json()
            results = [
                {
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "content": item.get("content", ""),
                    "score": item.get("score"),
                }
                for item in payload.get("results", [])
            ]
            return ToolResult(
                success=True,
                source=IntegrationSource.TAVILY,
                data={
                    "query": query,
                    "answer": payload.get("answer", ""),
                    "results": results,
                },
                is_mock=False,
            )
        except Exception as exc:
            return ToolResult(
                success=False,
                source=IntegrationSource.TAVILY,
                data={"query": query, "results": []},
                error=str(exc),
                is_mock=False,
            )

    def _search_firecrawl(self, query: str, max_results: int) -> ToolResult:
        try:
            response = httpx.post(
                "https://api.firecrawl.dev/v1/search",
                headers={"Authorization": f"Bearer {settings.firecrawl_api_key}"},
                json={"query": query, "limit": max_results},
                timeout=30.0,
            )
            response.raise_for_status()
            payload = response.json()
            raw = payload.get("data", payload.get("results", []))
            results = [
                {
                    "title": item.get("title", item.get("metadata", {}).get("title", "")),
                    "url": item.get("url", item.get("metadata", {}).get("sourceURL", "")),
                    "content": item.get("markdown", item.get("description", "")),
                }
                for item in raw
            ]
            return ToolResult(
                success=True,
                source=IntegrationSource.FIRECRAWL,
                data={"query": query, "results": results},
                is_mock=False,
            )
        except Exception as exc:
            return ToolResult(
                success=False,
                source=IntegrationSource.FIRECRAWL,
                data={"query": query, "results": []},
                error=str(exc),
                is_mock=False,
            )

    @staticmethod
    def _search_mock(query: str, max_results: int) -> ToolResult:
        """Deterministic mock search results when no search API is configured."""
        mock_results = [
            {
                "title": "Acme Corp — B2B SaaS sales platform",
                "url": "https://acme.example/about",
                "content": (
                    "Acme Corp is a B2B SaaS company with ~250 employees headquartered "
                    "in San Francisco. Recently raised Series B and hiring VP Sales."
                ),
            },
            {
                "title": "NovaStack DevTools — developer productivity",
                "url": "https://novastack.io",
                "content": (
                    "NovaStack builds developer tools for engineering teams, "
                    "120 employees, strong outbound GTM motion."
                ),
            },
        ][:max_results]
        return ToolResult(
            success=True,
            source=IntegrationSource.MOCK,
            data={"query": query, "answer": "Mock search — configure TAVILY_API_KEY or FIRECRAWL_API_KEY for live results.", "results": mock_results},
            is_mock=True,
            error="No search API key configured",
        )
