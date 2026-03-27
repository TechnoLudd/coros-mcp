"""
Dashboard tools for COROS MCP server.

Fitness overview, HRV trends, race predictions, and personal records.
Delegates to api.status for formatting.
"""

import json

from fastmcp import Context

from coros_mcp.client_factory import get_client
from coros_mcp.api import status as api_status


def register_tools(app):
    """Register dashboard tools with the MCP app."""

    @app.tool()
    async def get_fitness_summary(ctx: Context) -> str:
        """
        Get the athlete's current fitness overview.

        Combines dashboard summary and detail data into a unified view:
        recovery state, fitness scores, HRV baseline, stamina level,
        training load vs target, and current week records.

        This is the "how is the athlete doing right now" tool.

        Returns:
            JSON with fitness summary data
        """
        try:
            return json.dumps(api_status.get_fitness_status(get_client(ctx)), indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    @app.tool()
    async def get_race_predictions(ctx: Context) -> str:
        """
        Get race time predictions for 5K, 10K, half marathon, and marathon.

        Based on the athlete's current fitness level and training data.
        Useful for setting race goals and planning training paces.

        Returns:
            JSON with predicted race times and paces
        """
        try:
            return json.dumps(api_status.get_race_predictions(get_client(ctx)), indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    @app.tool()
    async def get_hrv_trend(ctx: Context) -> str:
        """
        Get HRV (Heart Rate Variability) trend data.

        Returns HRV baseline and daily values from sleep data.
        Useful for overtraining detection and recovery monitoring.

        Returns:
            JSON with HRV trend data
        """
        try:
            return json.dumps(api_status.get_hrv_trend(get_client(ctx)), indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    @app.tool()
    async def get_personal_records(ctx: Context) -> str:
        """
        Get personal records by time period.

        Returns PRs for week, month, year, and all-time across sports.
        Useful for motivation and progress tracking.

        Returns:
            JSON with personal records grouped by period
        """
        try:
            return json.dumps(api_status.get_personal_records(get_client(ctx)), indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    return app
