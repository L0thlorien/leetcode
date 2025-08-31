#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LeetCode Task Template
======================

Вставь краткое описание задачи здесь (2–6 предложений).
Сформулируй вход/выход, ограничения и особые случаи.

Ссылка: https://leetcode.com/problems/<slug>/
Сложность: ожидаемая O(...)/O(...)

Примеры:
    >>> # Небольшие doctest-примеры можно оставлять здесь
    >>> example_input = {"nums": [2, 7, 11, 15], "target": 9}
    >>> Solution().solve(**example_input)
    [0, 1]
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
# Метаданные задачи (заполни под себя)
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class TaskMeta:
    """Описание текущей задачи для быстрой навигации и логирования."""

    id: Optional[int] = None
    title: str = "Two Sum"  # ← поменяй название
    url: str = "https://leetcode.com/problems/two-sum/"  # ← поменяй ссылку
    difficulty: str = "Easy"  # Easy | Medium | Hard


META = TaskMeta()


# -----------------------------------------------------------------------------
# Решение
# -----------------------------------------------------------------------------

class Solution:
    """Класс в стиле LeetCode с методом, который вы будете отправлять.

    Рекомендуется:
      - Держать публичный метод с сигнатурой из условия.
      - Делегировать на `solve(...)` (ниже) с теми же аргументами.
      - Хранить вспомогательные приватные методы здесь же.
    """

    # Пример под Two Sum; замени на требуемую сигнатуру для своей задачи.
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        """Отправляемый на LeetCode метод (пример под Two Sum)."""
        return self.solve(nums=nums, target=target)

    # Унифицированная точка входа под локальные запуски/тесты.
    def solve(self, **kwargs: Any) -> Any:
        """Реализация решения. Меняй сигнатуру/тип возврата под задачу.

        Args:
            **kwargs: Именованные аргументы входа (удобно для JSON и тестов).

        Returns:
            Любой тип, требуемый условием задачи.
        """
        # --------- ЗДЕСЬ ТВОЁ РЕШЕНИЕ ---------
        # Пример — Two Sum со словарём индексов:
        nums: List[int] = kwargs["nums"]
        target: int = kwargs["target"]
        seen: Dict[int, int] = {}
        for i, v in enumerate(nums):
            need = target - v
            if need in seen:
                return [seen[need], i]
            seen[v] = i
        return []
        # --------------------------------------

# -----------------------------------------------------------------------------
# Набор тестов (правь под задачу)
# -----------------------------------------------------------------------------

class TestSolution(unittest.TestCase):
    """Мини-набор юнит-тестов. Добавляй кейсы свободно."""

    def setUp(self) -> None:
        self.sut = Solution()

    def test_basic(self) -> None:
        self.assertEqual(
            self.sut.solve(nums=[2, 7, 11, 15], target=9),
            [0, 1],
        )

    def test_no_answer(self) -> None:
        self.assertEqual(self.sut.solve(nums=[1, 2, 3], target=7), [])

    def test_duplicates(self) -> None:
        self.assertEqual(self.sut.solve(nums=[3, 3], target=6), [0, 1])


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

