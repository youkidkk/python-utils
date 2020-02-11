import unittest

import datetime
from pathlib import Path

from ykdpyutil import files

TEST_DIR = Path("tests/test_dir")
TEST_PATHS = [
    Path("tests/test_dir/.test_dir"),
    Path("tests/test_dir/.test_file"),
    Path("tests/test_dir/test_dir"),
    Path("tests/test_dir/test_file"),
    Path("tests/test_dir/test_file.txt"),
    Path("tests/test_dir/.test_dir/.test_dir"),
    Path("tests/test_dir/.test_dir/.test_file"),
    Path("tests/test_dir/.test_dir/test_dir"),
    Path("tests/test_dir/.test_dir/test_file"),
    Path("tests/test_dir/.test_dir/test_file.txt"),
    Path("tests/test_dir/.test_dir/.test_dir/.test_file"),
    Path("tests/test_dir/.test_dir/.test_dir/test_file"),
    Path("tests/test_dir/.test_dir/.test_dir/test_file.txt"),
    Path("tests/test_dir/.test_dir/test_dir/.test_file"),
    Path("tests/test_dir/.test_dir/test_dir/test_file"),
    Path("tests/test_dir/.test_dir/test_dir/test_file.txt"),
    Path("tests/test_dir/test_dir/.test_dir"),
    Path("tests/test_dir/test_dir/.test_file"),
    Path("tests/test_dir/test_dir/test_dir"),
    Path("tests/test_dir/test_dir/test_file"),
    Path("tests/test_dir/test_dir/test_file.txt"),
    Path("tests/test_dir/test_dir/.test_dir/.test_file"),
    Path("tests/test_dir/test_dir/.test_dir/test_file"),
    Path("tests/test_dir/test_dir/.test_dir/test_file.txt"),
    Path("tests/test_dir/test_dir/test_dir/.test_file"),
    Path("tests/test_dir/test_dir/test_dir/test_file"),
    Path("tests/test_dir/test_dir/test_dir/test_file.txt")]
TEMP_DIR = Path("tmp")


