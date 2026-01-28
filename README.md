# AnimalKingdom – Hierarchical Tree View with Flask and SQL Server

## Description

**AnimalKingdom** is an interactive Flask web application that demonstrates how to model, persist, and render hierarchical data using a clean, modular architecture. The application stores a self-referencing hierarchy in a Microsoft SQL Server database and displays it as an expandable tree view, with images attached to leaf nodes and displayed in a modal popup.

The project follows Flask best practices, using the **app factory pattern** and **Blueprints** to keep configuration, routing, and domain logic clearly separated. Database access is handled via **Flask-SQLAlchemy**, with schema evolution managed using **Flask-Migrate**. The UI is rendered server-side using **Jinja templates**, with lightweight JavaScript providing expand/collapse behaviour and modal image viewing.

The codebase is structured for clarity, maintainability, and extensibility, making it straightforward to add new hierarchy levels, content types, or future features such as REST APIs or administrative tools.

### Blueprints
Blueprints allow a Flask application to be split into smaller, well-organised parts. Instead of defining all routes in a single file, related routes are grouped together and registered with the application when it starts. This makes the code easier to read, reason about, and extend as the project grows. Blueprints are especially useful when using the app factory pattern, where the Flask app is created dynamically rather than as a global object.

#### Why Blueprints matter in this project
In this project, Blueprints are used to separate application setup (configuration, database initialisation, and migrations) from request-handling logic. The tree-view UI routes are defined in a Blueprint and registered within the app factory, ensuring they are correctly wired to the shared SQLAlchemy database instance. This structure allows the hierarchy and image-rendering logic to remain cleanly organised, makes future expansion (such as adding a REST API or admin interface) straightforward, and ensures compatibility with Flask CLI commands and Visual Studio’s development server.

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

## Installing AnimalKingdom
Follow these steps to get the AnimalKingdom web app running locally:

### Clone the repository:
```
git clone https://github.com/Steve-Shillitoe/Flask_Tree_View/
cd AnimalKingdom
```
### Create and activate a virtual environment:
In Windows PowerShell issue these commands,
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
### Initialize the database:
```
python -m flask db init       # Only the first time
python -m flask db migrate -m "Initial migration"
python -m flask db upgrade
```

### Seed the database with sample hierarchy and images:
See **Database setup** section below

### Run the development server:
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

## Database setup
### Database Migration Instructions (Flask + SQLAlchemy + Flask-Migrate)
#### 1️⃣ Setup

Before performing any migration:

Make sure your virtual environment is activated:
```
.\venv\Scripts\activate
```
Make sure your FLASK_APP environment variable points to your app factory:
```
$env:FLASK_APP="AnimalKingdom:create_app"
$env:FLASK_ENV="development"  # optional for debugging
```
#### 2️⃣ Initial Migration (First Time Only)

If this is the first time setting up the database:

Initialize Alembic migrations:
```
flask db init
```
This creates a migrations/ folder and alembic.ini.

No need to edit alembic.ini — Flask-Migrate will use your SQLALCHEMY_DATABASE_URI from config.py.

Generate the initial migration script:
```
flask db migrate -m "Initial schema"
```
Apply the migration to the database:
```
flask db upgrade
```
#### 3️⃣ Updating the Database After Modifying Models

Whenever you change or add tables/columns in models.py:

Generate a new migration:
```
flask db migrate -m "Descriptive message about changes"
```
Example:
```
flask db migrate -m "Add description field to NodeImage"
```
Apply the migration to the database:
```
flask db upgrade
```
Verify changes in SQL Server using SSMS or a query like:
```
SELECT COLUMN_NAME, TABLE_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME IN ('HierarchyNode', 'NodeImage');
```
#### 4️⃣ Rolling Back a Migration (Optional)

If a migration introduces errors, you can downgrade:

List the current revision:
```
flask db current
```
Downgrade to the previous revision:
```
flask db downgrade
```
⚠️ Only do this carefully, especially in production. Data in dropped columns/tables will be lost.

