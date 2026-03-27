"""Client factory for COROS MCP server — stateless token management."""

import json
import logging
from fastmcp import Context

from coros_mcp.sdk.client import CorosClient

logger = logging.getLogger(__name__)

COROS_TOKENS_KEY = "coros_tokens"


def create_client_from_tokens(tokens: str) -> CorosClient:
    """Create an authenticated CorosClient from serialized tokens."""
    client = CorosClient(region="eu")
    client.load_token(tokens)
    return client


def _get_session_tokens(ctx: Context) -> str | None:
    """Get tokens from request meta (stateless) or session state (fallback)."""
    try:
        if ctx.request_context and ctx.request_context.meta:
            meta_context = ctx.request_context.meta.context
            if meta_context and isinstance(meta_context, dict):
                token = meta_context.get('sport_platform_token')
                if token:
                    return token
    except (AttributeError, TypeError):
        pass
    return ctx.get_state(COROS_TOKENS_KEY)


def get_client(ctx: Context) -> CorosClient:
    """Get an authenticated CorosClient from context. Raises ValueError if no session."""
    tokens = _get_session_tokens(ctx)
    if not tokens:
        raise ValueError("No COROS session. Call coros_login() first.")
    return create_client_from_tokens(tokens)


def set_session_tokens(ctx: Context, tokens: str) -> None:
    """Store tokens in session state."""
    ctx.set_state(COROS_TOKENS_KEY, tokens)


def clear_session_tokens(ctx: Context) -> None:
    """Clear tokens from session state."""
    ctx.set_state(COROS_TOKENS_KEY, None)


def is_token_expired_error(error: Exception) -> bool:
    """Return True if the error indicates an expired/invalid COROS token."""
    msg = str(error).lower()
    return "access token is invalid" in msg or ("token" in msg and "invalid" in msg)


def handle_token_expired(ctx: Context) -> str:
    """Clear session and return a JSON error for expired token."""
    try:
        clear_session_tokens(ctx)
    except Exception:
        pass
    return json.dumps({
        "error": "Your COROS session has expired. Please log in again.",
        "error_code": "SESSION_EXPIRED",
    }, indent=2)
