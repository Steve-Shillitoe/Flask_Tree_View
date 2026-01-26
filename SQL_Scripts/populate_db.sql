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
