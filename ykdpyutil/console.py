from ykdpyutil import texts


class LinePrinter:
    """同一行への出力を行う。

    Attributes:
        max_width: 行の最大幅
        fillchar: 空白埋め文字
    """

    def __init__(self, max_width=120, fillchar=" "):
        """
        Args:
            max_width: 行の最大幅(default: 120)
            fillchar: 空白埋め文字(default: 半角スペース)
        """
        self.max_width = max_width
        self.fillchar = fillchar

    def print(self, text):
        """文字列を出力する。

        Args:
            text: 出力する文字列
        """
        text_width = texts.width(text)
        text_length = len(text)
        if text_width < self.max_width:
            text = text.ljust(text_length + self.max_width -
                              text_width, self.fillchar)
        else:
            t = ""
            for c in text:
                if texts.width(t + c) > self.max_width:
                    text = t
                    break
                t = t + c
        print("\r" + text, end="")
