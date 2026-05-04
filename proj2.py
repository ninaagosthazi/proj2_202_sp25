import sys
import csv
import math
from dataclasses import dataclass
from typing import *

sys.setrecursionlimit(10000)

# Put your data definitions first!

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





# Then your functions.

# ...
