import unittest
import sqlite3
from app import get_employees_by_department

class TestFiltering(unittest.TestCase):

    def setUp(self):
        """Setup a temporary in-memory database for testing."""
        self.db = sqlite3.connect(':memory:')
        self.db.execute(
            'CREATE TABLE employees (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, surname TEXT, experience INTEGER, responsibilities TEXT, department TEXT)'
        )
        self.db.execute(
            'INSERT INTO employees (name, surname, experience, responsibilities, department) VALUES (?, ?, ?, ?, ?)',
            ('John', 'Doe', 5, 'Project Manager', 'IT'),
        )
        self.db.execute(
            'INSERT INTO employees (name, surname, experience, responsibilities, department) VALUES (?, ?, ?, ?, ?)',
            ('Jane', 'Smith', 3, 'Software Engineer', 'IT'),
        )
        self.db.execute(
            'INSERT INTO employees (name, surname, experience, responsibilities, department) VALUES (?, ?, ?, ?, ?)',
            ('Peter', 'Jones', 7, 'Data Analyst', 'Data'),
        )
        self.db.commit()

    def tearDown(self):
        """Close the database connection after each test."""
        self.db.close()

    def test_filter_by_existing_department(self):
        """Test filtering by an existing department (case-insensitive)."""
        # Arrange
        department = 'IT'

        # Act
        employees = get_employees_by_department(self.db, department)

        # Assert
        self.assertEqual(len(employees), 2)  # Expect two employees in the IT department
        self.assertIn({'id': 1, 'name': 'John', 'surname': 'Doe', 'experience': 5, 'responsibilities': 'Project Manager', 'department': 'IT'}, employees)
        self.assertIn({'id': 2, 'name': 'Jane', 'surname': 'Smith', 'experience': 3, 'responsibilities': 'Software Engineer', 'department': 'IT'}, employees)

    def test_filter_by_non_existing_department(self):
        """Test filtering by a non-existing department."""
        # Arrange
        department = 'Marketing'

        # Act
        employees = get_employees_by_department(self.db, department)

        # Assert
        self.assertEqual(len(employees), 0)  # Expect no employees in the Marketing department

    def test_filter_by_case_insensitive_department(self):
        """Test case-insensitive filtering by department."""
        # Arrange
        department = 'data'  # Lowercase

        # Act
        employees = get_employees_by_department(self.db, department)

        # Assert
        self.assertEqual(len(employees), 1)  # Expect one employee in the Data department
        self.assertIn({'id': 3, 'name': 'Peter', 'surname': 'Jones', 'experience': 7, 'responsibilities': 'Data Analyst', 'department': 'Data'}, employees)

    def test_get_all_employees_when_no_department_provided(self):
        """Test retrieving all employees when no department is provided."""
        # Arrange
        department = None

        # Act
        employees = get_employees_by_department(self.db, department)

        # Assert
        self.assertEqual(len(employees), 3)  # Expect all 3 employees

if __name__ == '__main__':
    unittest.main()
