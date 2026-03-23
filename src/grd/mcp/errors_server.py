"""MCP server for GRD error handling and decision logging.

Exposes tools for recording decisions, managing verification
failures, and querying the decision audit trail.
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
from grd.core.constants import ProjectLayout

server = Server("grd-errors")


def _get_engine(project_root: str | None = None) -> StateEngine:
    if project_root:
        return StateEngine(layout=ProjectLayout(root=Path(project_root)))
    return StateEngine()


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="add_decision",
            description="Record a decision in the audit trail with phase, rationale, and agent.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_root": {"type": "string"},
                    "phase": {"type": "string", "description": "Phase where decision was made."},
                    "decision": {"type": "string", "description": "What was decided."},
                    "rationale": {"type": "string", "description": "Why this decision was made."},
                    "agent": {"type": "string", "description": "Agent or person who made the decision."},
                },
                "required": ["phase", "decision", "rationale"],
            },
        ),
        Tool(
            name="list_decisions",
            description="List all decisions in the audit trail, optionally filtered by phase.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_root": {"type": "string"},
                    "phase": {"type": "string", "description": "Filter by phase (optional)."},
                    "limit": {"type": "integer", "description": "Max decisions to return (default 50)."},
                },
            },
        ),
        Tool(
            name="get_verification_stats",
            description="Get verification pass/fail statistics.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_root": {"type": "string"},
                },
            },
        ),
        Tool(
            name="record_verification_result",
            description="Record a verification pass or failure and increment counters.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_root": {"type": "string"},
                    "passed": {"type": "boolean", "description": "True if verification passed."},
                    "phase": {"type": "string"},
                    "details": {"type": "string", "description": "Description of what was verified."},
                },
                "required": ["passed", "phase", "details"],
            },
        ),
        Tool(
            name="recover_state",
            description="Check for and recover from interrupted state writes.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_root": {"type": "string"},
                },
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    engine = _get_engine(arguments.get("project_root"))

    if name == "add_decision":
        engine.add_decision(
            phase=arguments["phase"],
            decision=arguments["decision"],
            rationale=arguments["rationale"],
            agent=arguments.get("agent", ""),
        )
        return [TextContent(type="text", text=json.dumps({"status": "recorded"}))]

    elif name == "list_decisions":
        state = engine.load()
        decisions = [
            {
                "timestamp": d.timestamp,
                "phase": d.phase,
                "decision": d.decision,
                "rationale": d.rationale,
                "agent": d.agent,
            }
            for d in state.decisions
        ]
        phase_filter = arguments.get("phase")
        if phase_filter:
            decisions = [d for d in decisions if d["phase"] == phase_filter]
        limit = arguments.get("limit", 50)
        decisions = decisions[-limit:]
        return [TextContent(type="text", text=json.dumps(decisions, indent=2))]

    elif name == "get_verification_stats":
        state = engine.load()
        return [TextContent(type="text", text=json.dumps({
            "total_tasks_completed": state.total_tasks_completed,
            "total_verification_passes": state.total_verification_passes,
            "total_verification_failures": state.total_verification_failures,
            "pass_rate": round(
                state.total_verification_passes / max(1, state.total_verification_passes + state.total_verification_failures) * 100, 1
            ),
        }))]

    elif name == "record_verification_result":
        state = engine.load()
        if arguments["passed"]:
            state.total_verification_passes += 1
        else:
            state.total_verification_failures += 1
        state.total_tasks_completed += 1
        engine.save(state)

        engine.add_decision(
            phase=arguments["phase"],
            decision=f"Verification {'PASS' if arguments['passed'] else 'FAIL'}: {arguments['details']}",
            rationale="Automated verification result recording.",
            agent="grd-errors-server",
        )
        return [TextContent(type="text", text=json.dumps({
            "status": "recorded",
            "passed": arguments["passed"],
        }))]

    elif name == "recover_state":
        recovered = engine.recover_if_needed()
        return [TextContent(type="text", text=json.dumps({
            "recovery_needed": recovered,
            "status": "recovered" if recovered else "clean",
        }))]

    return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
