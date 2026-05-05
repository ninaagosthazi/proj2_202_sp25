from __future__ import annotations
import sys
import csv
from typing import *
from dataclasses import dataclass
import unittest
import math

sys.setrecursionlimit(10_000)

# Row dataclass
@dataclass(frozen=True)
class Row:
    country: str
    year: int
    electricity_and_heat_co2_emissions: Optional[float]
    electricity_and_heat_co2_emissions_per_capita: Optional[float]
    energy_co2_emissions: Optional[float]
    energy_co2_emissions_per_capita: Optional[float]
    total_co2_emissions_excluding_lucf: Optional[float]
    total_co2_emissions_excluding_lucf_per_capita: Optional[float]

# Node dataclass
@dataclass(frozen=True)
class Node:
    value: Row
    next: Optional[Node]

# Project functions
def string_to_float(value: str) -> Optional[float]:
    """
    Purpose: A helper function that converts a CSV string into a float (or None if the value is missing).
    """
    if value == "":
        return None
    return float(value)

def parse_row(fields: list[str]) -> Row:
    """
    Purpose: A helper function that converts one CSV row, stored as a list of strings, into a Row object.
    """
    if len(fields) < 8:
        raise ValueError("Row does not have enough fields: {}".format(fields))

    return Row(country = fields[0],
               year = int(fields[1]),
               electricity_and_heat_co2_emissions = string_to_float(fields[2]),
               electricity_and_heat_co2_emissions_per_capita = string_to_float(fields[3]),
               energy_co2_emissions = string_to_float(fields[4]),
               energy_co2_emissions_per_capita = string_to_float(fields[5]),
               total_co2_emissions_excluding_lucf = string_to_float(fields[6]),
               total_co2_emissions_excluding_lucf_per_capita = string_to_float(fields[7]))

def build_linked_list(rows: list[list[str]], index: int) -> Optional[Node]:
    """
    Purpose: A helper function that builds a linked list from a list of CSV rows.
    """
    if index >= len(rows):
        return None

    current_row: list[str] = rows[index]

    if len(current_row) < 8 or all(field.strip() == "" for field in current_row):
        return build_linked_list(rows, index + 1)

    return Node(parse_row(current_row), build_linked_list(rows, index + 1))

def read_csv_lines(filename: str) -> Optional[Node]:
    """
    Purpose: A function that reads a CSV file, validates its header, converts each row into a Row,
    and builds a linked list of Node objects.
    """
    with open(filename, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        lines = list(reader)

    if len(lines) == 0:
        raise ValueError("CSV file is empty")

    return build_linked_list(lines[1:], 0)

def listlen(data: Node | None) -> int:
    """
    Purpose: A function that counts the number of rows in a linked list.
    """
    if data is None:
        return 0
    return 1 + listlen(data.next)

def row_matches(row: Row, field_name: str, comparison: str, value: Union[str, float, int]) -> bool:
    """
    Purpose: Helper function that checks whether one Row matches one filter conditions.
    """
    row_value = getattr(row, field_name)

    if row_value is None:
        return False

    if comparison == "equal":
        return row_value == value

    if comparison == "less_than":
        return row_value < value

    if comparison == "greater_than":
        return row_value > value

    raise ValueError("Invalid comparison: {}".format(comparison))

def filter_rows(data: Optional[Node], field_name: str, comparison: str, value: Union[str, float, int]) -> Optional[Node]:
    """
    Purpose: A function that filters a linked list of Row data using a field name, comparison type, and comparison value.
    """
    if data is None:
        return None

    filtered_rest = filter_rows(data.next, field_name, comparison, value)

    if row_matches(data.value, field_name, comparison, value):
        return Node(data.value, filtered_rest)

    return filtered_rest