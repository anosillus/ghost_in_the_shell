# ! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# File name: ghost.py
# First Edit: 2020-01-25
# Last Change: 26-Jan-2020.
"""
# Todolist
1. おばけをプリントする。
2. おばけを綺麗にする。
3. おばけの位置を変えて表示する。(右から左に)
4. 前のおばけを消すことで横に移動してるように見せる。
5. 移動速度を設定し、0.3秒毎に移動させる。
6. おばけを端から端まで移動させる。
7. おばけにフェードイン、フェードアウトさせる。
8. おばけの表われる高さをシェルの真ん中にする。
8. おばけの進行方向を左から右にする。
9. おばけを振動させる。
10. おばけに色をつける。
11. おばけの位置をランダムにする。
12. ランダムに毎秒おばけに色をつける。
13. おばけを無限ループさせる。(qで終了する。)
14. おばけの数を増やす。
"""
import os
import random
import re
import shutil
import sys
import time
import unicodedata

# 「幽霊 AA」などで検索すると出てくる。
BASE_AA_TEXT = """
    　　　／￣￣＼
    　_　/<●><●>ヽ　 _
    彡｜f　　　　　|　/ミ
    `//_|　ヽ二フ　|_//
    　￣ヽ　　　　 |￣
    　　 ヽ　　　　|
    　　　 ＼　　　ヽ_／/
    　　　　 ＼＿＿＿_／
    """

HARF_WIDTH_SPACE = " "
MOVE_STEP = 1


def todo1():
    # 1. おばけをプリントする。
    print("hello, world!")  # pythonの文法の確認
    print(BASE_AA_TEXT)  # Task1


def todo2():  # todolist 1-5
    """
    2. おばけを綺麗にする。
    """

    # AAで一般に用いられる全角スペースはターミナルのフォントによっては表示が上手くいかないことがあるので半角に直している。
    # それでも全角が一部に入るので環境によっては辛いこともある。
    aa_text = BASE_AA_TEXT.replace("　", HARF_WIDTH_SPACE * 2)
    print(aa_text)  # Task2


def change_zenkaku_space_into_hankaku(text):
    return text.replace("　", HARF_WIDTH_SPACE * 2)


def todo3():  # todolist 1-5
    """
    3. おばけの位置を変えて表示する。(右から左に)
    """

    aa_text = change_zenkaku_space_into_hankaku(BASE_AA_TEXT)

    # 複数の空白を数を変化させながら挿入し続けることで移動させる。
    last_place = 10  # last_place > first_place
    first_place = 1  # first_place > 0

    # おばけの移動はfor文でループを作ることで実装する。ループしながらスペースの数をmove_stepの数だけ変えている。

    for blank_count in range(first_place, last_place, MOVE_STEP):
        branks_s = HARF_WIDTH_SPACE * blank_count

        # ======= 移動の実装例1 (listとfor文を使うパターン) ================
        for text_chunk in aa_text.splitlines():
            print(branks_s + text_chunk)  # Task3
            pass
        # ===================================================================

        """
        ======== 移動の実装例2 (listを使わない)=========
        print(aa_text.replace("\n", "\n" + branks_s))
        # print(re.sub("^", branks_s, aa_text, flags=re.MULTILINE))
        ===================================================================
        """


def todo3_another():
    aa_text = change_zenkaku_space_into_hankaku(BASE_AA_TEXT)

    # 複数の空白を数を変化させながら挿入し続けることで移動させる。
    last_place = 10  # last_place > first_place
    first_place = 1  # first_place > 0

    # yieldを使う。
    def blank_generator():
        for blank_length in range(first_place, last_place, MOVE_STEP):
            yield blank_length * HARF_WIDTH_SPACE

    for branks_s in blank_generator():
        print(re.sub("^", branks_s, aa_text, flags=re.MULTILINE))


