"""
Unit tests for the build_tree helper function.
"""

from AnimalKingdom.models import build_tree


class MockImage:
    """Simple stand-in for NodeImage ORM objects."""

    def __init__(self, image_path, caption=None):
        self.image_path = image_path
        self.caption = caption


class MockNode:
    """Simple stand-in for HierarchyNode ORM objects."""

    def __init__(self, id, name, parent_id=None, images=None):
        self.id = id
        self.name = name
        self.parent_id = parent_id
        self.images = images or []


def test_build_tree_single_root():
    """A single root node with no children should produce a one-item tree."""
    nodes = [
        MockNode(1, "Animals")
    ]

    tree = build_tree(nodes)

    assert len(tree) == 1
    assert tree[0]["name"] == "Animals"
    assert tree[0]["children"] == []
    assert tree[0]["images"] == []


def test_build_tree_two_level_hierarchy():
    """A parent with children should nest correctly."""
    nodes = [
        MockNode(1, "Animals"),
        MockNode(2, "Mammals", parent_id=1),
        MockNode(3, "Reptiles", parent_id=1),
    ]

    tree = build_tree(nodes)

    assert len(tree) == 1
    assert tree[0]["name"] == "Animals"
    assert len(tree[0]["children"]) == 2

    child_names = {child["name"] for child in tree[0]["children"]}
    assert child_names == {"Mammals", "Reptiles"}


def test_build_tree_deep_hierarchy():
    """Multiple nested levels should be handled recursively."""
    nodes = [
        MockNode(1, "Animals"),
        MockNode(2, "Mammals", parent_id=1),
        MockNode(3, "Mustelids", parent_id=2),
        MockNode(4, "Polecat", parent_id=3),
    ]

    tree = build_tree(nodes)

    animals = tree[0]
    mammals = animals["children"][0]
    mustelids = mammals["children"][0]
    polecat = mustelids["children"][0]

    assert animals["name"] == "Animals"
    assert mammals["name"] == "Mammals"
    assert mustelids["name"] == "Mustelids"
    assert polecat["name"] == "Polecat"
    assert polecat["children"] == []


def test_build_tree_leaf_node_with_images():
    """Leaf nodes should include associated images."""
    nodes = [
        MockNode(1, "Animals"),
        MockNode(
            2,
            "Ferret",
            parent_id=1,
            images=[
                MockImage("/images/mustelids/ferret.jpg", "Ferret")
            ],
        ),
    ]

    tree = build_tree(nodes)
    otter = tree[0]["children"][0]

    assert otter["name"] == "Ferret"
    assert len(otter["images"]) == 1
    assert otter["images"][0]["path"] == "/images/mustelids/ferret.jpg"
    assert otter["images"][0]["caption"] == "Ferret"

    