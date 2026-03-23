"""MCP server for GRD protocol / phase lifecycle management.

Exposes tools for parsing ROADMAP.md, computing dependency waves,
discovering plans, and managing the phase lifecycle.
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

from grd.core.constants import ProjectLayout, get_layout
from grd.core.phases import (
    parse_roadmap,
    compute_waves,
    discover_plans,
    discover_summaries,
    parse_plan_file,
)

server = Server("grd-protocols")


def _get_layout(project_root: str | None = None) -> ProjectLayout:
    if project_root:
        return ProjectLayout(root=Path(project_root))
    return get_layout()


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="parse_roadmap",
            description="Parse ROADMAP.md into phases with plans and goals.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_root": {"type": "string"},
                },
            },
        ),
        Tool(
            name="compute_waves",
            description="Compute dependency-ordered execution waves for a phase's plans.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_root": {"type": "string"},
                    "phase_id": {"type": "string", "description": "Phase to compute waves for."},
                },
                "required": ["phase_id"],
            },
        ),
        Tool(
            name="discover_plans",
            description="Find all PLAN-*.md files for a given phase.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_root": {"type": "string"},
                    "phase_id": {"type": "string"},
                },
                "required": ["phase_id"],
            },
        ),
        Tool(
            name="discover_summaries",
            description="Find all SUMMARY-*.md files for a given phase.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_root": {"type": "string"},
                    "phase_id": {"type": "string"},
                },
                "required": ["phase_id"],
            },
        ),
        Tool(
            name="parse_plan",
            description="Parse a PLAN-*.md file into structured plan with tasks and dependencies.",
            inputSchema={
                "type": "object",
                "properties": {
                    "plan_path": {"type": "string", "description": "Absolute path to a PLAN-*.md file."},
                },
                "required": ["plan_path"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "parse_roadmap":
        layout = _get_layout(arguments.get("project_root"))
        phases = parse_roadmap(layout.roadmap_md)
        result = [
            {
                "id": p.id,
                "title": p.title,
                "goal": p.goal,
                "plans": [
                    {"id": pl.id, "title": pl.title, "depends_on": pl.depends_on}
                    for pl in p.plans
                ],
            }
            for p in phases
        ]
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "compute_waves":
        layout = _get_layout(arguments.get("project_root"))
        phases = parse_roadmap(layout.roadmap_md)
        target_phase = None
        for p in phases:
            if p.id == arguments["phase_id"]:
                target_phase = p
                break
        if not target_phase:
            return [TextContent(type="text", text=json.dumps({"error": f"Phase {arguments['phase_id']} not found"}))]

        waves = compute_waves(target_phase.plans)
        result = [
            {
                "wave": w.number,
                "plans": [{"id": pl.id, "title": pl.title} for pl in w.plans],
            }
            for w in waves
        ]
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "discover_plans":
        layout = _get_layout(arguments.get("project_root"))
        plans = discover_plans(layout, arguments["phase_id"])
        return [TextContent(type="text", text=json.dumps([str(p) for p in plans]))]

    elif name == "discover_summaries":
        layout = _get_layout(arguments.get("project_root"))
        summaries = discover_summaries(layout, arguments["phase_id"])
        return [TextContent(type="text", text=json.dumps([str(s) for s in summaries]))]

    elif name == "parse_plan":
        plan = parse_plan_file(Path(arguments["plan_path"]))
        result = {
            "id": plan.id,
            "phase_id": plan.phase_id,
            "title": plan.title,
            "goal": plan.goal,
            "status": plan.status,
            "depends_on": plan.depends_on,
            "tasks": [
                {
                    "id": t.id,
                    "title": t.title,
                    "description": t.description,
                    "status": t.status,
                    "depends_on": t.depends_on,
                    "wave": t.wave,
                }
                for t in plan.tasks
            ],
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
