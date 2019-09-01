"""文字列関連のユーティリティモジュール。
"""
import unicodedata
from typing import List, Optional


def width(text: Optional[str]) -> int:
    """文字列の幅を取得する。

    Args:
        text: 文字列

    Returns:
        文字列の幅（半角:1、全角:2）
    """
    result = 0
    if text:
        for c in text:
            if unicodedata.east_asian_width(c) in "FWA":
                result += 2
            else:
                result += 1
    return result


def max_width(list: List[str]) -> int:
    """文字列リストの最大幅を取得する。

    Args:
        text: 文字列

    Returns:
        最大幅（半角:1、全角:2）
    """
    return max(map(width, list))


def min_width(list: List[str]) -> int:
    """文字列リストの最小幅を取得する。

    Args:
        text: 文字列

    Returns:
        最小幅（半角:1、全角:2）
    """
    return min(map(width, list))


def reverse(text: str) -> str:
    """指定した文字列の逆順の文字列を取得する。

    Args:
        text: 文字列

    Returns:
        逆順の文字列
    """
    return "".join(list(reversed(text)))