def todo4():
    """
    4. 前のおばけを消すことで横に移動してるように見せる。
    """

    aa_text = change_zenkaku_space_into_hankaku(BASE_AA_TEXT)

    # 複数の空白を数を変化させながら挿入し続けることで移動させる。
    last_place = 10  # last_place > first_place
    first_place = 1  # first_place > 0

    def blank_generator():
        for blank_length in range(first_place, last_place, MOVE_STEP):
            yield blank_length * HARF_WIDTH_SPACE

    # おばけを表示する前に画面を綺麗にする。
    os.system("clear")  # 前のおばけを画面から消す。

    for branks_s in blank_generator():
        print(re.sub("^", branks_s, aa_text, flags=re.MULTILINE))
        time.sleep(0.3)  # 0.3秒間停止する。
        os.system("clear")  # 前のおばけを画面から消す。


def todo5():
    """
    5. おばけをターミナルのサイズを参考に移動させる。
    """
    aa_text = change_zenkaku_space_into_hankaku(BASE_AA_TEXT)

    columns, rows = shutil.get_terminal_size()
    # print(columns)  # ターミナルの横の長さが取得できている。
    # printの結果はclearですぐに消されてしますので注意。

    """ shutilを使わなくとも同じことはできる。
    rows, cols = [
        int(x) for x in os.popen("stty size").readline().strip().split()
    ]
    print(cols)
    """

    first_place = 0  # first_place < last_place
    last_place = columns

    # aa_height = len(aa_text.splitlines()) # こちらでも可能
    aa_height = aa_text.count(os.linesep)

    new_lines_for_aa_in_the_middle = (rows - aa_height) // 2

    # 5秒より長くは待ちたくないので、スピード調節を行っている。
    aa_speed = 5 / abs(last_place - first_place) / MOVE_STEP

    def blank_generator():
        for blank_length in range(first_place, last_place, MOVE_STEP):
            yield blank_length * HARF_WIDTH_SPACE

    # os.system("clear")
    for branks_s in blank_generator():
        print("\n" * new_lines_for_aa_in_the_middle)
        print(re.sub("^", branks_s, aa_text, flags=re.MULTILINE))
        time.sleep(aa_speed)
        os.system("clear")


def todo6():
    """ 6. おばけの進行方向を左から右にする。 """

    aa_text = change_zenkaku_space_into_hankaku(BASE_AA_TEXT)
    columns, rows = shutil.get_terminal_size()

    first_place = columns
    last_place = 0

    aa_height = aa_text.count(os.linesep)
    new_lines_for_aa_in_the_middle = (rows - aa_height) // 2

    aa_direction = -1  # 左向きならスペースの数をマイナスに変化させる。
    aa_speed = 5 / abs(last_place - first_place) / MOVE_STEP

    def blank_generator():
        for blank_length in range(
            first_place, last_place, aa_direction * MOVE_STEP
        ):
            yield blank_length * HARF_WIDTH_SPACE

    # os.system("clear")

    for branks_s in blank_generator():
        print("\n" * new_lines_for_aa_in_the_middle)
        print(re.sub("^", branks_s, aa_text, flags=re.MULTILINE))
        time.sleep(aa_speed)
        os.system("clear")


def get_east_asian_width_count(text):
    count = 0

    for c in text:
        if unicodedata.east_asian_width(c) in "FWA":
            count += 2
        else:
            count += 1

    return count


