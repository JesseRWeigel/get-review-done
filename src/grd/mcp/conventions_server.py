"""MCP server for GRD convention lock management.

Exposes tools for locking, querying, and diffing systematic review
conventions (PICO, inclusion/exclusion criteria, search strategy, etc.).
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from grd.core.state import StateEngine
from grd.core.constants import ProjectLayout, CONVENTION_FIELDS
from grd.core.conventions import (
    list_all_fields,
    check_conventions,
    diff_conventions,
    get_field_description,
    get_field_examples,
)

server = Server("grd-conventions")


def _get_engine(project_root: str | None = None) -> StateEngine:
    if project_root:
        return StateEngine(layout=ProjectLayout(root=Path(project_root)))
    return StateEngine()


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="list_convention_fields",
            description="List all convention fields with descriptions and examples.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="check_conventions",
            description="Check which conventions are locked vs unlocked, with coverage stats.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_root": {"type": "string"},
                },
            },
        ),
        Tool(
            name="lock_convention",
            description="Lock a convention field to a specific value.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_root": {"type": "string"},
                    "field": {
                        "type": "string",
                        "description": f"Field name. Valid: {', '.join(CONVENTION_FIELDS)}",
                    },
                    "value": {"type": "string", "description": "The value to lock."},
                    "locked_by": {"type": "string", "description": "Phase/plan that locked it."},
                    "rationale": {"type": "string", "description": "Why this value was chosen."},
                },
                "required": ["field", "value", "locked_by"],
            },
        ),
        Tool(
            name="get_convention",
            description="Get the current locked value for a convention field.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_root": {"type": "string"},
                    "field": {"type": "string"},
                },
                "required": ["field"],
            },
        ),
        Tool(
            name="diff_conventions",
            description="Compare proposed convention values against current locks. Returns conflicts.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_root": {"type": "string"},
                    "proposed": {
                        "type": "object",
                        "description": "Dict of field -> proposed_value to compare.",
                        "additionalProperties": {"type": "string"},
                    },
                },
                "required": ["proposed"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "list_convention_fields":
        fields = list_all_fields()
        return [TextContent(type="text", text=json.dumps(fields, indent=2))]

    engine = _get_engine(arguments.get("project_root"))

    if name == "check_conventions":
        report = check_conventions(engine)
        return [TextContent(type="text", text=json.dumps(report, indent=2))]

    elif name == "lock_convention":
        engine.set_convention(
            field=arguments["field"],
            value=arguments["value"],
            locked_by=arguments["locked_by"],
            rationale=arguments.get("rationale", ""),
        )
        return [TextContent(type="text", text=json.dumps({
            "status": "locked",
            "field": arguments["field"],
            "value": arguments["value"],
        }))]

    elif name == "get_convention":
        value = engine.get_convention(arguments["field"])
        return [TextContent(type="text", text=json.dumps({
            "field": arguments["field"],
            "value": value,
            "description": get_field_description(arguments["field"]),
            "examples": get_field_examples(arguments["field"]),
        }))]

    elif name == "diff_conventions":
        result = diff_conventions(engine, arguments["proposed"])
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
