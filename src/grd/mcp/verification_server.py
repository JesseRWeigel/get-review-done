"""MCP server for GRD verification kernel.

Exposes tools for running the 12 PRISMA/methodology predicates
over evidence registries and producing SHA-256 verdicts.
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

from grd.core.kernel import VerificationKernel, DEFAULT_PREDICATES, VERIFICATION_CHECKS

server = Server("grd-verification")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="verify",
            description=(
                "Run all 12 PRISMA/methodology verification checks against an evidence registry. "
                "Returns a content-addressed verdict with SHA-256 hashes."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "evidence": {
                        "type": "object",
                        "description": (
                            "Evidence registry dict. Keys include: prisma_items_reported, "
                            "prisma_items_missing, databases_searched, search_strategies_documented, "
                            "search_dates_recorded, screening_method, dual_screening, screening_kappa, "
                            "extraction_fields_specified, extraction_fields_extracted, "
                            "quality_assessment_tool, studies_assessed, studies_included, "
                            "meta_analysis_conducted, model_type, heterogeneity_assessed, i_squared, "
                            "effect_measure, publication_bias_assessed, publication_bias_methods, "
                            "grade_conducted, outcomes_graded, grade_domains_assessed, "
                            "sensitivity_analyses_planned, sensitivity_analyses_conducted, "
                            "narrative_inconsistencies, tables_cross_checked, figures_cross_checked, "
                            "protocol_registered, protocol_deviations, deviations_explained, "
                            "citations_checked, citation_errors, missing_citations."
                        ),
                    },
                },
                "required": ["evidence"],
            },
        ),
        Tool(
            name="list_checks",
            description="List all available verification checks with their IDs.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="run_single_check",
            description="Run a single named verification check against evidence.",
            inputSchema={
                "type": "object",
                "properties": {
                    "check_id": {
                        "type": "string",
                        "description": f"Check to run. Valid: {', '.join(VERIFICATION_CHECKS)}",
                    },
                    "evidence": {"type": "object"},
                },
                "required": ["check_id", "evidence"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "verify":
        kernel = VerificationKernel()
        verdict = kernel.verify(arguments["evidence"])
        return [TextContent(type="text", text=verdict.to_json())]

    elif name == "list_checks":
        from grd.core.constants import VERIFICATION_CHECKS as checks
        return [TextContent(type="text", text=json.dumps(checks, indent=2))]

    elif name == "run_single_check":
        check_id = arguments["check_id"]
        if check_id not in DEFAULT_PREDICATES:
            return [TextContent(type="text", text=json.dumps({
                "error": f"Unknown check: {check_id}",
                "available": list(DEFAULT_PREDICATES.keys()),
            }))]
        predicate = DEFAULT_PREDICATES[check_id]
        result = predicate(arguments["evidence"])
        return [TextContent(type="text", text=json.dumps({
            "check_id": result.check_id,
            "name": result.name,
            "status": result.status,
            "severity": result.severity.value,
            "message": result.message,
            "evidence": result.evidence,
            "suggestions": result.suggestions,
        }, indent=2))]

    return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
