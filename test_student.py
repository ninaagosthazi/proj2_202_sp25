import unittest
from proj2 import (
    Row,
    Node,
    parse_row,
    read_csv_lines,
    listlen,
    filter_rows,
    string_to_float
)

class TestRowAndNode(unittest.TestCase):

    def test_row_instantiation(self):
        r = Row(
            country="Mexico",
            year=1990,
            electricity_and_heat_co2_emissions=10.5,
            electricity_and_heat_co2_emissions_per_capita=0.9,
            energy_co2_emissions=15.0,
            energy_co2_emissions_per_capita=1.2,
            total_co2_emissions_excluding_lucf=20.3,
            total_co2_emissions_excluding_lucf_per_capita=1.7
        )

        self.assertEqual(r.country, "Mexico")
        self.assertEqual(r.year, 1990)
        self.assertEqual(r.energy_co2_emissions, 15.0)

    def test_node_instantiation(self):
        r = Row("USA", 2020, 1000.0, 15.0, 2000.0, 30.0, 5000.0, 75.0)
        n = Node(value=r, next=None)

        self.assertEqual(n.value.country, "USA")
        self.assertIsNone(n.next)

    def test_node_chain(self):
        r1 = Row("A", 2000, 1.0, 0.1, 2.0, 0.2, 3.0, 0.3)
        r2 = Row("B", 2001, 1.1, 0.2, 2.1, 0.3, 3.1, 0.4)

        n2 = Node(value=r2, next=None)
        n1 = Node(value=r1, next=n2)

        self.assertEqual(n1.value.country, "A")
        self.assertEqual(n1.next.value.country, "B")


class TestParsing(unittest.TestCase):

    def test_string_to_float_regular_value(self):
        self.assertEqual(string_to_float("3.5"), 3.5)

    def test_string_to_float_missing_value(self):
        self.assertIsNone(string_to_float(""))

    def test_parse_row_full_data(self):
        row = parse_row([
            "USA",
            "1990",
            "100.0",
            "1.5",
            "200.0",
            "2.5",
            "300.0",
            "3.5"
        ])

        self.assertIsInstance(row, Row)
        self.assertEqual(row.country, "USA")
        self.assertEqual(row.year, 1990)
        self.assertEqual(row.electricity_and_heat_co2_emissions, 100.0)
        self.assertEqual(row.total_co2_emissions_excluding_lucf_per_capita, 3.5)

    def test_parse_row_missing_numeric_data(self):
        row = parse_row([
            "Andorra",
            "2010",
            "",
            "",
            "50.0",
            "",
            "70.0",
            ""
        ])

        self.assertEqual(row.country, "Andorra")
        self.assertEqual(row.year, 2010)
        self.assertIsNone(row.electricity_and_heat_co2_emissions)
        self.assertEqual(row.energy_co2_emissions, 50.0)
        self.assertIsNone(row.energy_co2_emissions_per_capita)


class TestListLength(unittest.TestCase):

    def test_listlen_none(self):
        self.assertEqual(listlen(None), 0)

    def test_listlen_one_node(self):
        r = Row("USA", 2020, 100.0, 2.0, 200.0, 3.0, 300.0, 4.0)
        data = Node(r, None)

        self.assertEqual(listlen(data), 1)

    def test_listlen_chain(self):
        r1 = Row("X", 2000, None, None, None, None, None, None)
        r2 = Row("Y", 2001, None, None, None, None, None, None)
        r3 = Row("Z", 2002, None, None, None, None, None, None)

        data = Node(r1, Node(r2, Node(r3, None)))

        self.assertEqual(listlen(data), 3)


class TestFilterRows(unittest.TestCase):

    def test_filter_country_equal(self):
        r1 = Row("USA", 2000, 10.0, 1.0, 100.0, 2.0, 200.0, 3.0)
        r2 = Row("Mexico", 2001, 20.0, 1.5, 150.0, 2.5, 250.0, 3.5)
        r3 = Row("USA", 2002, 30.0, 2.0, 200.0, 3.0, 300.0, 4.0)

        data = Node(r1, Node(r2, Node(r3, None)))
        result = filter_rows(data, "country", "equal", "USA")

        self.assertEqual(listlen(result), 2)
        self.assertEqual(result.value.country, "USA")
        self.assertEqual(result.next.value.country, "USA")

    def test_filter_year_greater_than(self):
        r1 = Row("A", 1990, 10.0, 1.0, 100.0, 2.0, 200.0, 3.0)
        r2 = Row("B", 2005, 20.0, 1.5, 150.0, 2.5, 250.0, 3.5)
        r3 = Row("C", 2010, 30.0, 2.0, 200.0, 3.0, 300.0, 4.0)

        data = Node(r1, Node(r2, Node(r3, None)))
        result = filter_rows(data, "year", "greater_than", 2000)

        self.assertEqual(listlen(result), 2)
        self.assertEqual(result.value.country, "B")
        self.assertEqual(result.next.value.country, "C")

    def test_filter_numeric_less_than(self):
        r1 = Row("A", 2000, 10.0, 1.0, 100.0, 2.0, 200.0, 3.0)
        r2 = Row("B", 2001, 20.0, 1.5, 150.0, 2.5, 250.0, 3.5)
        r3 = Row("C", 2002, 30.0, 2.0, 200.0, 3.0, 300.0, 4.0)

        data = Node(r1, Node(r2, Node(r3, None)))
        result = filter_rows(
            data,
            "electricity_and_heat_co2_emissions",
            "less_than",
            25.0
        )

        self.assertEqual(listlen(result), 2)
        self.assertEqual(result.value.country, "A")
        self.assertEqual(result.next.value.country, "B")

    def test_filter_skips_missing_data(self):
        r1 = Row("A", 2000, None, None, None, None, None, None)
        r2 = Row("B", 2001, 20.0, 1.5, 150.0, 2.5, 250.0, 3.5)

        data = Node(r1, Node(r2, None))
        result = filter_rows(
            data,
            "electricity_and_heat_co2_emissions",
            "greater_than",
            10.0
        )

        self.assertEqual(listlen(result), 1)
        self.assertEqual(result.value.country, "B")

    def test_filter_no_matches(self):
        r1 = Row("A", 2000, 10.0, 1.0, 100.0, 2.0, 200.0, 3.0)
        r2 = Row("B", 2001, 20.0, 1.5, 150.0, 2.5, 250.0, 3.5)

        data = Node(r1, Node(r2, None))
        result = filter_rows(data, "country", "equal", "Canada")

        self.assertIsNone(result)


class TestReadCSVLines(unittest.TestCase):

    def test_read_csv_lines_small_file(self):
        data = read_csv_lines("sample.csv")

        self.assertTrue(data is None or isinstance(data, Node))

    def test_read_csv_lines_length(self):
        data = read_csv_lines("sample.csv")

        self.assertGreaterEqual(listlen(data), 0)


if __name__ == "__main__":
    unittest.main()
