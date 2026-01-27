# Flask Tree View - A Hierarchical Image Explorer
## AnimalKingdom – Hierarchical Tree View with Flask and SQL Server
**AnimalKingdom** is a Flask-based web application that demonstrates how to model, persist, and render hierarchical data using a clean, modular architecture. The application stores a self-referencing hierarchy in Microsoft SQL Server and displays it as an interactive, expandable tree view, with images attached to leaf nodes.

The project uses Flask’s **app factory pattern** and **Blueprints** to keep configuration, routing, and domain logic clearly separated. Database access is handled via **Flask-SQLAlchemy**, with schema evolution managed using **Flask-Migrate**. The hierarchical domain model maps naturally to the UI, allowing users to progressively explore the data by expanding and collapsing branches of the tree.

The user interface is rendered server-side using **Jinja templates**, with lightweight JavaScript providing expand/collapse behaviour. This approach keeps client-side complexity low while still delivering an intuitive, interactive experience.

The codebase is structured for maintainability and extensibility, making it straightforward to add new hierarchy levels, additional content types, or future features such as REST APIs or administrative tools.

## Architecture Overview

This Flask web application uses the **app factory pattern** combined with **Blueprints** to provide a clean, modular, and scalable structure. The application is created dynamically via a ```create_app()``` function, which is responsible for configuring the app, initialising extensions, importing models, and registering routes. This avoids global state and ensures compatibility with Flask CLI tooling, database migrations, and multiple execution environments (CLI, Visual Studio, WSGI servers).

Routing and view logic are organised using **Blueprints**, allowing request-handling code to remain separate from application setup. This makes the codebase easier to reason about and enables future expansion, such as adding APIs or admin views, without restructuring the core application.

Data persistence is handled using **Flask-SQLAlchemy** with a single shared database instance, initialised within the app factory. The domain model represents a **self-referencing hierarchy** (parent–child relationships), with images attached to leaf nodes. This structure maps naturally to the expandable tree view rendered in the UI.

The user interface is **server-rendered using Jinja templates**, with minimal JavaScript added to provide expand/collapse behaviour. This approach keeps the application simple, accessible, and easy to debug, while still offering an interactive experience.

The application uses Flask’s app factory pattern, with create_app() in AnimalKingdom/__init__.py acting as the primary entry point, while run.py is provided as a development launcher for IDE-based workflows.

## Architecture Overview (Technical Interview / Portfolio Version)
This application is built using Flask’s **app factory pattern**, allowing the application instance to be created dynamically with configuration, extensions, and routes initialised in a controlled way. This avoids global state, enables clean dependency initialisation, and ensures compatibility with Flask CLI tooling, database migrations, and multiple deployment environments.

Routing and request handling are organised using **Blueprints**, which encapsulate related view functions independently of the application instance. Blueprints are registered within the app factory, keeping application setup separate from request logic and making the codebase easier to extend with additional features such as APIs or administrative views.

Data access is handled through **Flask-SQLAlchemy**, using a single shared database instance initialised within the factory. The domain model represents hierarchical data using self-referencing relationships, allowing parent–child structures to be queried efficiently. Leaf nodes in the hierarchy are associated with image records, enabling the UI to render both structure and content in a single pass.

The user interface is rendered server-side using **Jinja templates**, producing a fully-formed HTML representation of the hierarchy. Lightweight JavaScript is then used to progressively enhance the UI with expand and collapse behaviour, keeping client-side complexity low while maintaining an interactive experience.

Overall, this architecture prioritises clarity, modularity, and maintainability, while remaining simple to deploy and reason about.
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

This project uses Flask’s **app factory pattern**, with ```create_app()``` in ```AnimalKingdom/__init__.py``` acting as the primary entry point. When run via the Flask CLI or deployed under IIS using wfastcgi, the application is created by calling create_app() and returning a fully configured Flask instance.

For development and IDE-based workflows, a small launcher script may be used to import and invoke create_app(). In production, IIS loads the application via a WSGI entry point that references the app returned by the factory, ensuring a single, consistent application instance across environments.

```
Flask CLI        → calls create_app()
Visual Studio    → imports create_app()
IIS / wfastcgi   → imports create_app()
```
## Running the Web App
### Running the App Locally (Flask CLI)

To run the application in a development environment using the Flask CLI:

#### 1.Activate your virtual environment:
```
cd C:\path\to\Flask_Tree_View
.\venv\Scripts\Activate.ps1
```
Set the Flask app environment variable:
```
$env:FLASK_APP="AnimalKingdom:create_app"
$env:FLASK_ENV="development"  # optional, enables debug mode
```
#### 2.Run the development server:
```
python -m flask run
```
Open the browser:
```
http://127.0.0.1:5000
```
#### Notes:
The development server automatically reloads on code changes when ```FLASK_ENV=development```.

Do not use app.run() manually when running with the Flask CLI — the CLI manages the server lifecycle.

## Quick Start

Follow these steps to get the AnimalKingdom web app running locally:

### Clone the repository:
```
git clone https://github.com/your-username/AnimalKingdom.git
cd AnimalKingdom
```
### Create and activate a virtual environment:
```
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
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

Leaf-node images are displayed in the tree view. Expand and collapse branches by clicking the links.

## Database setup
CREATE DATABASE AnimalKingdom;
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
### Blueprints
Blueprints allow a Flask application to be split into smaller, well-organised parts. Instead of defining all routes in a single file, related routes are grouped together and registered with the application when it starts. This makes the code easier to read, reason about, and extend as the project grows. Blueprints are especially useful when using the app factory pattern, where the Flask app is created dynamically rather than as a global object.

#### Why Blueprints matter in this project
In this project, Blueprints are used to separate application setup (configuration, database initialisation, and migrations) from request-handling logic. The tree-view UI routes are defined in a Blueprint and registered within the app factory, ensuring they are correctly wired to the shared SQLAlchemy database instance. This structure allows the hierarchy and image-rendering logic to remain cleanly organised, makes future expansion (such as adding a REST API or admin interface) straightforward, and ensures compatibility with Flask CLI commands and Visual Studio’s development server.
