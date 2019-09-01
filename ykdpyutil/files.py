"""ファイル関連のユーティリティモジュール。
"""
import glob
import os
import shutil
from datetime import datetime
from typing import cast, List, Optional, Tuple

from ykdpyutil import datetimes

FILE_NAME_DELIMITER = "."


def get_files(root: Optional[str], filter=lambda p: True,
              recursive=True) -> List[str]:
    """パス配下のファイルリストを取得する。

    Args:
        root: 対象パス
        filter: フィルター
        recursive: 再帰的検索を行うか

    Returns:
        パス配下のファイルリスト
    """
    return get_paths(root, lambda p: os.path.isfile(p) and filter(p),
                     recursive)


def get_dirs(root: Optional[str], filter=lambda p: True,
             recursive=True) -> List[str]:
    """パス配下のディレクトリリストを取得する。

    Args:
        root: 対象パス
        filter: フィルター
        recursive: 再帰的検索を行うか

    Returns:
        パス配下のディレクトリリスト
    """
    return get_paths(root,
                     lambda p: os.path.isdir(p) and p != root and filter(p),
                     recursive)


def get_paths(root: Optional[str],
              p_filter=lambda p: True, recursive=True) -> List[str]:
    """パス配下のパスリストを取得する。

    Args:
        root: 対象パス
        filter: フィルター
        recursive: 再帰的検索を行うか

    Returns:
        パス配下のパスリスト
    """
    if root is None:
        return []
    cast_root = cast(str, root)
    plist = glob.glob(os.path.join(cast_root, "**"), recursive=recursive)

    # ルートフォルダ以外 かつ パラメータフィルター でフィルター生成
    def flt(p):
        is_root = os.path.samefile(cast_root, p)
        result = not is_root and p_filter(p)
        return result
    # フィルタリングして返却
    return list(filter(flt, plist))


def check_exists(path: str) -> None:
    """対象パスの存在を確認する。

    Args:
        path: 対象パス
    """
    if not os.path.exists(path):
        raise OSError("Target path is not found. {}".format(path))


def check_not_exists(path: str) -> None:
    """対象パスの非存在を確認する。

    Args:
        path: 対象パス
    """
    if os.path.exists(path):
        raise OSError("Target path is already exists. {}".format(path))


def make_parent_dir(path: str) -> None:
    """対象パスの親ディレクトリを作成する。

    Args:
        path: 対象パス
    """
    parent = os.path.dirname(path)
    if not os.path.exists(parent):
        os.makedirs(parent)


def copy(src: Optional[str], dst: Optional[str]) -> None:
    """指定パスのコピーを行う。

    Args:
        src: コピー元パス
        dst: コピー先パス
    """
    if src is None or dst is None:
        return None
    check_exists(src)
    check_not_exists(dst)
    make_parent_dir(dst)
    if os.path.isfile(src):
        shutil.copy2(src, dst)
    else:
        shutil.copytree(src, dst)


def move(src: Optional[str], dst: Optional[str]) -> None:
    """指定パスの移動を行う。

    Args:
        src: 移動元パス
        dst: 移動先パス
    """
    if src is None or dst is None:
        return None
    check_exists(src)
    check_not_exists(dst)
    make_parent_dir(dst)
    shutil.move(src, dst)


def delete(target: Optional[str]) -> None:
    """対象パスの削除を行う。

    Args:
        target: 対象パス
    """
    if target is None:
        return None
    check_exists(target)
    if os.path.isfile(target):
        os.remove(target)
    else:
        shutil.rmtree(target)


def clear_dir(root: Optional[str]) -> None:
    """ディレクトリ配下のファイル、ディレクトリを再帰的に削除する。

    Args:
        root: 対象パス
    """
    if root is None:
        return None
    if not os.path.exists(root):
        return None
    paths = get_paths(root, lambda p: p != root)
    for path in reversed(paths):
        if os.path.isfile(path):
            os.remove(path)
        else:
            os.rmdir(path)


def get_times(path: Optional[str]) \
        -> Tuple[Optional[datetime], Optional[datetime], Optional[datetime]]:
    """パスの日時を取得する。

    Args:
        path: 対象パス

    Returns:
        作成日時、更新日時、アクセス日時
    """
    if path is None:
        return (None, None, None)
    if not os.path.exists(path):
        return (None, None, None)
    stat = os.stat(path)
    return (datetimes.get_from_utc(stat.st_ctime),
            datetimes.get_from_utc(stat.st_mtime),
            datetimes.get_from_utc(stat.st_atime))


def get_created(path: Optional[str]) -> Optional[datetime]:
    """パスの作成日時を取得する。

    Args:
        path: 対象パス

    Returns:
        作成日時
    """
    result, _, _ = get_times(path)
    return result


def get_updated(path: Optional[str]) -> Optional[datetime]:
    """パスの更新日時を取得する。

    Args:
        path: 対象パス

    Returns:
        更新日時
    """
    _, result, _ = get_times(path)
    return result


def get_accessed(path: Optional[str]) -> Optional[datetime]:
    """パスのアクセス日時を取得する。

    Args:
        path: 対象パス

    Returns:
        アクセス日時
    """
    _, _, result = get_times(path)
    return result


def modify_times(path: Optional[str],
                 updated: datetime = None, accessed: datetime = None) -> None:
    """パスの日時を変更する。

    Args:
        path: 対象パス
        updated: 更新日時
        accessed: アクセス日時
    """
    if path is None:
        return
    if not os.path.exists(path):
        return
    if updated is None:
        updated = get_updated(path)
    updated_utc = datetimes.to_utc(updated or get_updated(path))
    accessed_utc = datetimes.to_utc(accessed or get_accessed(path))
    if updated_utc is None or accessed_utc is None:
        return
    os.utime(path, (accessed_utc, updated_utc))


def get_prefix_suffix(path: Optional[str]) \
        -> Tuple[Optional[str], Optional[str]]:
    """パスのファイル名、拡張子を取得する。

    Args:
        path: 対象パス

    Returns:
        パスのファイル名（拡張子を除いた部分）
        パスの拡張子
    """
    if path is None:
        return None, None
    basename = os.path.basename(path)
    idx = basename.rfind(".")
    if idx <= 0 or idx >= len(basename) - 1:
        return basename, None
    return basename[0:idx], basename[idx + 1:]


def get_prefix(path: Optional[str]) -> Optional[str]:
    """パスのファイル名（拡張子を除いた部分）を取得する。

    Args:
        path: 対象パス

    Returns:
        パスのファイル名（拡張子を除いた部分）
    """
    result, _ = get_prefix_suffix(path)
    return result


def get_suffix(path: Optional[str]) -> Optional[str]:
    """パスの拡張子を取得する。

    Args:
        path: 対象パス

    Returns:
        パスの拡張子
    """
    _, result = get_prefix_suffix(path)
    return result
