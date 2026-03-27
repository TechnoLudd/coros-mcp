"""
Analysis tools for COROS MCP server.

Training load analysis, sport statistics, and long-term trends.
Delegates to api.status for formatting.
"""

import json

from fastmcp import Context

from coros_mcp.client_factory import get_client
from coros_mcp.api import status as api_status


def register_tools(app):
    """Register analysis tools with the MCP app."""

    @app.tool()
    async def get_training_load_analysis(ctx: Context) -> str:
        """
        Get comprehensive training load analysis.

        Returns daily/weekly load, ATI/CTI (acute/chronic training index),
        tired rate, VO2max trend, recommended load range, and periodization stages.

        Essential for load management and periodization decisions.

        Returns:
            JSON with training load analysis data
        """
        try:
            return json.dumps(api_status.get_training_load(get_client(ctx)), indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    @app.tool()
    async def get_sport_statistics(ctx: Context) -> str:
        """
        Get per-sport volume/load breakdown and intensity distribution.

        Returns sport-by-sport aggregates (count, distance, duration, load)
        and weekly training intensity breakdown (low/medium/high percentage).

        Useful for analyzing training balance across sports.

        Returns:
            JSON with sport statistics and intensity distribution
        """
        try:
            return json.dumps(api_status.get_sport_stats(get_client(ctx)), indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    return app
