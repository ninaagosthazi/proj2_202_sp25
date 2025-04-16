## 🌿 CSC 202 – Assignment 2: Linked Lists and Filtering CO₂ Emissions

---

### 🚨 URGENT — GitHub Codespaces Users

If you are using GitHub Codespaces:  
**Immediately after cloning the repo, open the terminal and run:**

```bash
git pull --no-rebase
```

This is required due to a known **GitHub Classroom bug**.  
If you skip this, your test files may not be synced correctly and your work may be misgraded.

---

### 📦 Overview

In this assignment, you’ll build a linked list of structured data rows based on real-world climate data — specifically, CO₂-equivalent emissions from around the world. You’ll practice:

- Using `@dataclass(frozen=True)` to define structured records  
- Recursively building and filtering linked lists  
- Reading and parsing multi-line CSV files  

> ✅ **All functions in this assignment must be external functions** — do not define methods inside classes.

---

## ✅ Task 1: Define Your Linked List Structure

You will be building a custom linked list of **rows** representing individual records in the CO₂ emissions dataset.

### 🧩 Create the following:

- A `Row` class to store one line of emissions data  
- A linked list class where each node contains a Row object

Each row of the CSV file includes the following fields:

```plaintext
"country"
"year"
"electricity_and_heat_co2_emissions"
"electricity_and_heat_co2_emissions_per_capita"
"energy_co2_emissions"
"energy_co2_emissions_per_capita"
"total_co2_emissions_excluding_lucf"
"total_co2_emissions_excluding_lucf_per_capita"
```

You will need to convert string values into appropriate types (e.g., float or int), and use `None` for missing data (`""` in the CSV).

> You must use `@dataclass(frozen=True)` for all class definitions.  
> ❗ **Reminder**: All logic must be implemented as external functions.

---

## ✅ Task 2: Reading the CSV File

### 🔧 Write the following function:

```python
read_csv_lines(filename: str) -> LinkedList
```

- Uses the `csv.reader` class to load rows  
- Validates the header row  
- Converts each row into a `Row` object  
- Builds and returns a linked list of all rows (in any order is fine)

> 💡 We suggest writing a **helper function**:  
> `def parse_row(fields: list[str]) -> Row`  
> to handle data conversion.

> ❗ All functionality must be implemented in **external functions** — not inside any class.

Set the recursion limit at the top of your file:
```python
import sys
sys.setrecursionlimit(10_000)
```

---

## ✅ Task 3: Count Rows

### ✍️ Write:

```python
listlen(data: LinkedList) -> int
```

This recursively returns the number of rows in the linked list.

> ❗ Use external functions only — do not define `.length()` as a method.

---

## ✅ Task 4: General Filtering

You will build a generic recursive filter that supports multiple types of queries.

### ✍️ Write:

```python
filter_rows(
    data: LinkedList,
    field_name: str,
    comparison: str,
    value: Union[str, float, int]
) -> LinkedList
```

- `field_name`: one of the CSV column names  
- `comparison`: `"less_than"`, `"greater_than"`, or `"equal"`  
- `value`: the value to compare against  

### ⚠️ Rules:
- Only `"equal"` is allowed for the `"country"` field  
- All numeric fields support `"less_than"` and `"greater_than"`  
- Missing data (i.e., `None`) should be skipped  

> ❗ Must be implemented as a standalone external function.

---

## 🧪 Task 6: Tests and Design Recipe

For each function:
- Write a **purpose statement**  
- Include **type hints**  
- Create **tests** using `unittest` in a file called `test_student.py`

You should define your own small CSV file with 5–10 rows for testing.  
Missing values (`""`) should be handled using `None`.

> ❗ No methods inside your data classes — write only **external functions**.

---

## 🔧 Setup and Restrictions

Your file should include the following at the top:

```python
import sys
import csv
from typing import *
from dataclasses import dataclass
import unittest
import math

sys.setrecursionlimit(10_000)
```

Do **not** import any other libraries. Your submission must be compatible with **Python 3.12.3**.

---

## 📤 Handin Instructions

Push the following files to your GitHub Classroom repo:

- `proj2.py` – your main implementation  
- `test_student.py` – your test suite  
- `sample.csv` – a small file for testing (optional but recommended)
