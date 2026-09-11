"""Tushare API client construction helpers."""

from urllib.parse import urlparse


DEFAULT_TUSHARE_API_URL = "http://api.tushare.pro"


def normalize_tushare_api_url(api_url: str | None) -> str:
    """Normalize and validate a Tushare-compatible API endpoint."""
    value = (api_url or "").strip().strip('"').strip("'")
    if not value:
        return DEFAULT_TUSHARE_API_URL

    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(
            "Tushare API 地址必须是完整的 HTTP(S) URL，例如 "
            "https://api.tushare.pro"
        )
    return value.rstrip("/")


def create_tushare_api(token: str, api_url: str | None = None):
    """Create a Tushare Pro client and apply a custom API endpoint."""
    if not token or not token.strip():
        raise ValueError("Tushare token 不能为空")

    import tushare as ts

    endpoint = normalize_tushare_api_url(api_url)
    try:
        api = ts.pro_api(token.strip())
    except TypeError:
        ts.set_token(token.strip())
        api = ts.pro_api()

    for attribute in ("_DataApi__http_url", "http_url", "_http_url"):
        if hasattr(api, attribute):
            setattr(api, attribute, endpoint)
            return api

    raise RuntimeError(
        "当前 tushare SDK 不支持设置自定义 API 地址，请升级 tushare 依赖"
    )
