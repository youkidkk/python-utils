"""ファイル関連のユーティリティモジュール。
"""
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import cast, List, Optional, Tuple

from ykdpyutil import datetimes

ERR_MSG_NOT_EXISTS = "Target path is not found. Path: {0}"
ERR_MSG_EXISTS = "Target path is already exists. Path: {0}"


def get_files(root: Optional[Path],
              recursive=False,
              path_filter=lambda p: True) -> List[Path]:
    """パス配下のファイルリストを取得する。

    Args:
        root: 対象パス
        recursive: 再帰的検索を行うか
        path_filter: フィルター

    Returns:
        パス配下のファイルリスト
    """
    return get_paths(root,
                     recursive,
                     lambda p: p.is_file() and path_filter(p))


def get_dirs(root: Optional[Path],
             recursive=False,
             path_filter=lambda p: True) -> List[Path]:
    """パス配下のディレクトリリストを取得する。

    Args:
        root: 対象パス
        recursive: 再帰的検索を行うか
        path_filter: フィルター

    Returns:
        パス配下のディレクトリリスト
    """
    return get_paths(root,
                     recursive,
                     lambda p: p.is_dir() and path_filter(p))


def get_paths(root: Optional[Path],
              recursive=False,
              path_filter=lambda p: True) -> List[Path]:
    """パス配下のパスリストを取得する。

    Args:
        root: 対象パス
        recursive: 再帰的検索を行うか
        path_filter: フィルター

    Returns:
        パス配下のパスリスト
    """
    if root is None:
        return []
    cast_root = cast(Path, root)
    plist = cast_root.rglob("*") if recursive else cast_root.glob("*")

    return list(filter(path_filter, plist))


def check_exists(path: Path) -> None:
    """対象パスの存在を確認する。

    Args:
        path: 対象パス
    """
    if not path.exists():
        raise OSError(ERR_MSG_NOT_EXISTS.format(str(path)))


def check_not_exists(path: Path) -> None:
    """対象パスの非存在を確認する。

    Args:
        path: 対象パス
    """
    if path.exists():
        raise OSError(ERR_MSG_EXISTS.format(str(path)))


def make_parent_dir(path: Path) -> None:
    """対象パスの親ディレクトリを作成する。

    Args:
        path: 対象パス
    """
    parent = path.parent
    if not parent.exists():
        parent.mkdir(parents=True)


def copy(src: Optional[Path], dst: Optional[Path]) -> None:
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


def move(src: Optional[Path], dst: Optional[Path]) -> None:
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


def delete(target: Optional[Path]) -> None:
    """対象パスの削除を行う。

    Args:
        target: 対象パス
    """
    if target is None:
        return None
    check_exists(target)
    if target.is_file():
        os.remove(target)
    else:
        shutil.rmtree(target)


def clear_dir(root: Optional[Path]) -> None:
    """ディレクトリ配下のファイル、ディレクトリを再帰的に削除する。

    Args:
        root: 対象パス
    """
    if root is None:
        return None
    if not os.path.exists(root):
        return None
    paths = get_paths(root, recursive=True)
    for path in reversed(paths):
        if path.is_file():
            path.unlink()
        else:
            path.rmdir()


def get_times(path: Optional[Path]) \
        -> Tuple[Optional[datetime], Optional[datetime], Optional[datetime]]:
    """パスの日時を取得する。

    Args:
        path: 対象パス

    Returns:
        作成日時、更新日時、アクセス日時
    """
    if path is None:
        return (None, None, None)
    if not path.exists():
        return (None, None, None)
    stat = path.stat()
    return (datetimes.get_from_utc(stat.st_ctime),
            datetimes.get_from_utc(stat.st_mtime),
            datetimes.get_from_utc(stat.st_atime))


def get_created(path: Optional[Path]) -> Optional[datetime]:
    """パスの作成日時を取得する。

    Args:
        path: 対象パス

    Returns:
        作成日時
    """
    result, _, _ = get_times(path)
    return result


def get_updated(path: Optional[Path]) -> Optional[datetime]:
    """パスの更新日時を取得する。

    Args:
        path: 対象パス

    Returns:
        更新日時
    """
    _, result, _ = get_times(path)
    return result


def get_accessed(path: Optional[Path]) -> Optional[datetime]:
    """パスのアクセス日時を取得する。

    Args:
        path: 対象パス

    Returns:
        アクセス日時
    """
    _, _, result = get_times(path)
    return result


def modify_times(path: Optional[Path],
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


def get_prefix_suffix(path: Optional[Path]) \
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
    basename = path.name
    idx = basename.rfind(os.extsep)
    if idx <= 0 or idx >= len(basename) - 1:
        return basename, None
    return basename[0:idx], basename[idx + 1:]


def get_prefix(path: Optional[Path]) -> Optional[str]:
    """パスのファイル名（拡張子を除いた部分）を取得する。

    Args:
        path: 対象パス

    Returns:
        パスのファイル名（拡張子を除いた部分）
    """
    result, _ = get_prefix_suffix(path)
    return result


def get_suffix(path: Optional[Path]) -> Optional[str]:
    """パスの拡張子を取得する。

    Args:
        path: 対象パス

    Returns:
        パスの拡張子
    """
    _, result = get_prefix_suffix(path)
    return result
