"""Simple inventory management with safe I/O, input validation, and clean error handling."""

from __future__ import annotations

import json
from datetime import datetime
from typing import List, Optional, Dict

# Global inventory store
stock_data: Dict[str, int] = {}


def add_item(item: str = "default", qty: int = 0, logs: Optional[List[str]] = None) -> None:
    """Add quantity to an item in the inventory, recording an optional log entry."""
    if not isinstance(item, str) or not item:
        raise ValueError("item must be a non-empty string")
    if not isinstance(qty, int):
        raise ValueError("qty must be an integer")
    if qty < 0:
        raise ValueError("qty must be non-negative")

    if logs is None:
        logs = []

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now().isoformat(timespec='seconds')}: Added {qty} of {item}")


def remove_item(item: str, qty: int) -> bool:
    """Remove quantity from an item; returns True if changed, False if item missing."""
    if not isinstance(item, str) or not item:
        raise ValueError("item must be a non-empty string")
    if not isinstance(qty, int) or qty <= 0:
        raise ValueError("qty must be a positive integer")

    if item not in stock_data:
        return False

    new_qty = stock_data[item] - qty
    if new_qty > 0:
        stock_data[item] = new_qty
    else:
        # remove item entirely if depleted or negative after removal
        del stock_data[item]
    return True


def get_qty(item: str) -> int:
    """Get current quantity for an item; returns 0 if not present."""
    if not isinstance(item, str) or not item:
        raise ValueError("item must be a non-empty string")
    return stock_data.get(item, 0)


def load_data(file_path: str = "inventory.json") -> None:
    """Load inventory from a JSON file into the global stock_data."""
    stock_data
    with open(file_path, "r", encoding="utf-8") as f:
        loaded = json.load(f)
        # Ensure data integrity: coerce keys to str and values to int >= 0
        stock_data = {
            str(k): int(v) for k, v in loaded.items() if isinstance(v, (int, float)) and int(v) >= 0
        }


def save_data(file_path: str = "inventory.json") -> None:
    """Persist inventory to a JSON file."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(stock_data, f, ensure_ascii=False, indent=2)


def print_data() -> None:
    """Print a human-readable report of inventory items."""
    print("Items Report")
    for name, qty in stock_data.items():
        print(f"{name} -> {qty}")


def check_low_items(threshold: int = 5) -> list[str]:
    """Return items whose quantity is strictly below the threshold."""
    if not isinstance(threshold, int) or threshold < 0:
        raise ValueError("threshold must be a non-negative integer")
    return [name for name, qty in stock_data.items() if qty < threshold]


def main() -> None:
    """Example workflow for exercising main functions."""
    add_item("apple", 10)
    add_item("banana", 2)

    remove_item("apple", 3)          # valid removal
    remove_item("orange", 1)         # non-existent; safely returns False

    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())

    save_data()
    load_data()
    print_data()


if __name__ == "__main__":
    main()
