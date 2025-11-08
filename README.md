# LeetCode Solutions

Personal collection of LeetCode problem solutions in Python.

## Quick Start

```bash
# Setup
uv venv
uv pip install -r requirements.txt

# List all solutions
.venv/bin/python leetcode_runner.py list

# Run a solution
.venv/bin/python leetcode_runner.py run 2568 -i '{"nums": [2, 1]}'

# Test a solution
.venv/bin/python leetcode_runner.py test 2568
```

## Structure

- **solutions/** - All solution files
- **leetcode_runner.py** - Centralized CLI and test runner
- **template.py** - Template for new solutions

## Creating New Solutions

```bash
cp template.py solutions/p{number}_{slug}.py
.venv/bin/python leetcode_runner.py test {number}
```
