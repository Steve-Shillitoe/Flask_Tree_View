from AnimalKingdom import db  # Importing db from the main app, see __init__.py for context

print("Models imported")

class HierarchyNode(db.Model):
    __tablename__ = "HierarchyNode"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("HierarchyNode.id"))

    children = db.relationship("HierarchyNode")
    images = db.relationship("NodeImage", backref="node")


class NodeImage(db.Model):
    __tablename__ = "NodeImage"

    id = db.Column(db.Integer, primary_key=True)
    node_id = db.Column(db.Integer, db.ForeignKey("HierarchyNode.id"))
    image_path = db.Column(db.String(500), nullable=False)
    caption = db.Column(db.String(200))


def build_tree(nodes, parent_id=None):
    tree = []
    for node in nodes:
        if node.parent_id == parent_id:
            tree.append({
                "id": node.id,
                "name": node.name,
                "images": [
                    {"path": img.image_path, "caption": img.caption}
                    for img in node.images
                ],
                "children": build_tree(nodes, node.id)
            })
    return tree
