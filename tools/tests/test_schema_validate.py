from pathlib import Path

import pytest

from dtl_tools.schema_validate import validate_device_type


def test_valid_yaml(tmp_path):
    yaml_content = "---\nmanufacturer: Test\nmodel: T-1\nslug: test-t-1\n"
    f = tmp_path / "T-1.yaml"
    f.write_text(yaml_content)
    schema_dir = Path("/opt/projects/repositories/nautobot-devicetype-library/schema")
    if not schema_dir.exists():
        pytest.skip("Schema dir not available")
    errors = validate_device_type(f, schema_dir)
    assert len(errors) == 0
