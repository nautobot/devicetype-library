from pathlib import Path

import pytest

from dtl_tools.visio_extract import parse_vssx_masters


def test_parse_vssx_masters():
    vssx = Path("/opt/tmp/arista/arista/Fixed-Configuration-Switches.vssx")
    if not vssx.exists():
        pytest.skip("Visio stencil not available")

    masters = parse_vssx_masters(vssx)
    assert len(masters) > 50
    names = {m.name for m in masters}
    assert any("7050CX3" in n for n in names)
    for m in masters:
        assert m.image_file.endswith((".png", ".emf", ".jpeg"))
