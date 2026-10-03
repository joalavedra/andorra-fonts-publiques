import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from fonts_andorra import mcp_server

ROOT = Path(__file__).resolve().parents[1]


def test_stdio_server_lists_tools():
    async def check():
        params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "fonts_andorra.mcp_server"],
            cwd=str(ROOT),
        )
        async with stdio_client(params) as (read_stream, write_stream), ClientSession(
            read_stream, write_stream
        ) as client:
            await client.initialize()
            result = await client.list_tools()
            return {tool.name for tool in result.tools}

    names = asyncio.run(check())
    assert {
        "search_catalog", "source", "bopa_search", "bopa_document", "stats_search",
        "stats_data", "tramits_search", "tramit", "geo_query", "feed_latest",
    } <= names


def test_tramit_exposes_application_period(monkeypatch):
    monkeypatch.setattr(
        mcp_server.tramits,
        "procedure",
        lambda code, lang: {
            "code": code,
            "lang": lang,
            "application_period": "Tot l’any.",
            "sections": {},
            "documents": [],
        },
    )

    result = json.loads(mcp_server.tramit("GV000484"))

    assert result["application_period"] == "Tot l’any."
