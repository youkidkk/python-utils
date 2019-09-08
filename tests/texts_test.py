import unittest

from ykdpyutil import texts


class TextsTest(unittest.TestCase):

    def test_width(self):
        self.assertEqual(texts.width("test"), 4)
        self.assertEqual(texts.width("testテスト"), 10)

    def test_max_width(self):
        text_list = ["a", "abc", "ああ"]
        self.assertEqual(texts.max_width(text_list), 4)

    def test_min_width(self):
        text_list = ["aあ", "abcd", "あああ"]
        self.assertEqual(texts.min_width(text_list), 3)

    def test_reverse(self):
        self.assertEqual(texts.reverse("aあbい"), "いbあa")


if __name__ == "__main__":
    unittest.main()
