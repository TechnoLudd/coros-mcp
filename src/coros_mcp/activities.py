"""
Activity management tools for COROS MCP server.

Delegates to api.activities for formatting.
"""

import json

from fastmcp import Context

from coros_mcp.client_factory import get_client
from coros_mcp.api import activities as api_activities


def register_tools(app):
    """Register activity tools with the MCP app."""

    @app.tool()
    async def get_activities(
        ctx: Context,
        start_date: str = None,
        end_date: str = None,
        page: int = 1,
        size: int = 20,
    ) -> str:
        """
        Get list of COROS activities.

        Returns a paginated list of activities with summary information.
        Activities can be filtered by date range.

        Args:
            start_date: Filter start date in YYYY-MM-DD format (optional)
            end_date: Filter end date in YYYY-MM-DD format (optional)
            page: Page number, starting from 1 (default: 1)
            size: Number of activities per page (default: 20, max: 50)

        Returns:
            JSON with activity list and pagination info
        """
        try:
            return json.dumps(api_activities.get_activities(get_client(ctx), start_date, end_date, page, size), indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    @app.tool()
    async def get_activity_details(activity_id: str, ctx: Context) -> str:
        """
        Get detailed information about a COROS activity.

        Returns comprehensive activity data including:
        - Summary metrics (distance, time, pace, heart rate, etc.)
        - Lap data with splits
        - Heart rate zones
        - Weather conditions

        Args:
            activity_id: The activity's labelId from get_activities

        Returns:
            JSON with detailed activity data
        """
        try:
            return json.dumps(api_activities.get_activity_detail(get_client(ctx), activity_id), indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    @app.tool()
    async def get_activity_download_url(
        activity_id: str,
        file_format: str = "fit",
        ctx: Context = None,
    ) -> str:
        """
        Get download URL for a COROS activity file.

        The returned URL can be used to download the activity in the
        specified format. URLs are temporary and expire after some time.

        Args:
            activity_id: The activity's labelId
            file_format: Export format: fit, tcx, gpx, kml, or csv (default: fit)

        Returns:
            JSON with the download URL
        """
        try:
            return json.dumps(api_activities.get_download_url(get_client(ctx), activity_id, format=file_format), indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    @app.tool()
    async def get_activities_summary(
        ctx: Context,
        days: int = 7,
    ) -> str:
        """
        Get a summary of recent activities.

        Provides an aggregated view of activities over the specified
        number of days, including totals for distance, time, and load.

        Args:
            days: Number of days to include (default: 7, max: 30)

        Returns:
            JSON with activity summary statistics
        """
        try:
            return json.dumps(api_activities.get_activities_summary(get_client(ctx), days), indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    return app
