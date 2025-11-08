#!/usr/bin/env python3
"""
Centralized runner for all LeetCode solutions.
Provides CLI interface for running, testing, and managing solutions.
"""

import importlib
import importlib.util
import inspect
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import click

from base import parse_json_input, pretty_dump


def find_solutions() -> List[Path]:
    """Find all solution files in the solutions directory."""
    solutions_dir = Path(__file__).parent / "solutions"
    if not solutions_dir.exists():
        return []
    return sorted(solutions_dir.glob("p*.py"))


def extract_problem_id(filepath: Path) -> Optional[int]:
    """Extract problem ID from filename like p0001_two_sum.py"""
    match = re.match(r"p(\d+)", filepath.stem)
    return int(match.group(1)) if match else None


def load_solution_module(filepath: Path):
    """Dynamically load a solution module from filepath."""
    spec = importlib.util.spec_from_file_location(filepath.stem, filepath)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {filepath}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[filepath.stem] = module
    spec.loader.exec_module(module)
    return module


def get_solution_class(module):
    """Get the Solution class from a module."""
    if hasattr(module, "Solution"):
        return module.Solution
    raise AttributeError(f"Module {module.__name__} has no Solution class")


def get_test_cases(module) -> List[Dict[str, Any]]:
    """Get test cases from module if they exist."""
    return getattr(module, "test_cases", [])


def extract_metadata(module) -> Dict[str, Any]:
    """Extract metadata from module docstring."""
    docstring = module.__doc__ or ""
    lines = [line.strip() for line in docstring.strip().split("\n") if line.strip()]

    metadata = {
        "title": lines[0] if lines else "Unknown",
        "url": "",
        "difficulty": "Unknown"
    }

    for line in lines:
        if line.startswith("http"):
            metadata["url"] = line
        elif "Difficulty:" in line or "Сложность:" in line:
            parts = line.split(":")
            if len(parts) > 1:
                metadata["difficulty"] = parts[1].strip()

    return metadata


def find_solution_by_id(problem_id: int) -> Optional[Path]:
    """Find solution file by problem ID."""
    solutions = find_solutions()
    for sol in solutions:
        if extract_problem_id(sol) == problem_id:
            return sol
    return None


@click.group(help="LeetCode solutions runner - manage and test all solutions.")
def cli():
    pass


@cli.command("list", help="List all available solutions.")
def list_command():
    """List all solutions with their metadata."""
    solutions = find_solutions()
    if not solutions:
        click.echo("No solutions found in solutions/ directory.")
        return

    click.echo(f"Found {len(solutions)} solution(s):\n")
    for sol_path in solutions:
        problem_id = extract_problem_id(sol_path)
        try:
            module = load_solution_module(sol_path)
            meta = extract_metadata(module)
            click.echo(f"  [{problem_id:4d}] {meta['title']} ({meta['difficulty']})")
        except Exception as e:
            click.echo(f"  [{problem_id:4d}] {sol_path.stem} (error loading: {e})")


@cli.command("run", help="Run a solution with JSON input.")
@click.argument("problem_id", type=int)
@click.option(
    "--input",
    "-i",
    "input_json",
    type=str,
    default=None,
    help="JSON string with input data, e.g., '{\"nums\":[1,2,3],\"target\":3}'",
)
@click.option(
    "--stdin",
    is_flag=True,
    help="Read JSON from stdin (overrides --input).",
)
@click.option(
    "--timeit",
    is_flag=True,
    help="Measure execution time.",
)
def run_command(problem_id: int, input_json: Optional[str], stdin: bool, timeit: bool):
    """Run a solution with provided input."""
    sol_path = find_solution_by_id(problem_id)
    if not sol_path:
        click.echo(f"Error: Solution for problem {problem_id} not found.", err=True)
        sys.exit(1)

    # Get input
    raw = ""
    if stdin:
        raw = sys.stdin.read()
    elif input_json:
        raw = input_json
    else:
        click.echo(
            "Error: No input provided. Use --input or --stdin.",
            err=True
        )
        sys.exit(2)

    # Parse input
    try:
        args = parse_json_input(raw)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(2)

    # Load and run solution
    try:
        module = load_solution_module(sol_path)
        solution_class = get_solution_class(module)
        solution = solution_class()

        # Find the appropriate method to call
        # Try common method names or use the first public method
        method = None
        for name in dir(solution):
            if not name.startswith("_") and callable(getattr(solution, name)):
                method = getattr(solution, name)
                break

        if method is None:
            raise AttributeError("No callable method found in Solution class")

        start = time.perf_counter()
        result = method(**args)
        elapsed_ms = (time.perf_counter() - start) * 1000.0

        click.echo(pretty_dump(result))
        if timeit:
            click.echo(f"\nElapsed: {elapsed_ms:.3f} ms", err=True)

    except Exception as e:
        click.echo(f"Error running solution: {e}", err=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)


@cli.command("test", help="Run tests for a solution.")
@click.argument("problem_id", type=int)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Verbose output."
)
def test_command(problem_id: int, verbose: bool):
    """Run test cases for a solution."""
    sol_path = find_solution_by_id(problem_id)
    if not sol_path:
        click.echo(f"Error: Solution for problem {problem_id} not found.", err=True)
        sys.exit(1)

    try:
        module = load_solution_module(sol_path)
        test_cases = get_test_cases(module)

        if not test_cases:
            click.echo(f"No test cases found for problem {problem_id}.")
            sys.exit(0)

        solution_class = get_solution_class(module)
        solution = solution_class()

        # Find the method to call
        method = None
        for name in dir(solution):
            if not name.startswith("_") and callable(getattr(solution, name)):
                method = getattr(solution, name)
                break

        if method is None:
            raise AttributeError("No callable method found in Solution class")

        passed = 0
        failed = 0

        click.echo(f"Running {len(test_cases)} test(s) for problem {problem_id}...\n")

        for i, case in enumerate(test_cases, 1):
            input_data = case["input"]
            expected = case["expected"]

            try:
                result = method(**input_data)
                if result == expected:
                    passed += 1
                    if verbose:
                        click.echo(f"  Test {i}: PASSED")
                        click.echo(f"    Input: {input_data}")
                        click.echo(f"    Output: {result}")
                else:
                    failed += 1
                    click.echo(f"  Test {i}: FAILED", err=True)
                    click.echo(f"    Input: {input_data}", err=True)
                    click.echo(f"    Expected: {expected}", err=True)
                    click.echo(f"    Got: {result}", err=True)
            except Exception as e:
                failed += 1
                click.echo(f"  Test {i}: ERROR", err=True)
                click.echo(f"    Input: {input_data}", err=True)
                click.echo(f"    Error: {e}", err=True)

        click.echo(f"\nResults: {passed} passed, {failed} failed")
        sys.exit(0 if failed == 0 else 1)

    except Exception as e:
        click.echo(f"Error loading solution: {e}", err=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)


@cli.command("info", help="Show information about a solution.")
@click.argument("problem_id", type=int)
def info_command(problem_id: int):
    """Show metadata and info for a solution."""
    sol_path = find_solution_by_id(problem_id)
    if not sol_path:
        click.echo(f"Error: Solution for problem {problem_id} not found.", err=True)
        sys.exit(1)

    try:
        module = load_solution_module(sol_path)
        meta = extract_metadata(module)

        click.echo(pretty_dump({
            "id": problem_id,
            "title": meta["title"],
            "url": meta["url"],
            "difficulty": meta["difficulty"],
            "file": str(sol_path.name)
        }))
    except Exception as e:
        click.echo(f"Error loading solution: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
