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
