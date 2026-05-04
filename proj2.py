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
    electricity_and_heat_co2_emissions: float | None
    electricity_and_heat_co2_emissions_per_capita: float | None
    energy_co2_emissions: float | None
    energy_co2_emissions_per_capita: float | None
    total_co2_emissions_excluding_lucf: float | None
    total_co2_emissions_excluding_lucf_per_capita: float | None

# Node dataclass
@dataclass(frozen=True)
class Node:
    value: Row
    next: Node | None

# Header
EXPECTED_HEADER: list[str] = ["country", "year", "electricity_and_heat_co2_emissions", "electricity_and_heat_co2_emissions_per_capita",
                              "energy_co2_emissions", "energy_co2_emissions_per_capita", "total_co2_emissions_excluding_lucf",
                              "total_co2_emissions_excluding_lucf_per_capita"]

def string_to_float(value: str) -> float | None:
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
    return Row(country = fields[0],
               year = int(fields[1]),
               electricity_and_heat_co2_emissions = string_to_float(fields[2]),
               electricity_and_heat_co2_emissions_per_capita = string_to_float(fields[3]),
               energy_co2_emissions = string_to_float(fields[4]),
               energy_co2_emissions_per_capita = string_to_float(fields[5]),
               total_co2_emissions_excluding_lucf = string_to_float(fields[6]),
               total_co2_emissions_excluding_lucf_per_capita = string_to_float(fields[7]))

def build_linked_list(rows: list[list[str]], index: int) -> Node | None:
    """
    Purpose: A helper function that recursively builds a linked list from a list of CSV rows.
    """
    if index >= len(rows):
        return None
    return Node(parse_row(rows[index]), build_linked_list(rows, index + 1))

def read_csv_lines(filename: str) -> Node | None:
    """
    Purpose: A function that reads a CSV file, validates its header, converts each row into a Row,
    and recursively builds a linked list of Node objects.
    """
    with open(filename, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        lines = list(reader)

    if len(lines) == 0:
        raise ValueError("CSV file is empty")
    if lines[0] != EXPECTED_HEADER:
        raise ValueError("Unexpected first line: got {}".format(lines[0]))

    return build_linked_list(lines[1:], 0)
