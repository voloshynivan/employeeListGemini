from flask import Flask, render_template, abort, g, request
import sqlite3
import click

app = Flask(__name__)

# Database setup
DATABASE = 'employees.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = sqlite3.connect(DATABASE)
        db.execute(
            'CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, surname TEXT, experience INTEGER, responsibilities TEXT, department TEXT)'
        )
        db.commit()
        g._database = db
    return db

def close_db(db):
    if db is not None:
        db.close()

@app.teardown_appcontext
def close_connection(exception):
    close_db(getattr(g, '_database', None))

# Initialize the database with sample data (moved to a function)
def init_db():
    db = get_db()
    db.execute(
        'INSERT INTO employees (name, surname, experience, responsibilities, department) VALUES (?, ?, ?, ?, ?)',
        ('John', 'Doe', 5, 'Project Manager', 'IT'),
    )
    db.execute(
        'INSERT INTO employees (name, surname, experience, responsibilities, department) VALUES (?, ?, ?, ?, ?)',
        ('Jane', 'Smith', 3, 'Software Engineer', 'IT'),
    )
    db.execute(
        'INSERT INTO employees (name, surname, experience, responsibilities, department) VALUES (?, ?, ?, ?, ?)',
        ('Peter', 'Jones', 7, 'Data Analyst', 'Data'),
    )
    db.execute(
        'INSERT INTO employees (name, surname, experience, responsibilities, department) VALUES (?, ?, ?, ?, ?)',
        ('Alice', 'Williams', 2, 'Junior Developer', 'IT'),
    )
    db.execute(
        'INSERT INTO employees (name, surname, experience, responsibilities, department) VALUES (?, ?, ?, ?, ?)',
        ('Bob', 'Brown', 10, 'Senior Architect', 'IT'),
    )
    db.execute(
        'INSERT INTO employees (name, surname, experience, responsibilities, department) VALUES (?, ?, ?, ?, ?)',
        ('Carol', 'Davis', 6, 'Team Lead', 'IT'),
    )
    db.execute(
        'INSERT INTO employees (name, surname, experience, responsibilities, department) VALUES (?, ?, ?, ?, ?)',
        ('David', 'Wilson', 4, 'QA Engineer', 'IT'),
    )
    db.execute(
        'INSERT INTO employees (name, surname, experience, responsibilities, department) VALUES (?, ?, ?, ?, ?)',
        ('Emily', 'Moore', 9, 'Product Manager', 'Product'),
    )
    db.execute(
        'INSERT INTO employees (name, surname, experience, responsibilities, department) VALUES (?, ?, ?, ?, ?)',
        ('Frank', 'Taylor', 1, 'Intern', 'IT'),
    )
    db.execute(
        'INSERT INTO employees (name, surname, experience, responsibilities, department) VALUES (?, ?, ?, ?, ?)',
        ('Grace', 'Anderson', 8, 'UX Designer', 'UX'),
    )
    db.execute(
        'INSERT INTO employees (name, surname, experience, responsibilities, department) VALUES (?, ?, ?, ?, ?)',
        ('Henry', 'Thomas', 5, 'DevOps Engineer', 'IT'),
    )
    db.execute(
        'INSERT INTO employees (name, surname, experience, responsibilities, department) VALUES (?, ?, ?, ?, ?)',
        ('Isabella', 'Jackson', 3, 'Data Scientist', 'Data'),
    )
    db.execute(
        'INSERT INTO employees (name, surname, experience, responsibilities, department) VALUES (?, ?, ?, ?, ?)',
        ('Jack', 'White', 7, 'Security Analyst', 'Security'),
    )
    db.execute(
        'INSERT INTO employees (name, surname, experience, responsibilities, department) VALUES (?, ?, ?, ?, ?)',
        ('Katherine', 'Harris', 2, 'Marketing Specialist', 'Marketing'),
    )
    db.execute(
        'INSERT INTO employees (name, surname, experience, responsibilities, department) VALUES (?, ?, ?, ?, ?)',
        ('Leo', 'Martin', 10, 'CEO', 'Management'),
    )
    db.execute(
        'INSERT INTO employees (name, surname, experience, responsibilities, department) VALUES (?, ?, ?, ?, ?)',
        ('Mia', 'Thompson', 6, 'HR Manager', 'HR'),
    )
    db.execute(
        'INSERT INTO employees (name, surname, experience, responsibilities, department) VALUES (?, ?, ?, ?, ?)',
        ('Noah', 'Garcia', 4, 'Finance Analyst', 'Finance'),
    )
    db.execute(
        'INSERT INTO employees (name, surname, experience, responsibilities, department) VALUES (?, ?, ?, ?, ?)',
        ('Olivia', 'Martinez', 9, 'Legal Counsel', 'Legal'),
    )
    db.execute(
        'INSERT INTO employees (name, surname, experience, responsibilities, department) VALUES (?, ?, ?, ?, ?)',
        ('Patrick', 'Robinson', 1, 'Sales Representative', 'Sales'),
    )
    db.execute(
        'INSERT INTO employees (name, surname, experience, responsibilities, department) VALUES (?, ?, ?, ?, ?)',
        ('Quinn', 'Clark', 8, 'Operations Manager', 'Operations'),
    )
    db.commit()

# Register the init_db function with the app
@app.cli.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def get_employees_by_department(db, department):
    if department:
        cursor = db.execute('SELECT * FROM employees WHERE LOWER(department) = LOWER(?)', (department,))
    else:
        cursor = db.execute('SELECT * FROM employees')
    employees = cursor.fetchall()
    employees = [dict(zip([column[0] for column in cursor.description], row)) for row in employees]
    return employees

@app.route("/")
def index():
    db = get_db()
    department = request.args.get('department')
    employees = get_employees_by_department(db, department)
    return render_template("index.html", employees=employees)

@app.route("/employee/<int:employee_id>")
def employee_details(employee_id):
    db = get_db()
    cursor = db.execute('SELECT * FROM employees WHERE id = ?', (employee_id,))  # Get the cursor
    employee = cursor.fetchone()
    if employee:
        employee = dict(zip([column[0] for column in cursor.description], employee))
        return render_template("employee.html", employee=employee)
    else:
        abort(404)

if __name__ == "__main__":
    app.run(debug=True)
