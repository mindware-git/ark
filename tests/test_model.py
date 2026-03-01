import pytest
import ark as ak


def test_empty_model_compile():
    """Test that a new empty model compiles successfully."""
    model = ak.Model("empty")
    result = model.compile()
    assert result.success


def test_model_name_in_output():
    """Test that the model name is included in the OpenSCAD output."""
    model = ak.Model("kitchen")
    result = model.compile()
    assert "// model: kitchen" in result.openscad


def test_single_cube_compile():
    """Test adding a single cube and compiling it to OpenSCAD."""
    model = ak.Model("cube_test")
    model.add_cube("c1", width=100, depth=50, height=30)
    result = model.compile()
    assert result.success
    assert "cube([100.0, 50.0, 30.0]);" in result.openscad


def test_duplicate_cube_id_error():
    """Test that adding two cubes with the same ID produces a ValueError."""
    model = ak.Model("dup")
    model.add_cube("c1", width=10, depth=10, height=10)
    with pytest.raises(ValueError):
        model.add_cube("c1", width=20, depth=20, height=20)


def test_invalid_dimension_error():
    """Test that adding a cube with negative dimensions produces an error."""
    model = ak.Model("invalid")
    model.add_cube("c1", width=-10, depth=10, height=10)
    result = model.compile()
    assert not result.success
    assert any("negative" in e.lower() for e in result.errors)


# Future tests placeholders


def test_top_of_dependency():
    """TODO: Test simple top_of dependency propagation."""
    pass


def test_align_x_dependency():
    """TODO: Test align_x dependency propagation."""
    pass


def test_structure_hierarchy():
    """TODO: Test nested structures and hierarchy handling."""
    pass


# ------------- Four Principles Tests ---------------


def test_hierarchy_structure():
    """Test that entities can be assigned to hierarchical structures."""
    model = ak.Model("hierarchy_test")
    root_cube = model.add_cube("root", width=100, depth=100, height=50)
    child_cube = model.add_cube("child", width=50, depth=50, height=25, z=0)
    # For now we just check that child exists and can reference root (future: parent/child structure)
    model.add_top_of("child", "root")
    result = model.compile()
    assert result.success
    assert (
        "translate([0.0, 0.0, 50.0])" in result.openscad
    )  # child.z == root.z + root.height


def test_semantic_tag_assignment():
    """Test that semantic tags are stored correctly in entities."""
    model = ak.Model("semantic_test")
    cube = model.add_cube("c1", width=10, depth=10, height=10, semantic="#Public")
    result = model.compile()
    assert result.success
    assert cube.semantic == "#Public"


def test_dependency_resolution():
    """Test that dependencies affect entity placement deterministically."""
    model = ak.Model("dependency_test")
    base = model.add_cube("base", width=100, depth=100, height=50, z=0)
    top = model.add_cube("top", width=50, depth=50, height=25)
    model.add_top_of("top", "base")
    result = model.compile()
    assert result.success
    assert "translate([0.0, 0.0, 50.0])" in result.openscad


def test_constraints_enforcement():
    """Test that basic constraint violations are detected."""
    model = ak.Model("constraint_test")
    # negative dimension is a simple hard constraint
    model.add_cube("bad_cube", width=-10, depth=10, height=10)
    result = model.compile()
    assert not result.success
    assert any("negative" in e.lower() for e in result.errors)
