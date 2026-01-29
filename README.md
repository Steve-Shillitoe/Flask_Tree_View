![CI](https://github.com/Steve-Shillitoe/Flask_Tree_View/actions/workflows/python_app.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.14%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.x-black)

# AnimalKingdom – Hierarchical Tree View with Flask and SQL Server

## Description
**AnimalKingdom** is a portfolio-focused demonstration of Flask application architecture and relational data modelling. It is an interactive Flask web application that demonstrates how to model, persist, and render hierarchical data using a clean, modular architecture. The application stores a self-referencing hierarchy in a Microsoft SQL Server database and displays it as an expandable tree view, with images attached to leaf nodes and displayed in a modal popup.

![TreeViewDemo](https://github.com/user-attachments/assets/18f4e99c-eaef-4438-9cdd-4f8bcd02484f)

---

## Key Features

- **Hierarchical data modelling** using SQLAlchemy self-referencing relationships  
- **Interactive tree view** with expand/collapse functionality  
- **Image modal popup** for leaf-node images  
- **Database migrations** managed with Flask-Migrate and Alembic  
- **Clean architecture** using the app factory pattern and Blueprints  
- **Minimal frontend JavaScript**, keeping client-side complexity low  
- **Unit tests** for tree-building logic  
- **CI pipeline** using GitHub Actions  

---

## Tech Stack

**Backend**: Python, Flask, Flask-SQLAlchemy, Flask-Migrate  
**Database**: Microsoft SQL Server  
**Frontend**: HTML, CSS, Vanilla JavaScript  
**Testing**: pytest  
**CI**: GitHub Actions  

---

## Architecture Overview

This application uses Flask’s **app factory pattern**, with the application instance created dynamically via a `create_app()` function. This approach avoids global state, ensures compatibility with Flask CLI tooling and database migrations, and supports multiple execution environments.

Routing and request handling are organised using **Blueprints**, keeping application setup separate from view logic and enabling future expansion without restructuring the core application.

Data persistence is handled using **Flask-SQLAlchemy**, with a domain model representing a **self-referencing hierarchy**. Leaf nodes may be associated with image records, allowing the hierarchy and content to be rendered efficiently in a single pass.

The UI is **server-rendered using Jinja templates**, with small amounts of JavaScript used to progressively enhance the experience through expand/collapse behaviour and modal image display.

## Request Lifecycle
```
Browser
   │
   │  HTTP GET /
   ▼
Flask Application
(create_app)
   │
   │  Route matched via Blueprint
   ▼
View Function (routes.py)
   │
   │  Query hierarchy + images
   ▼
SQLAlchemy ORM
   │
   │  SQL queries
   ▼
MS SQL Server
   │
   │  Result set
   ▲
   │
SQLAlchemy ORM
   │
   │  Python objects
   ▼
Tree Builder (models.py)
   │
   │  Nested tree structure
   ▼
Jinja Template (tree.html)
   │
   │  HTML rendered
   ▼
Browser
   │
   │  Expand / collapse via JavaScript

```
## Application Entry Point

The primary entry point is the `create_app()` function in `AnimalKingdom/__init__.py`. This function is used consistently across environments:

```
Flask CLI        → calls create_app()
Visual Studio    → imports create_app()
IIS / wfastcgi   → imports create_app()
```

## Local Development Setup
### Prerequisites

- Python 3.14+
- Microsoft SQL Server (local instance)
- ODBC Driver 17 for SQL Server
- Windows Authentication enabled

The database connection string is defined in ```config.py``` in the root of **AnimalKingdom** as
```
SQLALCHEMY_DATABASE_URI = (
    "mssql+pyodbc://@localhost\\SQLEXPRESS/AnimalKingdom"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
    "&TrustServerCertificate=yes"
)
```

Update this connection string if your SQL Server instance name differs from the default.

### Installation
Follow these steps to get the AnimalKingdom web app running locally:

In Windows PowerShell issue the following commands:
### Clone the repository:
```
git clone https://github.com/Steve-Shillitoe/Flask_Tree_View/
cd AnimalKingdom
```
### Create and activate a virtual environment:
```
python -m venv venv
.\venv\Scripts\Activate.ps1 
```
### Install dependencies:
```
pip install -r requirements.txt
```
### Set environment variables for Flask:
```
$env:FLASK_APP="AnimalKingdom:create_app"
$env:FLASK_ENV="development"  # enables debug mode
```
### Create the Microsoft SQL Server database
In Microsoft SQL Server Management Studio, open a query window and execute the following command.
```
CREATE DATABASE AnimalKingdom;
```
### Initialise the database:
Back in the Windows Powershell issue these commands:
```
python -m flask db init       # Only the first time
python -m flask db migrate -m "Initial migration"
python -m flask db upgrade
```
### Populate the database
The data seeded into the database has the following structure.  This repository contains images of some of the animals in this hierarchy. 
```
Animals
├── Mammals
│   ├── Primates
│   ├── Canines
│   ├── Felines
│   └── Mustelids
│       ├── Polecat
│       ├── Ferret
│       ├── Badger
│       ├── Otter
│       ├── Stoat
│       └── Weasel
├── Reptiles
├── Insects
└── Amphibians

```
In Microsoft SQL Server Management Studio, paste the SQL script **populate_db.sql** that can be found in the **SQL_Scripts** folder into another query window and run it. 

After running this SQL script, the database tables **NodeImage** and **HierarchyNode** will be populated with data.

### Run the development server:
Back in the Windows Powershell, issue this command,
```
python -m flask run
```
### Open the app in your browser:
```
http://127.0.0.1:5000
```
### Notes

The Flask CLI automatically detects routes and models via the app factory (create_app()).

Changes to models require a new migration:
```
python -m flask db migrate -m "Describe your change"
python -m flask db upgrade
```

### Unit Testing

The `build_tree` helper function is unit-tested using `pytest`.
Tests use lightweight mock objects rather than a real database,
ensuring fast and isolated test execution.

Run tests with:

```bash
pytest
```

### Continuous Integration
This project uses **GitHub Actions** to automatically run unit tests
on every push or pull request to `main`.

The workflow:
1. Sets up Python
2. Installs dependencies
3. Runs all `pytest` unit tests

This ensures that tree-building logic and other functionality
remain stable across changes.
