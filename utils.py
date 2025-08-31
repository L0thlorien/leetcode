import json
from typing import Any, Dict, Iterable, List

# -----------------------------------------------------------------------------
# Ввод/вывод и утилиты
# -----------------------------------------------------------------------------

def parse_json_input(raw: str) -> Dict[str, Any]:
    """Парсит JSON-строку во входные аргументы `solve(...)`.

    Подразумевается формат:
      {"nums": [2,7,11,15], "target": 9}

    Args:
        raw: Строка JSON.

    Returns:
        Словарь аргументов для Solution.solve(**args).

    Raises:
        ValueError: Если невалидный JSON.
    """
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON input: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("Top-level JSON must be an object with named fields.")
    return data


def pretty_dump(obj: Any) -> str:
    """Красивый JSON-дамп результата для CLI/отладки."""
    return json.dumps(obj, ensure_ascii=False, indent=2)

