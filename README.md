# Flask Tree View - A Hierarchical Image Explorer
## Database setup
CREATE DATABASE AnimalKingdom;
### Database Migration Instructions (Flask + SQLAlchemy + Flask-Migrate)
#### 1️⃣ Setup

Before performing any migration:

Make sure your virtual environment is activated:

.\venv\Scripts\activate

Make sure your FLASK_APP environment variable points to your app factory:

$env:FLASK_APP="AnimalKingdom:create_app"
$env:FLASK_ENV="development"  # optional for debugging

#### 2️⃣ Initial Migration (First Time Only)

If this is the first time setting up the database:

Initialize Alembic migrations:

flask db init

This creates a migrations/ folder and alembic.ini.

No need to edit alembic.ini — Flask-Migrate will use your SQLALCHEMY_DATABASE_URI from config.py.

Generate the initial migration script:

flask db migrate -m "Initial schema"

Apply the migration to the database:

flask db upgrade

#### 3️⃣ Updating the Database After Modifying Models

Whenever you change or add tables/columns in models.py:

Generate a new migration:

flask db migrate -m "Descriptive message about changes"

Example:

flask db migrate -m "Add description field to NodeImage"

Apply the migration to the database:

flask db upgrade

Verify changes in SQL Server using SSMS or a query like:

SELECT COLUMN_NAME, TABLE_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME IN ('HierarchyNode', 'NodeImage');

#### 4️⃣ Rolling Back a Migration (Optional)

If a migration introduces errors, you can downgrade:

List the current revision:

flask db current

Downgrade to the previous revision:

flask db downgrade

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