The data seeded into the database has the following structure.
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
```
USE AnimalKingdom;
GO

--------------------------------------------------
-- Clear existing data (optional, dev only)
--------------------------------------------------
DELETE FROM NodeImage;
DELETE FROM HierarchyNode;
GO

--------------------------------------------------
-- Level 1: Top-level node
--------------------------------------------------
DECLARE @AnimalsId INT;

INSERT INTO HierarchyNode (name, parent_id)
VALUES ('Animals', NULL);

SET @AnimalsId = SCOPE_IDENTITY();

--------------------------------------------------
-- Level 2: Animal categories
--------------------------------------------------
DECLARE @MammalsId INT;
DECLARE @ReptilesId INT;
DECLARE @InsectsId INT;
DECLARE @AmphibiansId INT;

INSERT INTO HierarchyNode (name, parent_id)
VALUES ('Mammals', @AnimalsId);
SET @MammalsId = SCOPE_IDENTITY();

INSERT INTO HierarchyNode (name, parent_id)
VALUES ('Reptiles', @AnimalsId);
SET @ReptilesId = SCOPE_IDENTITY();

INSERT INTO HierarchyNode (name, parent_id)
VALUES ('Insects', @AnimalsId);
SET @InsectsId = SCOPE_IDENTITY();

INSERT INTO HierarchyNode (name, parent_id)
VALUES ('Amphibians', @AnimalsId);
SET @AmphibiansId = SCOPE_IDENTITY();

--------------------------------------------------
-- Level 3: Mammal groups
--------------------------------------------------
DECLARE @PrimatesId INT;
DECLARE @CaninesId INT;
DECLARE @FelinesId INT;
DECLARE @MustelidsId INT;

INSERT INTO HierarchyNode (name, parent_id)
VALUES ('Primates', @MammalsId);
SET @PrimatesId = SCOPE_IDENTITY();

INSERT INTO HierarchyNode (name, parent_id)
VALUES ('Canines', @MammalsId);
SET @CaninesId = SCOPE_IDENTITY();

INSERT INTO HierarchyNode (name, parent_id)
VALUES ('Felines', @MammalsId);
SET @FelinesId = SCOPE_IDENTITY();

INSERT INTO HierarchyNode (name, parent_id)
VALUES ('Mustelids', @MammalsId);
SET @MustelidsId = SCOPE_IDENTITY();

--------------------------------------------------
-- Level 4: Mustelid species (leaf nodes)
--------------------------------------------------
DECLARE @PolecatId INT;
DECLARE @FerretId INT;
DECLARE @BadgerId INT;
DECLARE @OtterId INT;
DECLARE @StoatId INT;
DECLARE @WeaselId INT;

INSERT INTO HierarchyNode (name, parent_id)
VALUES ('Polecat', @MustelidsId);
SET @PolecatId = SCOPE_IDENTITY();

INSERT INTO HierarchyNode (name, parent_id)
VALUES ('Ferret', @MustelidsId);
SET @FerretId = SCOPE_IDENTITY();

INSERT INTO HierarchyNode (name, parent_id)
VALUES ('Badger', @MustelidsId);
SET @BadgerId = SCOPE_IDENTITY();

INSERT INTO HierarchyNode (name, parent_id)
VALUES ('Otter', @MustelidsId);
SET @OtterId = SCOPE_IDENTITY();

INSERT INTO HierarchyNode (name, parent_id)
VALUES ('Stoat', @MustelidsId);
SET @StoatId = SCOPE_IDENTITY();

INSERT INTO HierarchyNode (name, parent_id)
VALUES ('Weasel', @MustelidsId);
SET @WeaselId = SCOPE_IDENTITY();

--------------------------------------------------
-- Level 4: Canine species (leaf nodes)
--------------------------------------------------
DECLARE @FoxId INT;

INSERT INTO HierarchyNode (name, parent_id)
VALUES ('Fox', @CaninesId);
SET @FoxId= SCOPE_IDENTITY();
--------------------------------------------------
-- Level 4: Feline species (leaf nodes)
--------------------------------------------------
DECLARE @CatId INT;

INSERT INTO HierarchyNode (name, parent_id)
VALUES ('Cat', @FelinesId);
SET @CatId= SCOPE_IDENTITY();

--------------------------------------------------
-- Attach images to leaf nodes only
--------------------------------------------------
INSERT INTO NodeImage (node_id, image_path, caption)
VALUES
(@FoxId,  '/static/images/canines/fox.jpg',    'Red Fox'),
(@CatId, '/static/images/felines/cat.jpg', 'Domestic Cat'),
(@PolecatId, '/static/images/mustelids/polecat.jpg', 'European Polecat'),
(@FerretId,  '/static/images/mustelids/ferret.jpg',  'Domestic Ferret'),
(@BadgerId,  '/static/images/mustelids/badger.jpg',  'European Badger'),
(@OtterId,   '/static/images/mustelids/otter.jpg',   'Eurasian Otter'),
(@StoatId,   '/static/images/mustelids/stoat.jpg',   'Stoat in Winter Coat'),
(@WeaselId,  '/static/images/mustelids/weasel.jpg',  'Least Weasel');
GO

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
