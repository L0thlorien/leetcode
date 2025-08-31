#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Minimum Impossible OR
======================

You are given a 0-indexed integer array nums.

We say that an integer x is expressible from nums if there exist some integers 0 <= index1 < index2 < ... < indexk < nums.length for which nums[index1] | nums[index2] | ... | nums[indexk] = x. In other words, an integer is expressible if it can be written as the bitwise OR of some subsequence of nums.

Return the minimum positive non-zero integer that is not expressible from nums.

Ссылка: https://leetcode.com/problems/minimum-impossible-or/
Сложность: O(n)

Примеры:
    Example 1:
        Input: nums = [2,1]
        Output: 4
        Explanation: 1 and 2 are already present in the array. We know that 3 is expressible, since nums[0] | nums[1] = 2 | 1 = 3. Since 4 is not expressible, we return 4.

    Example 2:
        Input: nums = [5,3,2]
        Output: 1
        Explanation: We can show that 1 is the smallest number that is not expressible.
"""

from __future__ import annotations
from utils import parse_json_input, pretty_dump

import sys
import time
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

import click
import unittest


# -----------------------------------------------------------------------------
# Метаданные задачи
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class TaskMeta:
    """Описание текущей задачи для быстрой навигации и логирования."""

    id: Optional[int] = 2568
    title: str = "Minimum Impossible OR"
    url: str = "https://leetcode.com/problems/minimum-impossible-or/"
    difficulty: str = "Medium"  # Easy | Medium | Hard


META = TaskMeta()


# -----------------------------------------------------------------------------
# Решение
# -----------------------------------------------------------------------------

class Solution:
    def minImpossibleOR(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        return self.solve(nums=nums)

    def solve(self, **kwargs: Any) -> Any:
        nums: List[int] = kwargs["nums"]
        out = 0
        i = 0
        while True:
            if 2 ** i not in nums:
                out = 2 ** i
                break
            else:
                i += 1
        return out

# -----------------------------------------------------------------------------
# Набор тестов
# -----------------------------------------------------------------------------

class TestSolution(unittest.TestCase):
    def setUp(self) -> None:
        self.sut = Solution()

    def test_example1(self) -> None:
        self.assertEqual(
            self.sut.solve(nums=[2, 1]), 4
        )

    def test_example2(self) -> None:
        self.assertEqual(
            self.sut.solve(nums=[5, 3, 2]), 1
        )

    def test_example3(self) -> None:
        self.assertEqual(
            self.sut.solve(nums=[1,25,2,72]), 4
        )

    def test_example4(self) -> None:
        self.assertEqual(
            self.sut.solve(nums=[1,]), 2
        )

# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------

@click.group(help="LeetCode task runner (single-file).")
def cli() -> None:
    pass


@cli.command("run", help="Запуск решения на JSON-входе.")
@click.option(
    "--input",
    "-i",
    "input_json",
    type=str,
    default=None,
    help="JSON-строка с входными данными. "
    'Напр.: \'{"nums":[2,7,11,15],"target":9}\'',
)
@click.option(
    "--stdin",
    is_flag=True,
    help="Читать JSON из stdin (игнорирует --input).",
)
@click.option(
    "--timeit",
    is_flag=True,
    help="Измерить время выполнения.",
)
def run_command(input_json: Optional[str], stdin: bool, timeit: bool) -> None:
    """CLI: запуск solve(...) с JSON-аргументами."""
    raw = ""
    if stdin:
        raw = sys.stdin.read()
    elif input_json is not None:
        raw = input_json
    else:
        click.echo(
            "Не задано ни --input, ни --stdin. "
            "Смотри: python task.py run --help",
            err=True,
        )
        sys.exit(2)

    try:
        args = parse_json_input(raw)
    except ValueError as e:
        click.echo(str(e), err=True)
        sys.exit(2)

    sol = Solution()
    start = time.perf_counter()
    result = sol.solve(**args)
    elapsed_ms = (time.perf_counter() - start) * 1000.0

    click.echo(pretty_dump(result))
    if timeit:
        click.echo(f"\nElapsed: {elapsed_ms:.3f} ms", err=True)


@cli.command("info", help="Печать метаданных задачи.")
def info_command() -> None:
    click.echo(pretty_dump(META.__dict__))


@cli.command("test", help="Запуск встроенных unit-тестов.")
@click.option(
    "--pattern",
    "-k",
    type=str,
    default="",
    help="Фильтр по имени теста (подстрока).",
)
def test_command(pattern: str) -> None:
    # Формируем suite вручную, чтобы поддержать фильтр -k.
    suite = unittest.TestSuite()
    for name in unittest.defaultTestLoader.getTestCaseNames(TestSolution):
        if pattern and pattern not in name:
            continue
        suite.addTest(TestSolution(name))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    # Возвращаем ненулевой код при падении тестов (для CI).
    sys.exit(0 if result.wasSuccessful() else 1)


# -----------------------------------------------------------------------------
# Точка входа
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    # Примеры:
    #   python task.py info
    #   python task.py run -i '{"nums":[2,7,11,15],"target":9}'
    #   echo '{"nums":[2,7,11,15],"target":9}' | python task.py run --stdin --timeit
    #   python task.py test
    cli()

