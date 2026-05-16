import os
from typing import TYPE_CHECKING

import streamlit as st

if TYPE_CHECKING:
    from supabase import Client


def _get_secret(key: str) -> str:
    try:
        return st.secrets[key]
    except (KeyError, FileNotFoundError, AttributeError):
        value = os.environ.get(key)
        if value:
            return value
        raise RuntimeError(
            f"Missing {key}. For local runs, copy "
            ".streamlit/secrets.toml.example to .streamlit/secrets.toml. "
            "On Streamlit Community Cloud, add it in the app Secrets settings."
        ) from None


@st.cache_resource
def get_supabase_client() -> "Client":
    try:
        from supabase import create_client
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "Package 'supabase' is not installed. Add supabase==2.30.0 to "
            "requirements.txt, push to GitHub, and redeploy."
        ) from exc

    return create_client(
        _get_secret("SUPABASE_URL"),
        _get_secret("SUPABASE_KEY"),
    )


class _SupabaseProxy:
    def __getattr__(self, name):
        return getattr(get_supabase_client(), name)


supabase = _SupabaseProxy()
