import pytest
import ark as ak


def test_entity_creation():
    """Test that an Entity can be created with correct properties."""
    ent = ak.Entity(
        id="c1",
        width=100,
        depth=50,
        height=30,
        x=10,
        y=20,
        z=5,
        semantic="CABINET",
        source_file="test_file.py",
        source_line=42,
    )

    assert ent.id == "c1"
    assert ent.width == 100
    assert ent.depth == 50
    assert ent.height == 30
    assert ent.x == 10
    assert ent.y == 20
    assert ent.z == 5
    assert ent.semantic == "CABINET"
    assert ent.source_file == "test_file.py"
    assert ent.source_line == 42


def test_entity_repr():
    """Test that Entity __repr__ returns a string containing key information."""
    ent = ak.Entity(id="c2", width=10, depth=10, height=10)
    rep = repr(ent)
    assert "c2" in rep
    assert "width=10" in rep
