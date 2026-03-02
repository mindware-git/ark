import pytest
import ark as ak


def test_single_cube_compile():
    """Single cube should compile to OpenSCAD."""
    model = ak.Model("cube_test")
    model.add_cube("c1", width=100, depth=50, height=30)
    result = model.compile()
    assert result.success
    assert "translate([0.0, 0.0, 0.0]) cube([100.0, 50.0, 30.0]);" in result.openscad


def test_top_of_dependency():
    """Solver should adjust child.z based on parent top."""
    model = ak.Model("topof_test")
    model.add_cube("base", width=100, depth=100, height=50, z=0)
    model.add_cube("top", width=50, depth=50, height=25)
    model.add_top_of("top", "base")
    result = model.compile()
    assert result.success
    # top cube z should be base.z + base.height = 0 + 50 = 50
    assert "translate([0.0, 0.0, 50.0]) cube([50.0, 50.0, 25.0])" in result.openscad


def test_align_x_dependency():
    """Solver should adjust child.x based on parent.x"""
    model = ak.Model("alignx_test")
    model.add_cube("base", width=10, depth=10, height=10, x=100)
    model.add_cube("child", width=5, depth=5, height=5, x=0)
    model.add_align_x("child", "base")
    result = model.compile()
    assert result.success
    assert "translate([100.0, 0.0, 0.0]) cube([5.0, 5.0, 5.0]);" in result.openscad


def test_duplicate_id_error():
    """Adding two cubes with same id should produce a ValueError."""
    model = ak.Model("dup_test")
    model.add_cube("c1", width=10, depth=10, height=10)
    with pytest.raises(ValueError):
        model.add_cube("c1", width=20, depth=20, height=20)


def test_invalid_dimensions():
    """Cube with negative dimensions should produce error."""
    model = ak.Model("invalid_test")
    model.add_cube("c1", width=-10, depth=10, height=10)
    result = model.compile()
    assert not result.success
    assert any("negative" in e.lower() for e in result.errors)
