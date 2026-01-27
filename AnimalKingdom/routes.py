"""
Route definitions for the AnimalKingdom web application.

This module defines Blueprint-based routes responsible for handling
HTTP requests and rendering the hierarchical tree view UI.
"""

from flask import Blueprint, render_template

from AnimalKingdom import db
from AnimalKingdom.models import HierarchyNode, build_tree

# Create a Blueprint for main application routes.
# Blueprints allow routes to be registered with the application
# inside the app factory.
bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    """
    Render the root hierarchy tree view.

    Queries all hierarchy nodes and their associated images,
    builds an in-memory tree structure, and renders the tree
    using a Jinja template.

    Returns:
        str: Rendered HTML page displaying the expandable tree view.
    """
    # Query all hierarchy nodes and eagerly load related images
    # to avoid N+1 query issues.
    # Eager loading is a database access strategy where related data is 
    # loaded at the same time as the main query, instead of being fetched later on demand.
    # db.joinedload loads parent and related rows in a single query using an SQL JOIN.
    nodes = (
        db.session.query(HierarchyNode)
        .options(db.joinedload(HierarchyNode.images))
        .all()
    )

    # Build a nested tree structure from the flat node list
    tree = build_tree(nodes)

    # Render the tree view template
    return render_template("tree.html", tree=tree)
