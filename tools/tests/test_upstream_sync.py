from dtl_tools.upstream_sync import adapt_yaml_content


def test_removes_slug():
    content = "---\nmanufacturer: Arista\nmodel: DCS-7050\nslug: arista-dcs-7050\n"
    result = adapt_yaml_content(content)
    assert "slug:" not in result


def test_removes_mgmt_only_false():
    content = (
        "---\nmanufacturer: Arista\nmodel: X\ninterfaces:\n"
        "  - name: eth1\n    type: 1000base-t\n    mgmt_only: false\n"
    )
    result = adapt_yaml_content(content)
    assert "mgmt_only: false" not in result


def test_preserves_mgmt_only_true():
    content = (
        "---\nmanufacturer: Arista\nmodel: X\ninterfaces:\n"
        "  - name: mgmt\n    type: 1000base-t\n    mgmt_only: true\n"
    )
    result = adapt_yaml_content(content)
    assert "mgmt_only: true" in result


def test_ensures_trailing_newline():
    content = "---\nmanufacturer: Arista\nmodel: X"
    result = adapt_yaml_content(content)
    assert result.endswith("\n")
