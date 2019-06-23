"""日時関連のユーティリティモジュール。
"""
from datetime import datetime
from typing import Optional

DEFAULT_PATTERN = "%Y-%m-%d %H:%M:%S.%f"
"""デフォルト日時パターン文字列。
"""


def get_from_str(dt_str: Optional[str], pattern: str = DEFAULT_PATTERN) \
        -> Optional[datetime]:
    """日時文字列から、datetimeオブジェクトを取得する。

    Args:
        dt_str: 日時文字列
        pattern: 日時パターン文字列

    Returns:
        datetimeオブジェクト
    """
    if dt_str is None:
        return None
    try:
        return datetime.strptime(dt_str, pattern)
    except ValueError:
        return None


def to_str(dt: Optional[datetime], pattern: str = DEFAULT_PATTERN) \
        -> Optional[str]:
    """datetimeオブジェクトを日時文字列に変換する。

    Args:
        dt: datetimeオブジェクト
        pattern: 日時パターン文字列

    Returns:
        日時文字列
    """
    if dt is None:
        return None
    return dt.strftime(pattern)


def get_from_utc(utc: Optional[float]) -> Optional[datetime]:
    """UTC値から、datetimeオブジェクトを取得する。

    Args:
        utc: UTC値

    Returns:
        datetimeオブジェクト
    """
    if utc is None:
        return None
    return datetime.fromtimestamp(utc)


def to_utc(dt: Optional[datetime]) -> Optional[float]:
    """datetimeオブジェクトをUTC値に変換する。

    Args:
        dt: datetimeオブジェクト

    Returns:
        UTC値
    """
    if dt is None:
        return None
    return dt.timestamp()