def todo7():  # todolist 6-8
    """ 7. おばけを端から端まで移動させる。(フェードインフェードアウトはしない) """
    aa_text = change_zenkaku_space_into_hankaku(BASE_AA_TEXT)
    columns, rows = shutil.get_terminal_size()

    aa_width = 0

    for text_chunk in aa_text.splitlines():
        if get_east_asian_width_count(text_chunk) > aa_width:
            aa_width = get_east_asian_width_count(text_chunk)

    first_place = columns - aa_width
    last_place = 0

    aa_height = len(aa_text.splitlines())
    new_lines_for_aa_in_the_middle = (rows - aa_height) // 2

    aa_direction = -1  # 左向きならスペースの数をマイナスに変化させる。
    aa_speed = 5 / abs(last_place - first_place) / MOVE_STEP

    def blank_generator():
        for blank_length in range(
            first_place, last_place, aa_direction * MOVE_STEP
        ):
            yield blank_length * HARF_WIDTH_SPACE

    # os.system("clear")

    for branks_s in blank_generator():
        print("\n" * new_lines_for_aa_in_the_middle)
        print(re.sub("^", branks_s, aa_text, flags=re.MULTILINE))
        time.sleep(aa_speed)
        os.system("clear")


def todo8():
    """ 8. おばけを振動させる。 """
    aa_text = change_zenkaku_space_into_hankaku(BASE_AA_TEXT)
    columns, rows = shutil.get_terminal_size()

    aa_width = 0

    for text_chunk in aa_text.splitlines():
        if get_east_asian_width_count(text_chunk) > aa_width:
            aa_width = get_east_asian_width_count(text_chunk)

    first_place = columns - aa_width
    last_place = 0

    aa_height = len(aa_text.splitlines())
    new_lines_for_aa_in_the_middle = (rows - aa_height) // 2

    aa_direction = -1  # 左向きならスペースの数をマイナスに変化させる。
    aa_speed = 5 / abs(last_place - first_place) / MOVE_STEP

    def blank_generator():
        for blank_length in range(
            first_place, last_place, aa_direction * MOVE_STEP
        ):
            yield blank_length * HARF_WIDTH_SPACE

    # os.system("clear")

    flag = True

    for branks_s in blank_generator():
        if flag:
            print("\n")
            flag = False
        else:
            flag = True
        print("\n" * new_lines_for_aa_in_the_middle)
        print(re.sub("^", branks_s, aa_text, flags=re.MULTILINE))
        time.sleep(aa_speed)
        os.system("clear")


def get_aa_width(aa_text):
    aa_width = 0

    for text_chunk in aa_text.splitlines():
        if get_east_asian_width_count(text_chunk) > aa_width:
            aa_width = get_east_asian_width_count(text_chunk)

    return aa_width


def calc_vartical_aa_positon(aa_text):
    _, rows = shutil.get_terminal_size()
    aa_height = len(aa_text.splitlines())
    new_lines_for_aa_in_the_middle = (
        rows - aa_height
    ) // 2  # おばけを中央に置くために必要な改行の数(整数値)を求める。

    return new_lines_for_aa_in_the_middle


def print_aa_with_horizontal_moved_position(aa_text, blank):
    print(re.sub("^", blank, aa_text, flags=re.MULTILINE))

    return 0


def todo9():
    # 9. おばけの位置をランダムにする。
    aa_text = change_zenkaku_space_into_hankaku(BASE_AA_TEXT)

    first_place = columns - get_aa_width(aa_text)
    last_place = 0

    aa_direction = -1
    aa_speed = 5 / abs(last_place - first_place) / MOVE_STEP

    def blank_generator():
        for blank_length in range(
            first_place, last_place, aa_direction * MOVE_STEP
        ):
            yield blank_length * HARF_WIDTH_SPACE

    os.system("clear")

    flag = True

    for branks_s in blank_generator():
        """
        _, rows = shutil.get_terminal_size()
        aa_height = aa_text.count('\n')
        print("\n" * random.randint(0, rows - aa_height))
        """
        print(
            "\n"
            * random.randint(
                0, shutil.get_terminal_size()[1] - aa_text.count(os.linesep)
            )
        )
        print_aa_with_horizontal_moved_position(aa_text, branks_s)
        time.sleep(aa_speed)
        os.system("clear")


if __name__ == "__main__":
    # 10. おばけを無限ループさせる。(qで終了する。)
    # 11. おばけの数を増やす。

    todo9()
