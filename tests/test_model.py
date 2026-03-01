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
    """Test that adding two cubes with the same ID produces an error."""
    model = ak.Model("dup")
    model.add_cube("c1", width=10, depth=10, height=10)
    model.add_cube("c1", width=20, depth=20, height=20)
    result = model.compile()
    assert not result.success
    assert len(result.errors) > 0


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
