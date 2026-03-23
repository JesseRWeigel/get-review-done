"""MCP server for GRD state management.

Exposes tools for loading, saving, and querying project state
via the dual-write StateEngine.
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Add project root to path so core imports work
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from grd.core.state import StateEngine, ProjectState
from grd.core.constants import ProjectLayout

server = Server("grd-state")


def _get_engine(project_root: str | None = None) -> StateEngine:
    if project_root:
        return StateEngine(layout=ProjectLayout(root=Path(project_root)))
    return StateEngine()


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="load_state",
            description="Load the current project state from state.json.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_root": {
                        "type": "string",
                        "description": "Path to project root (optional, auto-detected if omitted).",
                    }
                },
            },
        ),
        Tool(
            name="save_state",
            description="Save project state (atomic dual-write to state.json + STATE.md).",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_root": {"type": "string"},
                    "state": {
                        "type": "object",
                        "description": "Full ProjectState dict to save.",
                    },
                },
                "required": ["state"],
            },
        ),
        Tool(
            name="advance_phase",
            description="Mark a phase as completed and activate the next pending phase.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_root": {"type": "string"},
                    "phase_id": {
                        "type": "string",
                        "description": "ID of the phase to mark complete.",
                    },
                },
                "required": ["phase_id"],
            },
        ),
        Tool(
            name="set_result",
            description="Store an intermediate result for cross-phase access.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_root": {"type": "string"},
                    "key": {"type": "string"},
                    "value": {"type": "string", "description": "JSON-encoded value to store."},
                },
                "required": ["key", "value"],
            },
        ),
        Tool(
            name="get_result",
            description="Retrieve a stored intermediate result by key.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_root": {"type": "string"},
                    "key": {"type": "string"},
                },
                "required": ["key"],
            },
        ),
        Tool(
            name="update_prisma_counts",
            description="Increment PRISMA flow diagram counts (identified, screened, included, excluded).",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_root": {"type": "string"},
                    "identified": {"type": "integer", "default": 0},
                    "screened": {"type": "integer", "default": 0},
                    "included": {"type": "integer", "default": 0},
                    "excluded": {"type": "integer", "default": 0},
                },
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    engine = _get_engine(arguments.get("project_root"))

    if name == "load_state":
        state = engine.load()
        return [TextContent(type="text", text=json.dumps(state.model_dump(mode="json"), indent=2))]

    elif name == "save_state":
        state = ProjectState(**arguments["state"])
        engine.save(state)
        return [TextContent(type="text", text=json.dumps({"status": "saved", "updated_at": state.updated_at}))]

    elif name == "advance_phase":
        engine.advance_phase(arguments["phase_id"])
        state = engine.load()
        return [TextContent(type="text", text=json.dumps({
            "status": "advanced",
            "current_phase": state.current_phase,
        }))]

    elif name == "set_result":
        value = json.loads(arguments["value"])
        engine.set_result(arguments["key"], value)
        return [TextContent(type="text", text=json.dumps({"status": "stored", "key": arguments["key"]}))]

    elif name == "get_result":
        value = engine.get_result(arguments["key"])
        return [TextContent(type="text", text=json.dumps({"key": arguments["key"], "value": value}))]

    elif name == "update_prisma_counts":
        engine.update_prisma_counts(
            identified=arguments.get("identified", 0),
            screened=arguments.get("screened", 0),
            included=arguments.get("included", 0),
            excluded=arguments.get("excluded", 0),
        )
        state = engine.load()
        return [TextContent(type="text", text=json.dumps({
            "status": "updated",
            "total_identified": state.total_studies_identified,
            "total_screened": state.total_studies_screened,
            "total_included": state.total_studies_included,
            "total_excluded": state.total_studies_excluded,
        }))]

    return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
