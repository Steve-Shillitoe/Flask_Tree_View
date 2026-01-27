"""
Database models and helper functions for the AnimalKingdom application.

This module defines the SQLAlchemy ORM models used to represent a hierarchical
taxonomy of animals and associated images. It also provides a utility function
to transform flat query results into a nested tree structure suitable for
rendering in templates.
"""

from AnimalKingdom import db  # Shared SQLAlchemy instance created in app factory

print("Models imported")


class HierarchyNode(db.Model):
    """Represents a node in the animal hierarchy.

    Each node can have a parent node (forming a self-referential hierarchy)
    and may have zero or more child nodes. Leaf nodes may have associated
    images.

    Attributes:
        id (int): Primary key for the hierarchy node.
        name (str): Human-readable name of the node.
        parent_id (int | None): Foreign key referencing the parent node.
        children (list[HierarchyNode]): Child nodes in the hierarchy.
        images (list[NodeImage]): Images associated with this node.
    """

    __tablename__ = "HierarchyNode"

    # Unique identifier for the node
    id = db.Column(db.Integer, primary_key=True)

    # Display name for the node
    name = db.Column(db.String(200), nullable=False)

    # Self-referential foreign key to model parent-child relationships
    parent_id = db.Column(
        db.Integer,
        db.ForeignKey("HierarchyNode.id"),
        nullable=True,
    )

    # Relationship to child nodes (self-referential)
    children = db.relationship("HierarchyNode")

    # Relationship to images associated with this node
    images = db.relationship("NodeImage", backref="node")


class NodeImage(db.Model):
    """Represents an image associated with a hierarchy node.

    Images are typically attached to leaf nodes in the hierarchy and are
    displayed when those nodes are expanded in the tree view.

    Attributes:
        id (int): Primary key for the image.
        node_id (int): Foreign key referencing the associated hierarchy node.
        image_path (str): Filesystem or URL path to the image.
        caption (str | None): Optional descriptive caption for the image.
    """

    __tablename__ = "NodeImage"

    # Unique identifier for the image
    id = db.Column(db.Integer, primary_key=True)

    # Foreign key linking the image to a hierarchy node
    node_id = db.Column(
        db.Integer,
        db.ForeignKey("HierarchyNode.id"),
        nullable=False,
    )

    # Path or URL to the image file
    image_path = db.Column(db.String(500), nullable=False)

    # Optional caption displayed alongside the image
    caption = db.Column(db.String(200))


def build_tree(nodes, parent_id=None):
    """Build a nested tree structure from a flat list of hierarchy nodes.

    This function converts a list of HierarchyNode ORM objects into a recursive
    dictionary-based structure that mirrors the parent-child relationships.
    It is used to prepare data for rendering the expandable tree view in the UI.

    Args:
        nodes (list[HierarchyNode]): Flat list of hierarchy nodes fetched from
            the database.
        parent_id (int | None): ID of the parent node to build the subtree for.
            Defaults to None, which builds the root level.

    Returns:
        list[dict]: A list of dictionaries representing the hierarchy tree.
        Each dictionary contains:
            - id: Node ID
            - name: Node name
            - images: List of image dictionaries
            - children: Recursively built child nodes
    """
    
    tree = []

    for node in nodes:
        # Match nodes to the current parent
        if node.parent_id == parent_id:
            tree.append({
                "id": node.id,
                "name": node.name,
                # Include associated images (eager-loaded)
                "images": [
                    {
                        "path": img.image_path,
                        "caption": img.caption,
                    }
                    for img in node.images
                ],
                # Recursively build child subtrees
                "children": build_tree(nodes, node.id),
            })

    return tree
