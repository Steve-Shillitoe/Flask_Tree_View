from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