class FilesTest(unittest.TestCase):

    def test_get_files(self):
        # テスト対象の実行
        result = files.get_files(TEST_DIR)

        expected = [
            TEST_PATHS[1],
            TEST_PATHS[3],
            TEST_PATHS[4]]
        self.assertListEqual(result, expected)

    def test_get_files_recursive(self):
        # テスト対象の実行
        result = files.get_files(TEST_DIR, recursive=True)

        expected = [
            TEST_PATHS[1],
            TEST_PATHS[3],
            TEST_PATHS[4],
            TEST_PATHS[6],
            TEST_PATHS[8],
            TEST_PATHS[9],
            TEST_PATHS[10],
            TEST_PATHS[11],
            TEST_PATHS[12],
            TEST_PATHS[13],
            TEST_PATHS[14],
            TEST_PATHS[15],
            TEST_PATHS[17],
            TEST_PATHS[19],
            TEST_PATHS[20],
            TEST_PATHS[21],
            TEST_PATHS[22],
            TEST_PATHS[23],
            TEST_PATHS[24],
            TEST_PATHS[25],
            TEST_PATHS[26]]
        self.assertListEqual(result, expected)

    def test_get_files_recursive_filter(self):
        # テスト対象の実行
        result = files.get_files(
            TEST_DIR, recursive=True,
            path_filter=lambda p: p.name.startswith("."))

        expected = [
            TEST_PATHS[1],
            TEST_PATHS[6],
            TEST_PATHS[10],
            TEST_PATHS[13],
            TEST_PATHS[17],
            TEST_PATHS[21],
            TEST_PATHS[24]]
        self.assertListEqual(result, expected)

    def test_get_dirs(self):
        # テスト対象の実行
        result = files.get_dirs(TEST_DIR)

        expected = [
            TEST_PATHS[0],
            TEST_PATHS[2]]
        self.assertListEqual(result, expected)

    def test_get_dirs_recursive(self):
        # テスト対象の実行
        result = files.get_dirs(TEST_DIR, recursive=True)

        expected = [
            TEST_PATHS[0],
            TEST_PATHS[2],
            TEST_PATHS[5],
            TEST_PATHS[7],
            TEST_PATHS[16],
            TEST_PATHS[18]]
        self.assertListEqual(result, expected)

    def test_get_dirs_recursive_filter(self):
        # テスト対象の実行
        result = files.get_dirs(
            TEST_DIR, recursive=True,
            path_filter=lambda p: p.name.startswith("."))

        expected = [
            TEST_PATHS[0],
            TEST_PATHS[5],
            TEST_PATHS[16]]
        self.assertListEqual(result, expected)

    def test_get_paths(self):
        # テスト対象の実行
        result = files.get_paths(TEST_DIR)

        expected = [
            TEST_PATHS[0],
            TEST_PATHS[1],
            TEST_PATHS[2],
            TEST_PATHS[3],
            TEST_PATHS[4]]
        self.assertListEqual(result, expected)

    def test_get_paths_recursive(self):
        # テスト対象の実行
        result = files.get_paths(TEST_DIR, recursive=True)

        expected = TEST_PATHS
        self.assertListEqual(result, expected)

    def test_get_paths_recursive_filter(self):
        # テスト対象の実行
        result = files.get_paths(
            TEST_DIR, recursive=True,
            path_filter=lambda p: p.name.startswith("."))

        expected = [
            TEST_PATHS[0],
            TEST_PATHS[1],
            TEST_PATHS[5],
            TEST_PATHS[6],
            TEST_PATHS[10],
            TEST_PATHS[13],
            TEST_PATHS[16],
            TEST_PATHS[17],
            TEST_PATHS[21],
            TEST_PATHS[24]]
        self.assertListEqual(result, expected)

    def test_check_exists(self):
        # テスト対象の実行
        files.check_exists(TEST_DIR)

    def test_check_exists_raises(self):
        with self.assertRaises(OSError) as cm:
            # テスト対象の実行
            files.check_exists(Path("not_exists_dir"))
        self.assertEqual(
            str(cm.exception),
            files.ERR_MSG_NOT_EXISTS.format("not_exists_dir"))

    def test_check_not_exists(self):
        # テスト対象の実行
        files.check_not_exists(Path("not_exists_dir"))

    def test_check_not_exists_raises(self):
        with self.assertRaises(OSError) as cm:
            # テスト対象の実行
            files.check_not_exists(TEST_DIR)
        self.assertEqual(
            str(cm.exception),
            files.ERR_MSG_EXISTS.format(TEST_DIR))

    def test_check_not_empty(self):
        self.clear_temp_dir()

        # テスト対象の実行
        files.check_empty(TEMP_DIR)

    def test_check_not_empty_raises_not_dir(self):
        with self.assertRaises(OSError) as cm:
            # テスト対象の実行
            files.check_empty(TEST_PATHS[1])
        self.assertEqual(
            str(cm.exception),
            files.ERR_MSG_NOT_DIR.format(TEST_PATHS[1]))

    def test_check_not_empty_raises_not_empty(self):
        with self.assertRaises(OSError) as cm:
            # テスト対象の実行
            files.check_empty(TEST_DIR)
        self.assertEqual(
            str(cm.exception),
            files.ERR_MSG_NOT_EMPTY.format(TEST_DIR))

    def clear_temp_dir(self):
        if TEMP_DIR.exists() and TEMP_DIR.is_file():
            TEMP_DIR.unlink()
        if not TEMP_DIR.exists():
            TEMP_DIR.mkdir()
        files.clear_dir(TEMP_DIR)

    def test_make_parent_dir(self):
        self.clear_temp_dir()
        parent_path = Path(TEMP_DIR, "test")
        target_path = Path(parent_path, "test.txt")

        # テスト対象の実行
        files.make_parent_dir(target_path)

        self.assertTrue(parent_path.exists())
        self.assertTrue(parent_path.is_dir())
        self.assertEqual(len(files.get_paths(parent_path)), 0)

    def test_copy(self):
        self.clear_temp_dir()
        src_path = TEST_DIR
        dst_path = Path(TEMP_DIR, "dst")

        # テスト対象の実行
        files.copy(src_path, dst_path)

        rel_src = list(map(lambda p: p.relative_to(TEST_DIR),
                           files.get_paths(src_path, recursive=True)))
        rel_dst = list(map(lambda p: p.relative_to(dst_path),
                           files.get_paths(dst_path, recursive=True)))
        self.assertListEqual(rel_src, rel_dst)

    def test_move(self):
        self.clear_temp_dir()

        # 移動元ファイルを作成
        temp_src = Path(TEMP_DIR, "temp_src")
        files.copy(TEST_DIR, temp_src)

        # テスト対象の実行
        dst_path = Path(TEMP_DIR, "temp_dst")
        files.move(temp_src, dst_path)

        rel_src = list(map(lambda p: p.relative_to(TEST_DIR),
                           files.get_paths(TEST_DIR, recursive=True)))
        rel_dst = list(map(lambda p: p.relative_to(dst_path),
                           files.get_paths(dst_path, recursive=True)))
        self.assertListEqual(rel_src, rel_dst)

    def test_delete_file(self):
        self.clear_temp_dir()

        target_path = Path(TEMP_DIR, "test_file")
        files.copy(Path(TEST_DIR, "test_file"), target_path)
        files.check_exists(target_path)

        # テスト対象の実行
        files.delete(target_path)

        self.assertFalse(target_path.exists())

    def test_delete_dir(self):
        self.clear_temp_dir()

        target_path = Path(TEMP_DIR, "test_dir")
        files.copy(TEST_DIR, target_path)
        files.check_exists(target_path)

        # テスト対象の実行
        files.delete(target_path)

        self.assertFalse(target_path.exists())

    def test_clear_dir(self):
        self.clear_temp_dir()

        tmp_dst = Path(TEMP_DIR, "test_dir")
        files.copy(TEST_DIR, tmp_dst)
        files.check_exists(tmp_dst)

        # テスト対象の実行
        files.clear_dir(TEMP_DIR)

        self.assertEqual(len(files.get_paths(TEMP_DIR, recursive=True)), 0)

    def test_times_func(self):
        self.clear_temp_dir()

        now = datetime.datetime.now()
        updated = now - datetime.timedelta(weeks=1)
        accessed = now - datetime.timedelta(weeks=2)

        target = Path(TEMP_DIR, "test")
        target.touch()

        files.modify_times(target, updated, accessed)

        target_created = files.get_created(target)
        target_updated = files.get_updated(target)
        target_accessed = files.get_accessed(target)

        self.assertTrue(target_created + datetime.timedelta(hours=1) > now)
        self.assertEqual(target_updated, updated)
        self.assertEqual(target_accessed, accessed)

    def test_get_prefix_suffix_basic(self):
        self.clear_temp_dir()

        target = Path(TEMP_DIR, "test.txt")
        target.touch()

        result_prefix = files.get_prefix(target)
        result_suffix = files.get_suffix(target)

        self.assertEqual(result_prefix, "test")
        self.assertEqual(result_suffix, "txt")

    def test_get_prefix_suffix_nosuffix(self):
        self.clear_temp_dir()

        target = Path(TEMP_DIR, "test")
        target.touch()

        result_prefix = files.get_prefix(target)
        result_suffix = files.get_suffix(target)

        self.assertEqual(result_prefix, "test")
        self.assertIsNone(result_suffix)

    def test_get_prefix_suffix_startdot(self):
        self.clear_temp_dir()

        target = Path(TEMP_DIR, ".test")
        target.touch()

        result_prefix = files.get_prefix(target)
        result_suffix = files.get_suffix(target)

        self.assertEqual(result_prefix, ".test")
        self.assertIsNone(result_suffix)


if __name__ == "__main__":
    unittest.main()
