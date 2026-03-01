import ark as ak


def test_empty_model_compile():
    model = ak.Model("empty")
    result = model.compile()
    assert result.success
