from flask import Blueprint, render_template
from AnimalKingdom.models import HierarchyNode, build_tree
from AnimalKingdom import db

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    nodes = (
        db.session.query(HierarchyNode)
        .options(db.joinedload(HierarchyNode.images))
        .all()
    )

    tree = build_tree(nodes)
    return render_template("tree.html", tree=tree)

