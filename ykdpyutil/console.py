import shutil

from ykdpyutil import texts


class LinePrinter:
    """同一行への出力を行う。

    Attributes:
        max_width: 行の最大幅
        fillchar: 空白埋め文字
    """

    def __init__(
            self,
            max_width=shutil.get_terminal_size().columns,
            fillchar=" "):
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


def confirm(msg="よろしいですか？(y/n) ",
            msg_retry="y または n を入力してください。",
            key_ok="y",
            key_ng="n"):
    """確認入力を行う。

    Args:
        msg: 確認メッセージ(default: よろしいですか？(y/n))
        msg_retry: 入力エラー時メッセージ(default: y または n を入力してください。)
        key_ok: 確認OKキー(default: y)
        key_ng: 確認NGキー(default: n)

    Returns:
        True: 確認OK
        False: 確認NG
    """
    while True:
        print(msg)
        instr = input(msg)
        instr_l = instr.lower()
        if(instr_l == key_ok):
            return True
        elif(instr_l == key_ng):
            return False
        else:
            print(msg_retry)
